
import argparse
import sys
from pathlib import Path

import pandas as pd


# Add project root to import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.actor_pipeline import run_actor_pipeline


def load_input_file(input_path):
    """
    Load CSV or parquet input file.
    """
    input_path = Path(input_path)

    if input_path.suffix.lower() == ".csv":
        return pd.read_csv(
            input_path,
            dtype=str,
            low_memory=False
        )

    if input_path.suffix.lower() in [".parquet", ".pq"]:
        return pd.read_parquet(input_path)

    raise ValueError(
        f"Unsupported input format: {input_path.suffix}"
    )


def save_output_file(df, output_path):
    """
    Save output as CSV or parquet.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if output_path.suffix.lower() == ".csv":
        df.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )
        return

    if output_path.suffix.lower() in [".parquet", ".pq"]:
        df.to_parquet(
            output_path,
            index=False
        )
        return

    raise ValueError(
        f"Unsupported output format: {output_path.suffix}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Run CRIMEX Actor Intelligence pipeline."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to OpenSanctions CSV or parquet file."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to save enriched actor dataset."
    )

    args = parser.parse_args()

    print("Loading input file...")
    df_input = load_input_file(args.input)

    df_output = run_actor_pipeline(df_input)

    print("Saving output...")
    save_output_file(
        df_output,
        args.output
    )

    print("Done.")
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
