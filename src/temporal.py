# src/temporal.py

import pandas as pd


def standardize_datetime_columns(df):
    """
    Convert available date and time columns into datetime fields.
    """
    df = df.copy()

    if "date_reported" in df.columns:
        df["date_reported"] = pd.to_datetime(
            df["date_reported"],
            errors="coerce"
        )

    if "date_occured" in df.columns:
        df["date_occured"] = pd.to_datetime(
            df["date_occured"],
            errors="coerce"
        )

    if "time_occured" in df.columns:
        df["time_occured"] = (
            df["time_occured"]
            .astype(str)
            .str.zfill(4)
        )

        df["time_occured"] = pd.to_datetime(
            df["time_occured"],
            format="%H%M",
            errors="coerce"
        ).dt.time

    return df


def create_datetime_occured(df):
    """
    Create datetime_occured from date_occured and time_occured when available.
    """
    df = df.copy()

    if "date_occured" in df.columns and "time_occured" in df.columns:
        df["datetime_occured"] = pd.to_datetime(
            df["date_occured"].astype(str)
            + " "
            + df["time_occured"].astype(str),
            errors="coerce"
        )

    elif "date_occured" in df.columns:
        df["datetime_occured"] = pd.to_datetime(
            df["date_occured"],
            errors="coerce"
        )

    else:
        df["datetime_occured"] = pd.NaT

    return df


def get_hemisphere_code(latitude):
    """
    Return hemisphere from latitude.
    """
    if pd.isna(latitude):
        return "unknown"

    if latitude > 0:
        return "north"

    if latitude < 0:
        return "south"

    return "equator"


def get_local_season_code(month, hemisphere_code):
    """
    Return localized season based on month and hemisphere.
    """
    if pd.isna(month) or hemisphere_code == "unknown":
        return "unknown"

    if hemisphere_code == "north":
        if month in [12, 1, 2]:
            return "winter"
        if month in [3, 4, 5]:
            return "spring"
        if month in [6, 7, 8]:
            return "summer"
        return "autumn"

    if hemisphere_code == "south":
        if month in [12, 1, 2]:
            return "summer"
        if month in [3, 4, 5]:
            return "autumn"
        if month in [6, 7, 8]:
            return "winter"
        return "spring"

    return "tropical"


def add_temporal_features(df):
    """
    Add temporal features from datetime_occured.
    """
    df = df.copy()

    df = standardize_datetime_columns(df)
    df = create_datetime_occured(df)

    df["year"] = df["datetime_occured"].dt.year
    df["quarter"] = df["datetime_occured"].dt.quarter
    df["month"] = df["datetime_occured"].dt.month
    df["month_name"] = df["datetime_occured"].dt.month_name()
    df["week_of_year"] = df["datetime_occured"].dt.isocalendar().week.astype("Int64")
    df["day"] = df["datetime_occured"].dt.day
    df["day_of_year"] = df["datetime_occured"].dt.dayofyear
    df["day_of_week_number"] = df["datetime_occured"].dt.dayofweek
    df["day_of_week_name"] = df["datetime_occured"].dt.day_name()
    df["hour"] = df["datetime_occured"].dt.hour

    df["is_weekend"] = df["day_of_week_number"].isin([5, 6]).astype(int)

    if "latitude_final" in df.columns:
        df["hemisphere_code"] = df["latitude_final"].apply(
            get_hemisphere_code
        )
    else:
        df["hemisphere_code"] = "unknown"

    df["local_season_code"] = df.apply(
        lambda row: get_local_season_code(
            row["month"],
            row["hemisphere_code"]
        ),
        axis=1
    )

    return df