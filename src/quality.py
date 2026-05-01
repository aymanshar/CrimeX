# src/quality.py

import pandas as pd


QUALITY_REQUIRED_FIELDS = [
    "case_id",
    "crime_description_raw",
    "latitude_final",
    "crime_ontology_code",
]


def calculate_completeness_score(row, required_fields=QUALITY_REQUIRED_FIELDS):
    available_count = 0

    for field in required_fields:
        if field in row.index and pd.notna(row[field]):
            available_count += 1

    return available_count / len(required_fields)


def derive_consistency_flag(row):
    scores = [
        row.get("criminal_sophistication_score", 0),
        row.get("behavior_signature_risk_score", 0),
        row.get("opportunity_context_score", 0),
    ]

    for score in scores:
        if pd.notna(score) and score < 0:
            return 0

    return 1


def calculate_enrichment_confidence(completeness_score, consistency_flag, source_reliability_score=0.80):
    score = (completeness_score + consistency_flag + source_reliability_score) / 3

    if score >= 0.85:
        return score, "high"

    if score >= 0.65:
        return score, "medium"

    return score, "low"


def derive_record_anomaly_flag(row):
    if (
        row.get("behavior_signature_risk_code") == "high"
        and row.get("behavior_signature_rarity_code") == "uncommon"
    ):
        return 1

    if row.get("enrichment_confidence_code") == "low":
        return 1

    return 0


def derive_review_priority(record_anomaly_flag, behavioral_threat_code):
    if record_anomaly_flag == 1 and behavioral_threat_code == "high":
        return "priority_review"

    if record_anomaly_flag == 1:
        return "review"

    return "normal"


def add_quality_features(df):
    df = df.copy()

    df["completeness_score"] = df.apply(
        calculate_completeness_score,
        axis=1
    )

    df["consistency_flag"] = df.apply(
        derive_consistency_flag,
        axis=1
    )

    df[["enrichment_confidence_score", "enrichment_confidence_code"]] = df.apply(
        lambda row: pd.Series(
            calculate_enrichment_confidence(
                row["completeness_score"],
                row["consistency_flag"]
            )
        ),
        axis=1
    )

    df["record_anomaly_flag"] = df.apply(
        derive_record_anomaly_flag,
        axis=1
    )

    df["analyst_review_priority_code"] = df.apply(
        lambda row: derive_review_priority(
            row["record_anomaly_flag"],
            row.get("behavior_signature_risk_code", "low")
        ),
        axis=1
    )

    return df