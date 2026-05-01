# src/schema.py

# Minimum fields accepted by the CRIMEX pipeline.
# The pipeline can enrich sparse records, but every record needs an ID and offense text.
MIN_INPUT_COLUMNS = [
    "case_id",
    "crime_description",
]


# Incident-level fields.
# These describe the criminal event itself.
INCIDENT_INPUT_COLUMNS = [
    "date_reported",
    "date_occured",
    "time_occured",
    "datetime_occured",
    "latitude",
    "longitude",
    "country_code",
    "city_desc",
    "state_desc",
    "premise_code",
    "premise_description",
    "weapon_code",
    "weapon_description",
    "modus_operandi",
]


# Victim-level fields.
# Some open crime datasets provide victim information instead of offender information.
VICTIM_INPUT_COLUMNS = [
    "victim_age",
    "victim_sex",
    "victim_ethnicity",
    "victim_nationality_code",
]


# Actor/offender-level fields.
# These may come from court records, watchlists, sanctions, wanted lists, or trusted OSINT.
ACTOR_INPUT_COLUMNS = [
    "offender_id",
    "offender_name",
    "offender_aliases",
    "offender_age",
    "offender_birth_date",
    "offender_gender_code",
    "offender_nationality_code",
    "offender_country_of_residence_code",
    "offender_address",
    "offender_identifier",
    "offender_watchlist_flag",
    "offender_sanction_flag",
    "offender_group_affiliation",
    "prior_offense_count",
    "repeat_offender_flag",
]


# Source provenance fields.
# These are critical for reliability, reproducibility, and later merging.
SOURCE_METADATA_COLUMNS = [
    "source_system_code",
    "source_record_url",
    "source_language_code",
    "source_country_code",
    "source_collection_method_code",
    "source_reliability_score",
    "record_validation_status",
    "record_ingestion_timestamp",
    "enrichment_pipeline_version",
]


# All optional input columns.
OPTIONAL_INPUT_COLUMNS = (
    INCIDENT_INPUT_COLUMNS
    + VICTIM_INPUT_COLUMNS
    + ACTOR_INPUT_COLUMNS
    + SOURCE_METADATA_COLUMNS
)


def ensure_required_columns(df):
    """
    Validate that minimum required CRIMEX input columns exist.
    """
    missing_columns = [
        col for col in MIN_INPUT_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def add_missing_optional_columns(df):
    """
    Add missing optional columns as None.
    This allows sparse internet-collected records to pass through the pipeline safely.
    """
    df = df.copy()

    for col in OPTIONAL_INPUT_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df


def standardize_schema(df):
    """
    Apply the CRIMEX schema contract.
    """
    df = ensure_required_columns(df)
    df = add_missing_optional_columns(df)

    return df