
import pandas as pd


def safe_ratio(numerator, denominator):
    if pd.isna(denominator) or denominator == 0:
        return 0
    return numerator / denominator


def add_actor_extended_features(df):
    df = df.copy()

    # -----------------------------
    # Text richness
    # -----------------------------
    df["crime_text_length"] = df["crime_description_enhanced"].fillna("").apply(len)

    df["crime_text_word_count"] = df["crime_description_enhanced"].fillna("").apply(
        lambda x: len(str(x).split())
    )

    df["has_rich_crime_text_flag"] = (
        df["crime_text_word_count"] >= 8
    ).astype(int)

    df["short_crime_text_flag"] = (
        (df["crime_text_word_count"] > 0)
        & (df["crime_text_word_count"] < 4)
    ).astype(int)

    # -----------------------------
    # Identity density
    # -----------------------------
    df["alias_identifier_ratio"] = df.apply(
        lambda row: safe_ratio(
            row.get("alias_count", 0),
            row.get("identifier_count", 0)
        ),
        axis=1
    )

    df["identity_density_score"] = (
        df.get("alias_count", 0)
        + df.get("identifier_count", 0)
        + df.get("program_count", 0)
    )

    df["high_identity_density_flag"] = (
        df["identity_density_score"] >= 3
    ).astype(int)

    # -----------------------------
    # Geography density
    # -----------------------------
    df["address_country_ratio"] = df.apply(
        lambda row: safe_ratio(
            row.get("address_count", 0),
            row.get("actor_country_count", 0)
        ),
        axis=1
    )

    df["high_geo_complexity_flag"] = (
        (df.get("actor_country_count", 0) > 1)
        | (df.get("address_count", 0) > 2)
    ).astype(int)

    # -----------------------------
    # Temporal dynamics
    # -----------------------------
    df["short_observed_actor_flag"] = (
        df.get("actor_observed_days", 0) < 90
    ).astype(int)

    df["very_long_observed_actor_flag"] = (
        df.get("actor_observed_days", 0) >= 730
    ).astype(int)

    df["stale_record_flag"] = (
        df.get("days_since_last_change", 0) > 365
    ).astype(int)

    # -----------------------------
    # Source strength
    # -----------------------------
    df["strong_source_signal_flag"] = (
        (df.get("interpol_red_notice_flag", 0) == 1)
        | (df.get("is_wanted_flag", 0) == 1)
        | (df.get("is_terrorism_flag", 0) == 1)
    ).astype(int)

    df["weak_source_signal_flag"] = (
        df.get("source_risk_score", 0) == 0
    ).astype(int)

    # -----------------------------
    # Risk disagreement / analyst review
    # -----------------------------
    df["risk_priority_mismatch_flag"] = (
        (
            (df["actor_risk_level_v3"] == "low")
            & (df["investigator_priority_level_refined"] != "low")
        )
        | (
            (df["actor_risk_level_v3"] == "high")
            & (df["investigator_priority_level_refined"] == "low")
        )
    ).astype(int)

    df["needs_manual_review_flag"] = (
        (df["risk_priority_mismatch_flag"] == 1)
        | (df.get("is_potential_duplicate_flag", 0) == 1)
        | (df.get("high_identity_density_flag", 0) == 1)
    ).astype(int)

    # -----------------------------
    # Data quality
    # -----------------------------
    df["core_identity_available_score"] = (
        df["offender_name"].notna().astype(int)
        + df.get("has_birth_date_flag", 0)
        + df.get("country_context_available_flag", 0)
    )

    df["data_sparse_flag"] = (
        df["core_identity_available_score"] <= 1
    ).astype(int)

    # -----------------------------
    # Investigator segment
    # -----------------------------
    def investigator_segment(row):
        if row.get("actor_risk_level_v3") == "high" and row.get("recent_high_risk_flag", 0) == 1:
            return "urgent_high_risk"

        if row.get("actor_risk_level_v3") == "high":
            return "high_risk_monitor"

        if row.get("needs_manual_review_flag", 0) == 1:
            return "manual_review"

        if row.get("actor_risk_level_v3") == "medium":
            return "medium_risk_watch"

        return "low_risk_archive"

    df["investigator_segment"] = df.apply(
        investigator_segment,
        axis=1
    )

    return df
