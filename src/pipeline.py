# src/pipeline.py

from tqdm.auto import tqdm

from src.schema import standardize_schema
from src.cleaning import basic_cleaning_pipeline
from src.multilingual import multilingual_pipeline
from src.geo import validate_coordinates
from src.temporal import add_temporal_features
from src.behavior import add_behavior_features
from src.context import add_context_features
from src.quality import add_quality_features
from src.graph import add_graph_intelligence_features
from src.explainability import add_explainability_features


def run_crimex_pipeline(df, pipeline_config):
    """
    Run the full CRIMEX enrichment pipeline with progress tracking.
    """

    df = df.copy()

    steps = [
        "Schema standardization",
        "Basic cleaning",
        "Multilingual ontology",
        "Geo validation",
        "Temporal features",
        "Behavioral intelligence",
        "Contextual enrichment",
        "Quality validation",
        "Graph intelligence",
        "Explainability",
    ]

    progress = tqdm(
        total=len(steps),
        desc="CRIMEX pipeline",
        unit="step"
    )

    progress.set_description("Schema standardization")
    df = standardize_schema(df)
    progress.update(1)

    progress.set_description("Basic cleaning")
    df = basic_cleaning_pipeline(df)
    progress.update(1)

    progress.set_description("Multilingual ontology")
    if pipeline_config.get("enable_translation_module", True):
        df = multilingual_pipeline(df)
    progress.update(1)

    progress.set_description("Geo validation")
    df = validate_coordinates(df)
    progress.update(1)

    progress.set_description("Temporal features")
    df = add_temporal_features(df)
    progress.update(1)

    progress.set_description("Behavioral intelligence")
    df = add_behavior_features(df)
    progress.update(1)

    progress.set_description("Contextual enrichment")
    df = add_context_features(df)
    progress.update(1)

    progress.set_description("Quality validation")
    if pipeline_config.get("enable_quality_validation", True):
        df = add_quality_features(df)
    progress.update(1)

    progress.set_description("Graph intelligence")
    if pipeline_config.get("enable_graph_features", True):
        df = add_graph_intelligence_features(df)
    progress.update(1)

    progress.set_description("Explainability")
    df = add_explainability_features(df)
    progress.update(1)

    progress.close()

    print("CRIMEX pipeline completed.")
    print("Final shape:", df.shape)

    return df