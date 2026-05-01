# src/multilingual.py

import re
import pandas as pd


def detect_crime_language(crime_description):
    """
    Detect the language of the crime description.
    """
    if pd.isna(crime_description):
        return "unknown"

    text = str(crime_description)

    # Arabic script detection
    if re.search(r"[\u0600-\u06FF]", text):
        return "ar"

    return "en"


def normalize_crime_description(
    crime_description,
    language_code
):
    """
    Normalize multilingual crime descriptions into canonical English terms.
    """
    if pd.isna(crime_description):
        return None

    text = str(crime_description).lower().strip()

    arabic_mapping = {
        "سرقة": "theft",
        "احتيال": "fraud",
        "اعتداء": "assault",
        "قتل": "homicide",
        "تزوير": "forgery",
        "مخدرات": "narcotics",
        "سلاح": "weapon",
        "مركبة": "vehicle",
        "طفل": "child",
    }

    if language_code == "ar":
        normalized_terms = []

        for arabic_word, english_term in arabic_mapping.items():
            if arabic_word in text:
                normalized_terms.append(english_term)

        if normalized_terms:
            return " ".join(normalized_terms)

    return text


def map_crime_ontology(canonical_description):
    """
    Map canonical crime description into CRIMEX ontology.
    """
    if pd.isna(canonical_description):
        return "unknown", "unknown crime ontology"

    text = str(canonical_description).lower()

    if "identity" in text or "fraud" in text or "forgery" in text:
        return "fraud_identity", "fraud or identity crime"

    if "assault" in text or "battery" in text or "weapon" in text or "homicide" in text:
        return "violent", "violent crime"

    if "theft" in text or "burglary" in text or "vehicle" in text or "robbery" in text:
        return "property", "property crime"

    if "child" in text or "chld" in text:
        return "child_related", "child related crime"

    if "narcotics" in text or "drug" in text:
        return "narcotics", "narcotics crime"

    return "other", "other crime"


def multilingual_pipeline(df):
    """
    Apply language detection, normalization, and ontology mapping.
    """
    df = df.copy()

    df["crime_description_language_code"] = df["crime_description_raw"].apply(
        detect_crime_language
    )

    df["crime_description_canonical_en"] = df.apply(
        lambda row: normalize_crime_description(
            row["crime_description_raw"],
            row["crime_description_language_code"]
        ),
        axis=1
    )

    df[
        [
            "crime_ontology_code",
            "crime_ontology_desc"
        ]
    ] = df["crime_description_canonical_en"].apply(
        lambda x: pd.Series(
            map_crime_ontology(x)
        )
    )

    return df