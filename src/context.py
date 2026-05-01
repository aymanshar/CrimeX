# src/context.py

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar


def derive_daylight_context(hour):
    if pd.isna(hour):
        return "unknown", 0, 0

    if 6 <= hour < 18:
        return "daylight", 1, 0

    return "darkness", 0, 1


def derive_opportunity_context(darkness_flag, is_weekend, target_context_code):
    score = 0

    if darkness_flag == 1:
        score += 1

    if is_weekend == 1:
        score += 1

    if target_context_code == "public_space":
        score += 1

    if score <= 1:
        return score, "low"

    if score == 2:
        return score, "medium"

    return score, "high"


def derive_guardianship_proxy(daylight_flag, target_context_code, darkness_flag):
    score = 0

    if daylight_flag == 1:
        score += 1

    if target_context_code == "residential":
        score += 1

    if darkness_flag == 1:
        score -= 1

    score = max(score, 0)

    if score == 0:
        return score, "low"

    if score == 1:
        return score, "medium"

    return score, "high"


def create_us_holiday_calendar(start_date, end_date):
    calendar = USFederalHolidayCalendar()

    holiday_dates = calendar.holidays(
        start=start_date,
        end=end_date
    )

    return pd.DataFrame(
        {
            "holiday_date": holiday_dates.normalize()
        }
    )


def add_holiday_features(df):
    df = df.copy()

    if "date_occured" not in df.columns:
        df["is_holiday"] = 0
        df["days_to_holiday"] = None
        df["days_from_holiday"] = None
        return df

    df["date_occured_only"] = pd.to_datetime(
        df["date_occured"],
        errors="coerce"
    ).dt.normalize()

    holiday_df = create_us_holiday_calendar(
        df["date_occured_only"].min(),
        df["date_occured_only"].max()
    )

    holiday_set = set(
        holiday_df["holiday_date"]
    )

    df["is_holiday"] = (
        df["date_occured_only"]
        .isin(holiday_set)
        .astype(int)
    )

    def closest_holiday_features(crime_date):
        if pd.isna(crime_date):
            return None, None

        day_diffs = [
            (crime_date - holiday_date).days
            for holiday_date in holiday_set
        ]

        past_diffs = [
            diff for diff in day_diffs
            if diff >= 0
        ]

        future_diffs = [
            -diff for diff in day_diffs
            if diff < 0
        ]

        days_from = (
            min(past_diffs)
            if past_diffs
            else None
        )

        days_to = (
            min(future_diffs)
            if future_diffs
            else None
        )

        return days_to, days_from

    df[
        [
            "days_to_holiday",
            "days_from_holiday"
        ]
    ] = df["date_occured_only"].apply(
        lambda x: pd.Series(
            closest_holiday_features(x)
        )
    )

    return df


def derive_holiday_context(
    is_holiday,
    is_weekend,
    days_to_holiday,
    days_from_holiday
):
    score = 0

    if is_holiday == 1:
        score += 2

    if is_weekend == 1:
        score += 1

    if pd.notna(days_to_holiday) and 0 <= days_to_holiday <= 2:
        score += 1

    if pd.notna(days_from_holiday) and 0 <= days_from_holiday <= 2:
        score += 1

    if score <= 1:
        return score, "low"

    if score <= 2:
        return score, "medium"

    return score, "high"


def derive_weather_stress_proxy(local_season_code, month):
    score = 0

    if local_season_code == "summer":
        score += 1

    if month in [7, 8]:
        score += 1

    if score == 0:
        return score, "low"

    if score == 1:
        return score, "medium"

    return score, "high"


def derive_weather_disruption_flag(weather_stress_code):
    return int(weather_stress_code == "high")


def derive_strain_context(
    opportunity_context_score,
    holiday_context_score,
    darkness_flag,
    behavioral_threat_score
):
    score = 0

    if opportunity_context_score >= 2:
        score += 1

    if holiday_context_score >= 2:
        score += 1

    if darkness_flag == 1:
        score += 1

    if behavioral_threat_score >= 8:
        score += 1

    if score <= 1:
        return score, "low"

    if score <= 2:
        return score, "medium"

    return score, "high"


def derive_routine_activity_risk(
    opportunity_score,
    guardianship_code,
    darkness_flag
):
    score = 0

    if opportunity_score >= 2:
        score += 1

    if guardianship_code == "low":
        score += 1

    if darkness_flag == 1:
        score += 1

    if score <= 1:
        return score, "low"

    if score == 2:
        return score, "medium"

    return score, "high"


def add_context_features(df):
    df = df.copy()

    df[
        [
            "daylight_context_code",
            "daylight_flag",
            "darkness_flag"
        ]
    ] = df["hour"].apply(
        lambda x: pd.Series(
            derive_daylight_context(x)
        )
    )

    df["is_weekend"] = (
        df["is_weekend"]
        .fillna(0)
        .astype(int)
    )

    df[
        [
            "opportunity_context_score",
            "opportunity_context_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_opportunity_context(
                row["darkness_flag"],
                row["is_weekend"],
                row.get("target_context_code", "other")
            )
        ),
        axis=1
    )

    df[
        [
            "guardianship_proxy_score",
            "guardianship_proxy_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_guardianship_proxy(
                row["daylight_flag"],
                row.get("target_context_code", "other"),
                row["darkness_flag"]
            )
        ),
        axis=1
    )

    df = add_holiday_features(df)

    df[
        [
            "holiday_context_score",
            "holiday_context_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_holiday_context(
                row["is_holiday"],
                row["is_weekend"],
                row["days_to_holiday"],
                row["days_from_holiday"]
            )
        ),
        axis=1
    )

    df[
        [
            "strain_context_score",
            "strain_context_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_strain_context(
                row["opportunity_context_score"],
                row["holiday_context_score"],
                row["darkness_flag"],
                row.get("behavioral_threat_score", 0)
            )
        ),
        axis=1
    )

    df[
        [
            "weather_stress_score",
            "weather_stress_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_weather_stress_proxy(
                row.get("local_season_code", "unknown"),
                row.get("month")
            )
        ),
        axis=1
    )

    df["weather_disruption_flag"] = df[
        "weather_stress_code"
    ].apply(
        derive_weather_disruption_flag
    )

    df[
        [
            "routine_activity_risk_score",
            "routine_activity_risk_code"
        ]
    ] = df.apply(
        lambda row: pd.Series(
            derive_routine_activity_risk(
                row["opportunity_context_score"],
                row["guardianship_proxy_code"],
                row["darkness_flag"]
            )
        ),
        axis=1
    )

    return df