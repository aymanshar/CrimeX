# src/geo.py

import pandas as pd


def validate_coordinates(df):
    df = df.copy()

    if "latitude" not in df.columns or "longitude" not in df.columns:
        df["latitude_final"] = None
        df["longitude_final"] = None
        df["is_valid_coordinate"] = 0
        return df

    df["latitude_original"] = df["latitude"]
    df["longitude_original"] = df["longitude"]

    valid_mask = (
        df["latitude"].notna()
        & df["longitude"].notna()
        & (df["latitude"] != 0)
        & (df["longitude"] != 0)
        & df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    )

    df["is_valid_coordinate"] = valid_mask.astype(int)
    df["latitude_final"] = df["latitude"].where(valid_mask)
    df["longitude_final"] = df["longitude"].where(valid_mask)

    return df