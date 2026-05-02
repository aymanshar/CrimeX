
import pandas as pd


def split_count(value):
    if pd.isna(value):
        return 0
    return len([x for x in str(value).split(";") if x.strip()])


def get_age_group(age):
    if pd.isna(age):
        return "unknown"
    if age < 18:
        return "minor"
    if age <= 25:
        return "young_adult"
    if age <= 40:
        return "adult"
    if age <= 60:
        return "middle_age"
    return "senior"


def improved_crime_ontology(text):
    if pd.isna(text):
        return "unknown", "unknown crime ontology"

    t = str(text).lower()

    if any(k in t for k in ["terror", "terrorist", "armed formation", "illegal armed", "extremist"]):
        return "violent", "terrorism / armed group activity"

    if any(k in t for k in ["homicide", "murder", "killing", "agravado"]):
        return "violent", "serious violent crime"

    if any(k in t for k in ["fraud", "forgery", "identity", "money laundering"]):
        return "fraud_identity", "fraud or identity crime"

    if any(k in t for k in ["drug", "narcotic"]):
        return "narcotics", "narcotics crime"

    if any(k in t for k in ["child", "minor"]):
        return "child_related", "child related crime"

    return "other", "other crime"


def enhanced_crime_text(row):
    text = str(row.get("sanctions", "")).strip()
    dataset = str(row.get("source_dataset_name", row.get("dataset", ""))).lower()

    if text and text.lower() not in ["nan", "none", ""]:
        if not any(k in text.lower() for k in [
            "active", "reciprocal", "nonprocurement", "procurement", "effective", "expired"
        ]):
            return text

    if "interpol" in dataset:
        return "interpol wanted notice"

    if "terror" in dataset:
        return "terrorism related activity"

    if "wanted" in dataset:
        return "wanted person"

    if "sanction" in dataset:
        return "sanctioned individual"

    return None


def final_risk_level(score):
    if score <= 3:
        return "low"
    if score <= 7:
        return "medium"
    return "high"


def refined_priority(row):
    risk = row["actor_risk_level_v3"]
    score = row["investigator_priority_score"]

    if risk == "high":
        return "high" if score >= 10 else "medium"

    if risk == "medium":
        return "medium"

    if risk == "low":
        if row["recently_changed_actor_flag"] == 1 and row["source_risk_score"] > 0:
            return "medium"
        return "low"

    return "low"


def build_risk_explanation(row):
    reasons = []

    if row.get("risk_driver_crime_flag", 0):
        reasons.append("serious_crime")

    if row.get("risk_driver_source_flag", 0):
        reasons.append("watchlist_source")

    if row.get("risk_driver_geo_flag", 0):
        reasons.append("cross_border")

    if row.get("risk_driver_identity_flag", 0):
        reasons.append("multiple_identities")

    if row.get("risk_driver_temporal_flag", 0):
        reasons.append("long_term_activity")

    return "|".join(reasons) if reasons else "low_signal"


def add_actor_features(df):
    df = df.copy()

    # Keep only persons if schema exists
    if "schema" in df.columns:
        df = df[df["schema"] == "Person"].copy()

    # CRIMEX-compatible fields
    df["offender_id"] = df.get("id")
    df["offender_name"] = df.get("name")
    df["offender_aliases"] = df.get("aliases")
    df["offender_birth_date"] = pd.to_datetime(df.get("birth_date"), errors="coerce")
    df["offender_nationality_code"] = df.get("countries")

    df["source_system_code"] = "opensanctions"
    df["source_dataset_name"] = df.get("dataset")
    df["source_program_ids"] = df.get("program_ids")

    # Crime text
    df["sanctions"] = df.get("sanctions", "").fillna("")
    df["crime_description_raw"] = df["sanctions"].astype(str).str.split(";").str[0].str.strip()
    df["crime_description_raw"] = df["crime_description_raw"].replace(["nan", "None", ""], None)

    df["crime_description_enhanced"] = df.apply(enhanced_crime_text, axis=1)
    df["crime_text_quality_flag"] = df["crime_description_enhanced"].notna().astype(int)
    df["has_crime_text_flag"] = df["crime_text_quality_flag"]

    df[["crime_ontology_code_v3", "crime_ontology_desc_v3"]] = df["crime_description_enhanced"].apply(
        lambda x: pd.Series(improved_crime_ontology(x))
    )

    df["serious_crime_flag_v3"] = df["crime_ontology_code_v3"].isin(
        ["violent", "child_related", "narcotics"]
    ).astype(int)

    # Country features
    df["actor_country_count"] = df["offender_nationality_code"].apply(split_count)
    df["country_context_available_flag"] = (df["actor_country_count"] > 0).astype(int)
    df["multi_country_actor_flag"] = (df["actor_country_count"] > 1).astype(int)
    df["cross_border_risk_flag"] = df["multi_country_actor_flag"]

    # Age features
    df["first_seen_date"] = pd.to_datetime(df.get("first_seen"), errors="coerce")
    df["last_seen_date"] = pd.to_datetime(df.get("last_seen"), errors="coerce")
    df["last_change_date"] = pd.to_datetime(df.get("last_change"), errors="coerce")

    df["offender_age_at_first_seen"] = (
        (df["first_seen_date"] - df["offender_birth_date"]).dt.days / 365.25
    ).round(1)

    df["offender_age_group"] = df["offender_age_at_first_seen"].apply(get_age_group)
    df["has_birth_date_flag"] = df["offender_birth_date"].notna().astype(int)

    # Identity features
    df["alias_count"] = df.get("aliases", "").apply(split_count)
    df["has_alias_flag"] = (df["alias_count"] > 0).astype(int)
    df["has_multiple_aliases_flag"] = (df["alias_count"] > 1).astype(int)

    df["identifier_count"] = df.get("identifiers", "").apply(split_count)
    df["has_identifier_flag"] = (df["identifier_count"] > 0).astype(int)
    df["has_multiple_ids_flag"] = (df["identifier_count"] > 1).astype(int)

    df["identity_complexity_score"] = df["alias_count"] + df["identifier_count"]

    # Address/contact features
    df["address_count"] = df.get("addresses", "").apply(split_count)
    df["has_address_flag"] = (df["address_count"] > 0).astype(int)
    df["multi_address_flag"] = (df["address_count"] > 1).astype(int)

    df["phone_count"] = df.get("phones", "").apply(split_count)
    df["email_count"] = df.get("emails", "").apply(split_count)
    df["has_phone_flag"] = (df["phone_count"] > 0).astype(int)
    df["has_email_flag"] = (df["email_count"] > 0).astype(int)
    df["contact_traceability_score"] = df["has_phone_flag"] + df["has_email_flag"]

    df["geo_mobility_score"] = df["address_count"] + df["actor_country_count"]

    # Source features
    df["dataset_lower"] = df["source_dataset_name"].fillna("").str.lower()
    df["is_interpol_flag"] = df["dataset_lower"].str.contains("interpol").astype(int)
    df["is_wanted_flag"] = df["dataset_lower"].str.contains("wanted").astype(int)
    df["is_terrorism_flag"] = df["dataset_lower"].str.contains("terror").astype(int)
    df["is_sanctions_flag"] = df["dataset_lower"].str.contains("sanction").astype(int)

    df["program_count"] = df["source_program_ids"].apply(split_count)
    df["has_program_flag"] = (df["program_count"] > 0).astype(int)
    df["interpol_red_notice_flag"] = (
        df["source_program_ids"].fillna("").str.contains("INTERPOL", case=False)
    ).astype(int)

    df["source_count"] = df["source_dataset_name"].apply(split_count)
    df["multi_source_flag"] = (df["source_count"] > 1).astype(int)

    df["source_risk_score"] = (
        df["is_interpol_flag"] * 3
        + df["is_wanted_flag"] * 2
        + df["is_terrorism_flag"] * 3
        + df["interpol_red_notice_flag"] * 2
    )

    # Temporal features
    df["actor_observed_days"] = (df["last_seen_date"] - df["first_seen_date"]).dt.days
    df["long_observed_actor_flag"] = (df["actor_observed_days"] >= 365).astype(int)

    latest_change_date = df["last_change_date"].max()
    df["days_since_last_change"] = (latest_change_date - df["last_change_date"]).dt.days
    df["recently_changed_actor_flag"] = (df["days_since_last_change"] <= 90).astype(int)

    # Quality/text features
    df["data_completeness_score"] = (
        df["has_birth_date_flag"] + df["has_address_flag"] + df["has_identifier_flag"]
    )

    df["crime_text_length"] = df["crime_description_enhanced"].fillna("").apply(len)
    df["crime_text_word_count"] = df["crime_description_enhanced"].fillna("").apply(
        lambda x: len(str(x).split())
    )

    # Risk model
    df["identity_score"] = df["identity_complexity_score"].clip(0, 5)
    df["geo_score"] = df["geo_mobility_score"].clip(0, 5)
    df["temporal_score"] = df["long_observed_actor_flag"] + df["recently_changed_actor_flag"]

    df["actor_risk_score_v3"] = (
        df["serious_crime_flag_v3"] * 4
        + df["has_crime_text_flag"] * 2
        + df["source_risk_score"]
        + df["cross_border_risk_flag"]
        + df["identity_score"] * 0.5
        + df["geo_score"] * 0.5
        + df["temporal_score"]
    )

    df["actor_risk_level_v3"] = df["actor_risk_score_v3"].apply(final_risk_level)

    # Explainability
    df["risk_driver_crime_flag"] = df["serious_crime_flag_v3"]
    df["risk_driver_source_flag"] = (df["source_risk_score"] > 0).astype(int)
    df["risk_driver_geo_flag"] = df["cross_border_risk_flag"]
    df["risk_driver_identity_flag"] = (df["identity_complexity_score"] > 0).astype(int)
    df["risk_driver_temporal_flag"] = df["long_observed_actor_flag"]

    df["risk_explanation"] = df.apply(build_risk_explanation, axis=1)

    # Expert features
    df["normalized_name"] = (
        df["offender_name"]
        .fillna("")
        .str.lower()
        .str.replace(r"[^a-z0-9 ]", "", regex=True)
        .str.strip()
    )

    name_counts = df["normalized_name"].value_counts()
    df["potential_duplicate_count"] = df["normalized_name"].map(name_counts)
    df["is_potential_duplicate_flag"] = (df["potential_duplicate_count"] > 1).astype(int)

    df["terrorism_flag"] = (
        df["crime_description_enhanced"].fillna("").str.contains("terror", case=False)
    ).astype(int)

    df["financial_crime_flag"] = (
        df["crime_description_enhanced"].fillna("").str.contains("fraud|money", case=False)
    ).astype(int)

    df["recent_high_risk_flag"] = (
        (df["actor_risk_level_v3"] == "high")
        & (df["recently_changed_actor_flag"] == 1)
    ).astype(int)

    df["data_confidence_score"] = (
        df["source_count"] + df["identifier_count"] + df["program_count"]
    )

    df["investigator_priority_score"] = (
        df["actor_risk_score_v3"] * 2
        + df["recently_changed_actor_flag"] * 2
        + df["interpol_red_notice_flag"] * 3
    )

    df["investigator_priority_level_refined"] = df.apply(refined_priority, axis=1)

    return df.reset_index(drop=True)
