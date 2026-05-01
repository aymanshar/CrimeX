# src/cleaning.py

import pandas as pd


def normalize_column_names(df):
    """
    Standardize column names.
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def standardize_crime_description(df):
    """
    Create canonical crime text field.
    """
    df = df.copy()

    df["crime_description_raw"] = (
        df["crime_description"]
        .astype(str)
        .str.strip()
    )

    df["crime_description_canonical_en"] = (
        df["crime_description_raw"]
        .str.lower()
    )

    return df


def remove_duplicate_cases(
    df,
    case_key="case_id"
):
    """
    Drop duplicate case records.
    """
    df = df.copy()

    df = df.drop_duplicates(
        subset=[case_key]
    )

    return df


def basic_cleaning_pipeline(df):
    """
    Core cleaning sequence.
    """
    df = normalize_column_names(df)

    df = standardize_crime_description(df)

    df = remove_duplicate_cases(df)

    return df