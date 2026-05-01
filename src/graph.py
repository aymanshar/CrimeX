# src/graph.py

import pandas as pd


def add_graph_keys(df):
    df = df.copy()

    df["incident_node_key"] = (
        "incident|" +
        df["case_id"].astype(str)
    )

    df["location_node_key"] = (
        "location|"
        + df["latitude_final"].round(5).astype(str)
        + "|"
        + df["longitude_final"].round(5).astype(str)
    )

    df["behavior_signature_node_key"] = (
        "behavior_signature|"
        + df["behavior_signature_key"].astype(str)
    )

    df["crime_type_node_key"] = (
        "crime_type|"
        + df["crime_ontology_code"].astype(str)
    )

    return df


def derive_behavior_centrality_risk(connectivity_degree):
    if connectivity_degree >= 5000:
        return 3, "high"

    if connectivity_degree >= 500:
        return 2, "medium"

    return 1, "low"


def derive_location_connectivity_code(x):
    if x >= 5:
        return "high"

    if x >= 2:
        return "medium"

    return "low"


def derive_cooffending_proxy(
    behavior_connectivity,
    mo_complexity,
    behavioral_threat
):
    score = 0

    if behavior_connectivity >= 500:
        score += 1

    if mo_complexity == "complex":
        score += 2

    if behavioral_threat == "high":
        score += 2

    if score <= 1:
        return score, "low"

    if score <= 3:
        return score, "medium"

    return score, "high"


def derive_network_exposure_risk(
    cooffending_score,
    behavior_centrality_score,
    location_connectivity_degree
):
    score = (
        cooffending_score
        + behavior_centrality_score
    )

    if location_connectivity_degree >= 5:
        score += 1

    if score <= 2:
        return score, "low"

    if score <= 4:
        return score, "medium"

    return score, "high"


def add_graph_intelligence_features(df):

    df = df.copy()

    df = add_graph_keys(df)

    # ---------------------------------
    # behavior signature connectivity
    # ---------------------------------

    behavior_counts = (
        df["behavior_signature_key"]
        .value_counts()
    )

    df[
        "behavior_signature_connectivity_degree"
    ] = df[
        "behavior_signature_key"
    ].map(
        behavior_counts
    )

    df[
        "behavior_signature_connectivity_code"
    ] = df[
        "behavior_signature_connectivity_degree"
    ].apply(
        lambda x:
        "high"
        if x >= 1000
        else (
            "medium"
            if x >= 200
            else "low"
        )
    )

    # ---------------------------------
    # behavior centrality risk
    # ---------------------------------

    df[
        [
            "behavior_centrality_risk_score",
            "behavior_centrality_risk_code"
        ]
    ] = df[
        "behavior_signature_connectivity_degree"
    ].apply(
        lambda x:
        pd.Series(
            derive_behavior_centrality_risk(x)
        )
    )

    # ---------------------------------
    # location connectivity
    # ---------------------------------

    location_counts = (
        df["location_node_key"]
        .value_counts()
    )

    df[
        "location_connectivity_degree"
    ] = df[
        "location_node_key"
    ].map(
        location_counts
    )

    df[
        "location_connectivity_code"
    ] = df[
        "location_connectivity_degree"
    ].apply(
        derive_location_connectivity_code
    )

    # ---------------------------------
    # cooffending risk proxy
    # ---------------------------------

    df[
        [
            "cooffending_risk_score",
            "cooffending_risk_code"
        ]
    ] = df.apply(
        lambda row:
        pd.Series(
            derive_cooffending_proxy(
                row[
                    "behavior_signature_connectivity_degree"
                ],
                row[
                    "mo_complexity_code"
                ],
                row[
                    "behavioral_threat_code"
                ]
            )
        ),
        axis=1
    )

    # ---------------------------------
    # network exposure
    # ---------------------------------

    df[
        [
            "network_exposure_risk_score",
            "network_exposure_risk_code"
        ]
    ] = df.apply(
        lambda row:
        pd.Series(
            derive_network_exposure_risk(
                row[
                    "cooffending_risk_score"
                ],
                row[
                    "behavior_centrality_risk_score"
                ],
                row[
                    "location_connectivity_degree"
                ]
            )
        ),
        axis=1
    )

    return df