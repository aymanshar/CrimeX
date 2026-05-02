
from src.actor import add_actor_features


def run_actor_pipeline(df):
    """
    Run CRIMEX Actor Intelligence enrichment pipeline.
    """
    df = df.copy()

    print("Running CRIMEX Actor Intelligence pipeline...")
    print("Input shape:", df.shape)

    df = add_actor_features(df)

    print("Actor pipeline completed.")
    print("Output shape:", df.shape)

    return df
