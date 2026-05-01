# CRIMEX: Multimodal Behavioral Crime Intelligence Dataset

## Overview
CRIMEX is a next-generation crime dataset designed to advance research in crime analysis, prediction, and behavioral intelligence. Unlike traditional crime datasets that focus only on structured records, CRIMEX integrates multiple layers of information including behavioral signals, temporal patterns, geo-spatial context, environmental factors, and AI-driven insights.

The goal of CRIMEX is to provide a comprehensive, scalable, and research-ready dataset that enables advanced machine learning and deep learning applications for crime understanding.

---

## Key Features

- **Multilayer Data Architecture**
  - Observed (raw factual data)
  - External (weather, events, socioeconomic context)
  - Derived (time, spatial, statistical features)
  - Internal (pattern mining and clustering)
  - LLM-enriched (behavioral and psychological insights)

- **Behavioral Intelligence**
  - Motive inference
  - Emotional and psychological profiling
  - Planning and risk assessment

- **Spatio-Temporal Modeling**
  - Crime location intelligence
  - Time-based patterns and seasonality
  - Event-driven crime context

- **Graph-Ready Design**
  - Supports graph-based modeling using Neo4j
  - Captures relationships between offenders, crimes, and locations

- **Reproducible Research Workflow**
  - Versioned data pipeline
  - Config-driven processing
  - Deterministic transformations where possible
  - Notebook outputs aligned with script-based execution

- **Clean Notebook Design**
  - Step-by-step research notebooks
  - Clear markdown explanations
  - Re-runnable from top to bottom
  - Figures, tables, and intermediate outputs saved for later reuse

- **Scalable Pipeline**
  - Designed for large-scale data processing (50K–500K+ cases)

---

## Dataset Structure

The dataset is organized into the following modules:

1. Core Crime Data  
2. Offender Profile  
3. Victim Profile  
4. Crime Methodology  
5. Temporal Features  
6. Geo-Spatial Features  
7. Event & Environmental Context  
8. Country & Socioeconomic Context  
9. Risk & Watchlist Signals  
10. Derived Behavioral Features  
11. Internal Pattern Features  
12. LLM-Enriched Intelligence  
13. Event Sequence (Advanced)

---

## Data Sources

CRIMEX integrates multiple data sources:

### Core Data
- OpenICPSR
- FBI Crime Data Explorer
- UK Police Data
- Kaggle crime datasets

### News & Events
- GDELT Project
- Google News
- Media Cloud
- EventRegistry

### Geo & Environment
- OpenStreetMap / Overpass API
- OpenWeather API
- Calendar APIs (holidays, seasonal data)

### Socioeconomic Data
- World Bank
- Numbeo
- OECD

### Risk & Compliance
- OpenSanctions
- OFAC Sanctions List

### Legal Data
- CourtListener
- Harvard Law Case Corpus

---

## Pipeline Architecture

The CRIMEX pipeline consists of the following stages:

1. Data Collection  
2. Data Cleaning and Normalization  
3. Feature Engineering (Derived Features)  
4. External Enrichment (APIs and contextual data)  
5. Risk Enrichment (sanctions and watchlists)  
6. LLM Enrichment (behavioral and psychological analysis)  
7. Internal Pattern Mining (clustering and trends)  
8. Validation Layer (quality checks and filtering)  
9. Dataset Assembly (tabular and graph formats)  
10. Publishing (HuggingFace, Kaggle)

---

## Reproducibility

Reproducibility is a core principle of CRIMEX.

The project is designed so that the dataset construction process can be repeated, audited, and extended by other researchers.

### Reproducibility Design Principles

- All major pipeline stages are implemented as standalone scripts
- Config files control paths, API options, thresholds, and runtime parameters
- Intermediate outputs are saved between stages
- Random seeds are fixed for deterministic steps where applicable
- LLM enrichment outputs are versioned and traceable
- Dataset versions are documented with clear metadata and changelogs
- Notebooks are used for research presentation and analysis, not as the only execution path

### Reproducible Execution Strategy

Each major step should support:

- command-line execution
- notebook execution
- saved artifacts for reuse without rerunning expensive stages

Example stages:

- raw data ingestion
- data normalization
- feature engineering
- external enrichment
- LLM enrichment
- validation
- final dataset export

### Recommended Reproducibility Files

- `requirements.txt` or `pyproject.toml`
- `configs/`
- `.env.example`
- `data/README.md`
- `VERSION`
- `CHANGELOG.md`

---

## Notebook Philosophy

CRIMEX notebooks are intended to be clean, structured, and publication-friendly.

### Notebook Rules

- Every notebook must run from top to bottom
- Each notebook should have a clear objective
- Markdown should explain why each step exists
- Heavy processing should live in Python scripts, not inline notebook code
- Notebook cells should call reusable functions from `src/`
- All important plots, metrics, and tables should be saved to disk
- Final outputs should be suitable for direct use in research papers

### Notebook Types

- `01_data_collection_overview.ipynb`
- `02_data_cleaning_validation.ipynb`
- `03_feature_engineering.ipynb`
- `04_external_enrichment.ipynb`
- `05_llm_enrichment_analysis.ipynb`
- `06_dataset_statistics.ipynb`
- `07_baseline_modeling.ipynb`

### Clean Notebook Structure

Each notebook should follow this structure:

1. Title and objective  
2. Imports and setup  
3. Config loading  
4. Data loading  
5. Processing steps  
6. Validation checks  
7. Visualizations  
8. Saved outputs  
9. Summary and next step  

---


## Example Features

- Age and age group  
- Crime type and methodology  
- Time bucket and seasonality  
- Geo-spatial indicators and POI proximity  
- Weather and event context  
- Country-level economic indicators  
- Risk and sanction signals  
- Behavioral and psychological attributes (LLM-derived)  
- Crime sequence modeling  

---

## Supported Machine Learning Tasks

- Crime type classification  
- Motive prediction  
- Risk scoring  
- Crime time prediction  
- Crime location prediction  
- Behavior sequence modeling  
- Case similarity retrieval  
- Graph-based crime prediction  

---

## Graph Representation

CRIMEX supports graph-based modeling:

- **Nodes**: Person, Crime, Location, Event  
- **Relationships**:
  - Person → Crime  
  - Crime → Location  
  - Crime → Victim  
  - Person → Person (associations)  

---

## Ethical Considerations

- All data is anonymized  
- No personally identifiable information (PII) is included  
- Sensitive attributes are handled with care  
- Bias and fairness considerations are documented  


## Project Structure

```text
	crimex/
	│
	├── configs/
	├── data/
	│   ├── raw/
	│   ├── interim/
	│   ├── processed/
	│   ├── enriched/
	│   └── final/
	│
	├── notebooks/
	├── outputs/
	│   ├── figures/
	│   ├── tables/
	│   ├── logs/
	│   └── reports/
	│
	├── src/
	│   ├── collection/
	│   ├── cleaning/
	│   ├── features/
	│   ├── enrichment/
	│   ├── validation/
	│   ├── graph/
	│   └── modeling/
	│
	├── tests/
	├── .env.example
	├── CHANGELOG.md
	├── LICENSE
	├── README.md
	├── requirements.txt
	└── VERSION
```

---

## Roadmap

- Phase 1: Core data collection and schema definition  
- Phase 2: External enrichment integration  
- Phase 3: LLM-based behavioral enrichment  
- Phase 4: Pattern mining and clustering  
- Phase 5: Dataset release and benchmarking  

---

## Expected Output

- Large-scale enriched dataset (50K–500K records)  
- Graph dataset for network analysis  
- Baseline and advanced ML models  
- Research paper and benchmarks  

---

## Contribution

CRIMEX is designed as an open research initiative. Contributions are welcome in:

- Data collection  
- Feature engineering  
- Model development  
- Evaluation and benchmarking  

---

## License

(To be defined based on data source compatibility)

---

## Contact

Project maintained by Ayman.

---

## Future Work

- Integration with real-time data streams  
- Advanced graph neural networks  
- Cross-country comparative analysis  
- Explainable AI for crime prediction  