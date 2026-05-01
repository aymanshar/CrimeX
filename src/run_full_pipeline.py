# scripts/run_full_pipeline.py

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


# Add project root to import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import PIPELINE_CONFIG, OUTPUT_PATHS, FINAL_DIR
from src.pipeline import run_crimex_pipeline


def load_input_file(input_path):
    """
    Load CSV or parquet input file.
    """
    input_path = Path(input_path)

    if input_path.suffix.lower() == ".csv":
        return pd.read_csv(input_path)

    if input_path.suffix.lower() in [".parquet", ".pq"]:
        return pd.read_parquet(input_path)

    raise ValueError(
        f"Unsupported input format: {input_path.suffix}"
    )


def save_outputs(df):
    """
    Save final CRIMEX outputs.
    """
    FINAL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_PATHS["final_parquet"],
        index=False
    )

    df.to_csv(
        OUTPUT_PATHS["final_csv"],
        index=False
    )

    schema = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": list(df.columns),
    }

    with open(
        OUTPUT_PATHS["schema_json"],
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            schema,
            f,
            ensure_ascii=False,
            indent=2
        )


def main():
    parser = argparse.ArgumentParser(
        description="Run CRIMEX full enrichment pipeline."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV or parquet file."
    )

    args = parser.parse_args()

    print("Loading input file...")
    df_input = load_input_file(args.input)

    print("Input shape:", df_input.shape)

    print("Running CRIMEX pipeline...")
    df_output = run_crimex_pipeline(
        df_input,
        PIPELINE_CONFIG
    )

    print("Output shape:", df_output.shape)

    print("Saving outputs...")
    save_outputs(df_output)

    print("Done.")
    print("Saved parquet:", OUTPUT_PATHS["final_parquet"])
    print("Saved csv    :", OUTPUT_PATHS["final_csv"])
    print("Saved schema :", OUTPUT_PATHS["schema_json"])


if __name__ == "__main__":
    main()