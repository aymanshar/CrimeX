# src/explainability.py


def build_risk_explanation(row):
    reasons = []

    if row.get("behavior_signature_risk_code") == "high":
        reasons.append("high behavioral threat")

    if row.get("routine_activity_risk_code") == "high":
        reasons.append("high routine activity risk")

    if row.get("network_exposure_risk_code") in ["medium", "high"]:
        reasons.append("elevated network exposure risk")

    if row.get("record_anomaly_flag") == 1:
        reasons.append("behavioral anomaly detected")

    if not reasons:
        return "no elevated risk indicators detected"

    return " | ".join(reasons)


def build_explanation_signature(row):
    parts = []

    if row.get("behavior_signature_risk_code") == "high":
        parts.append("THREAT")

    if row.get("routine_activity_risk_code") == "high":
        parts.append("ROUTINE")

    if row.get("network_exposure_risk_code") in ["medium", "high"]:
        parts.append("NETWORK")

    if row.get("record_anomaly_flag") == 1:
        parts.append("ANOMALY")

    if not parts:
        return "BASELINE"

    return "|".join(parts)


def add_explainability_features(df):
    df = df.copy()

    df["risk_explanation_text"] = df.apply(
        build_risk_explanation,
        axis=1
    )

    df["risk_explanation_signature_code"] = df.apply(
        build_explanation_signature,
        axis=1
    )

    return df