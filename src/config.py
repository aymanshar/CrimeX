# src/config.py

from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
FINAL_DIR = DATA_DIR / "final"


# Dataset version
DATASET_VERSION = "v1_checkpoint"


# Pipeline toggles
PIPELINE_CONFIG = {
    "enable_geo_enrichment": False,
    "geo_backend_code": "online",

    "enable_poi_enrichment": False,

    "enable_translation_module": True,
    "translation_backend_code": "rule_based_ontology",

    "enable_weather_enrichment": False,
    "weather_backend_code": "prototype_seasonal_proxy",

    "enable_graph_features": True,
    "enable_actor_enrichment": True,
    "enable_quality_validation": True,
    "enable_incremental_merge": True,

    "fail_on_missing_required_fields": False,
}


# Output paths
OUTPUT_PATHS = {
    "final_parquet": FINAL_DIR / f"crimex_{DATASET_VERSION}.parquet",
    "final_csv": FINAL_DIR / f"crimex_{DATASET_VERSION}.csv",
    "schema_json": FINAL_DIR / f"crimex_schema_{DATASET_VERSION}.json",
}