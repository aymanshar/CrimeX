# src/behavior.py

import pandas as pd


def classify_crime_behavior(crime_ontology_code):
    if crime_ontology_code == "fraud_identity":
        return "fraud_identity", "fraud or identity crime", "medium", "medium severity"

    if crime_ontology_code == "violent":
        return "violent", "violent crime", "high", "high severity"

    if crime_ontology_code == "property":
        return "property", "property crime", "medium", "medium severity"

    if crime_ontology_code == "child_related":
        return "child_related", "child related crime", "high", "high severity"

    if crime_ontology_code == "narcotics":
        return "narcotics", "narcotics crime", "medium", "medium severity"

    return "other", "other crime", "low", "low severity"


def derive_weapon_features(weapon_code, weapon_description):
    weapon_involved_flag = 0
    deadly_weapon_flag = 0
    unknown_weapon_flag = 0

    if pd.notna(weapon_code):
        weapon_involved_flag = 1

    weapon_text = str(weapon_description).lower()

    if (
        "knife" in weapon_text
        or "gun" in weapon_text
        or "firearm" in weapon_text
        or "deadly" in weapon_text
    ):
        deadly_weapon_flag = 1

    if "unknown" in weapon_text:
        unknown_weapon_flag = 1

    return weapon_involved_flag, deadly_weapon_flag, unknown_weapon_flag


def derive_mo_features(modus_operandi):
    if pd.isna(modus_operandi) or str(modus_operandi).strip() == "":
        return 0, 0, "none", "no modus operandi"

    mo_codes = str(modus_operandi).split()
    mo_code_count = len(mo_codes)
    multi_step_behavior_flag = int(mo_code_count > 1)

    if mo_code_count == 1:
        return mo_code_count, multi_step_behavior_flag, "simple", "single-step behavior"

    if mo_code_count <= 3:
        return mo_code_count, multi_step_behavior_flag, "moderate", "moderately complex behavior"

    return mo_code_count, multi_step_behavior_flag, "complex", "multi-step complex behavior"


def derive_target_context(crime_description, premise_description):
    crime_text = str(crime_description).lower()
    premise_text = str(premise_description).lower()

    if "identity" in crime_text:
        return "identity", "identity-related target"

    if "vehicle" in crime_text:
        return "vehicle", "vehicle-related target"

    if "child" in crime_text or "chld" in crime_text:
        return "child", "child-related target"

    if "dwelling" in premise_text or "apartment" in premise_text or "residence" in premise_text:
        return "residential", "residential target"

    if "street" in premise_text or "sidewalk" in premise_text or "alley" in premise_text:
        return "public_space", "public space target"

    return "other", "other target context"


def derive_behavior_risk_profile(
    crime_family_code,
    deadly_weapon_flag,
    multi_step_behavior_flag,
    mo_complexity_code,
    target_context_code
):
    if crime_family_code == "violent" and deadly_weapon_flag == 1:
        return "violent_high_risk", "high risk violent behavior"

    if target_context_code == "child":
        return "vulnerable_targeted", "crime targeting vulnerable victims"

    if multi_step_behavior_flag == 1 and mo_complexity_code == "complex":
        return "organized_complex", "organized or complex behavior"

    if crime_family_code == "fraud_identity":
        return "structured_fraud", "structured fraud behavior"

    if crime_family_code == "property":
        return "opportunistic_property", "opportunistic property behavior"

    return "general_risk", "general risk behavior"


def derive_criminal_sophistication(
    multi_step_behavior_flag,
    mo_complexity_code,
    deadly_weapon_flag,
    crime_family_code
):
    score = 0

    if multi_step_behavior_flag == 1:
        score += 1

    if mo_complexity_code == "complex":
        score += 2

    if deadly_weapon_flag == 1:
        score += 1

    if crime_family_code == "fraud_identity":
        score += 1

    if score <= 1:
        return score, "low"

    if score <= 3:
        return score, "medium"

    return score, "high"


def derive_behavior_signature_risk(
    behavior_risk_profile_code,
    deadly_weapon_flag,
    criminal_sophistication_score,
    target_context_code
):
    score = 0

    if behavior_risk_profile_code == "violent_high_risk":
        score += 4
    elif behavior_risk_profile_code == "vulnerable_targeted":
        score += 3
    elif behavior_risk_profile_code == "organized_complex":
        score += 2
    elif behavior_risk_profile_code == "structured_fraud":
        score += 1

    if deadly_weapon_flag == 1:
        score += 2

    score += min(criminal_sophistication_score, 3)

    if target_context_code == "child":
        score += 2

    if score <= 2:
        return score, "low"

    if score <= 5:
        return score, "medium"

    return score, "high"


def build_behavior_signature_text(row):
    parts = [
        str(row.get("crime_family_desc", "")),
        str(row.get("target_context_desc", "")),
        str(row.get("behavior_risk_profile_desc", "")),
        str(row.get("mo_complexity_desc", "")),
    ]

    weapon_desc = str(row.get("weapon_description", "")).lower()

    if weapon_desc and weapon_desc != "unknown":
        parts.append(weapon_desc)

    return " | ".join([p for p in parts if p and p != "nan"])


def build_behavior_signature_key(row):
    parts = [
        str(row["crime_family_code"]),
        str(row["target_context_code"]),
        str(row["behavior_risk_profile_code"]),
        str(row["mo_complexity_code"]),
        str(row["deadly_weapon_flag"]),
    ]

    return "|".join(parts)


def derive_escalation_potential(
    behavior_risk_profile_code,
    behavior_signature_risk_code,
    deadly_weapon_flag,
    crime_family_code
):
    score = 0

    if behavior_risk_profile_code == "violent_high_risk":
        score += 3

    if behavior_risk_profile_code == "vulnerable_targeted":
        score += 2

    if behavior_signature_risk_code == "high":
        score += 2

    if deadly_weapon_flag == 1:
        score += 2

    if crime_family_code == "violent":
        score += 1

    if score <= 2:
        return score, "low"

    if score <= 5:
        return score, "medium"

    return score, "high"


def derive_behavioral_diversity(
    mo_complexity_code,
    behavior_signature_rarity_code,
    criminal_sophistication_score
):
    score = 0

    if mo_complexity_code == "moderate":
        score += 1

    if mo_complexity_code == "complex":
        score += 2

    if behavior_signature_rarity_code == "uncommon":
        score += 2

    if behavior_signature_rarity_code == "rare":
        score += 3

    if criminal_sophistication_score >= 3:
        score += 1

    if score <= 1:
        return score, "low"

    if score <= 3:
        return score, "medium"

    return score, "high"


def derive_behavioral_threat(
    behavior_signature_risk_score,
    escalation_potential_score,
    behavioral_diversity_score
):
    score = (
        behavior_signature_risk_score
        + escalation_potential_score
        + behavioral_diversity_score
    )

    if score <= 4:
        return score, "low"

    if score <= 8:
        return score, "medium"

    return score, "high"


def derive_offender_persistence_proxy(
    mo_complexity_code,
    behavior_signature_rarity_code,
    criminal_sophistication_score,
    behavior_risk_profile_code
):
    score = 0

    if behavior_risk_profile_code == "organized_complex":
        score += 2

    if behavior_signature_rarity_code == "rare":
        score += 2
    elif behavior_signature_rarity_code == "uncommon":
        score += 1

    if criminal_sophistication_score >= 3:
        score += 1

    if mo_complexity_code == "complex":
        score += 1

    if score <= 1:
        return score, "low"

    if score <= 3:
        return score, "medium"

    return score, "high"


def derive_behavioral_anomaly_flag(
    behavior_signature_rarity_code,
    behavioral_threat_code,
    behavioral_diversity_code,
    escalation_potential_code,
    criminal_sophistication_code
):
    if behavior_signature_rarity_code == "rare" and behavioral_threat_code == "high":
        return 1

    if behavioral_diversity_code == "high" and escalation_potential_code in ["medium", "high"]:
        return 1

    if criminal_sophistication_code == "high" and behavioral_threat_code == "high":
        return 1

    return 0


def add_behavior_features(df):
    df = df.copy()

    df[["crime_family_code", "crime_family_desc", "crime_severity_code", "crime_severity_desc"]] = (
        df["crime_ontology_code"].apply(lambda x: pd.Series(classify_crime_behavior(x)))
    )

    df[["weapon_involved_flag", "deadly_weapon_flag", "unknown_weapon_flag"]] = df.apply(
        lambda row: pd.Series(
            derive_weapon_features(
                row.get("weapon_code"),
                row.get("weapon_description")
            )
        ),
        axis=1
    )

    df[["mo_code_count", "multi_step_behavior_flag", "mo_complexity_code", "mo_complexity_desc"]] = (
        df.get("modus_operandi", pd.Series([None] * len(df))).apply(
            lambda x: pd.Series(derive_mo_features(x))
        )
    )

    df[["target_context_code", "target_context_desc"]] = df.apply(
        lambda row: pd.Series(
            derive_target_context(
                row.get("crime_description_canonical_en"),
                row.get("premise_description")
            )
        ),
        axis=1
    )

    df[["behavior_risk_profile_code", "behavior_risk_profile_desc"]] = df.apply(
        lambda row: pd.Series(
            derive_behavior_risk_profile(
                row["crime_family_code"],
                row["deadly_weapon_flag"],
                row["multi_step_behavior_flag"],
                row["mo_complexity_code"],
                row["target_context_code"]
            )
        ),
        axis=1
    )

    df[["criminal_sophistication_score", "criminal_sophistication_code"]] = df.apply(
        lambda row: pd.Series(
            derive_criminal_sophistication(
                row["multi_step_behavior_flag"],
                row["mo_complexity_code"],
                row["deadly_weapon_flag"],
                row["crime_family_code"]
            )
        ),
        axis=1
    )

    df[["behavior_signature_risk_score", "behavior_signature_risk_code"]] = df.apply(
        lambda row: pd.Series(
            derive_behavior_signature_risk(
                row["behavior_risk_profile_code"],
                row["deadly_weapon_flag"],
                row["criminal_sophistication_score"],
                row["target_context_code"]
            )
        ),
        axis=1
    )

    df["behavior_signature_text"] = df.apply(
        build_behavior_signature_text,
        axis=1
    )

    df["behavior_signature_key"] = df.apply(
        build_behavior_signature_key,
        axis=1
    )

    signature_counts = df["behavior_signature_key"].value_counts()

    df["behavior_signature_frequency"] = df["behavior_signature_key"].map(
        signature_counts
    )

    df["behavior_signature_rarity_code"] = df["behavior_signature_frequency"].apply(
        lambda x: "rare" if x <= 20 else ("uncommon" if x <= 500 else "common")
    )

    df[["escalation_potential_score", "escalation_potential_code"]] = df.apply(
        lambda row: pd.Series(
            derive_escalation_potential(
                row["behavior_risk_profile_code"],
                row["behavior_signature_risk_code"],
                row["deadly_weapon_flag"],
                row["crime_family_code"]
            )
        ),
        axis=1
    )

    df[["behavioral_diversity_score", "behavioral_diversity_code"]] = df.apply(
        lambda row: pd.Series(
            derive_behavioral_diversity(
                row["mo_complexity_code"],
                row["behavior_signature_rarity_code"],
                row["criminal_sophistication_score"]
            )
        ),
        axis=1
    )

    df[["behavioral_threat_score", "behavioral_threat_code"]] = df.apply(
        lambda row: pd.Series(
            derive_behavioral_threat(
                row["behavior_signature_risk_score"],
                row["escalation_potential_score"],
                row["behavioral_diversity_score"]
            )
        ),
        axis=1
    )

    df[["offender_persistence_proxy_score", "offender_persistence_proxy_code"]] = df.apply(
        lambda row: pd.Series(
            derive_offender_persistence_proxy(
                row["mo_complexity_code"],
                row["behavior_signature_rarity_code"],
                row["criminal_sophistication_score"],
                row["behavior_risk_profile_code"]
            )
        ),
        axis=1
    )

    df["behavioral_anomaly_flag"] = df.apply(
        lambda row: derive_behavioral_anomaly_flag(
            row["behavior_signature_rarity_code"],
            row["behavioral_threat_code"],
            row["behavioral_diversity_code"],
            row["escalation_potential_code"],
            row["criminal_sophistication_code"]
        ),
        axis=1
    )

    return df