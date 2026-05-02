# CRIMEX — Crime Intelligence Dataset Pipeline

## 📌 Overview

CRIMEX is a research-grade framework that transforms raw crime and watchlist data into **intelligence-ready datasets** using feature engineering, behavioral modeling, and explainability.

It consists of two complementary pipelines:

- **CRIMEX v1** → Crime incident intelligence (Los Angeles dataset)
- **CRIMEX v2** → Actor Intelligence (OpenSanctions)

---

The recommended entry point is the Actor Intelligence pipeline notebook.

## Reproducibility

All results in this project are fully reproducible using:

- Notebook pipelines
- Modular Python scripts (`src/`)
- Command-line execution

No hidden steps or manual preprocessing are required.

---

## Quick Start

### Option 1 — Actor Intelligence (Recommended)

Run the full pipeline:

```bash
notebooks/01_crimex_actor_intelligence_pipeline.ipynb
```

This notebook will:

1. Download OpenSanctions dataset  
2. Load and inspect raw data  
3. Apply CRIMEX actor pipeline  
4. Generate intelligence features  
5. Compute risk and priority scores  
6. Save final dataset  
7. Generate feature dictionary and metadata  

---

### Option 2 — Command Line

Run the core pipeline without the notebook:

```bash
python scripts/run_actor_pipeline.py \
  --input data/raw/opensanctions/crime_targets_simple.csv \
  --output data/final/opensanctions/crimex_actor_intelligence_core.parquet
  ```

---

## 📁 Project Structure

CrimeX/
├── data/
│ ├── raw/ # Raw downloaded datasets
│ └── final/ # Final enriched datasets
│
├── notebooks/
│ ├── crimex_la_pipeline_reproducible.ipynb
│ └── 01_crimex_actor_intelligence_pipeline.ipynb
│
├── src/
│ ├── actor.py
│ ├── actor_pipeline.py
│ ├── actor_extended.py
│ ├── pipeline.py
│ ├── cleaning.py
│ ├── temporal.py
│ ├── geo.py
│ ├── multilingual.py
│ ├── behavior.py
│ ├── context.py
│ ├── graph.py
│ ├── quality.py
│ ├── explainability.py
│ └── schema.py
│
├── scripts/
│ └── run_actor_pipeline.py
│
└── README.md
	
---


## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/CrimeX.git
cd CrimeX
```

Install dependencies:
```bash
pip install pandas requests tqdm pyarrow
```

---

# 🧱 CRIMEX v1 — Crime Intelligence (LA Dataset)

CRIMEX v1 transforms raw crime incident data into intelligence-ready features.

### Input Data

Typical raw datasets contain:

- Crime description  
- Date and time  
- Location  
- Victim information  

### Output Features

CRIMEX generates:

- Temporal patterns  
- Geo features  
- Behavioral signals  
- Contextual risk indicators  
- Graph-inspired relationships  
- Explainable outputs  

---

# 🧠 CRIMEX v2 — Actor Intelligence Pipeline

## 📌 Overview

CRIMEX Actor Intelligence builds a **person-level intelligence dataset** from public watchlists and criminal datasets.

It transforms OpenSanctions data into:

- Structured actor profiles  
- Crime-aware intelligence features  
- Risk scoring and prioritization  
- Explainable investigation signals  

---

## 📊 Data Source

This pipeline uses:

- OpenSanctions — Crime dataset  
  https://www.opensanctions.org  

⚠️ Data License: **CC BY-NC 4.0**  
Users must comply with attribution and non-commercial usage requirements.

---

## ⚙️ Pipeline Design

### 🔹 Core Pipeline (`src/actor.py`)

Production-ready features:

- Identity and aliases  
- Crime text extraction  
- Crime ontology mapping  
- Country and cross-border features  
- Source intelligence  
- Temporal features  
- Risk scoring  
- Investigator priority  

---

### 🔹 Extended Features (`src/actor_extended.py`)

Research and analyst features:

- Text richness analysis  
- Identity density  
- Geographic complexity  
- Temporal dynamics  
- Source strength  
- Manual review flags  
- Investigator segmentation  

---

## 📦 Output

The pipeline produces:

- ~170K actor records  
- 95+ core features  
- 110+ extended features  
- Feature dictionary (CSV)  
- Metadata file (JSON)  

---

## 🎯 Example Features

| Feature | Description |
|--------|------------|
| actor_risk_level_v3 | Risk classification |
| investigator_priority_level_refined | Action priority |
| risk_explanation | Human-readable explanation |
| cross_border_risk_flag | Multi-country indicator |
| identity_complexity_score | Identity density |

---

# 🔬 Feature Engineering (CRIMEX v1)

## Temporal Features
- Year, month, day, hour  
- Weekday / weekend  
- Season  

## Geo Features
- Coordinate validation  
- Cleaned latitude/longitude  
- Hemisphere information  

## Crime Ontology
- Standardized crime categories  
- Crime family and severity levels  

## Behavioral Intelligence
- Modus operandi analysis  
- Multi-step crime detection  
- Criminal sophistication score  

## Contextual Risk Features
- Opportunity signals  
- Routine activity theory features  

## Data Quality Features
- Completeness score  
- Consistency checks  

## Graph-Inspired Features
- Node identifiers  
- Connectivity proxies  

## Explainability Features
- Human-readable explanations  
- Structured explanation codes  

---

# 📊 Example Output

| Stage | Columns |
|------|--------|
| Raw dataset | ~13 |
| CRIMEX v1 output | 140+ |
| Actor Intelligence v2 | 110+ |

---

# 🎯 Use Cases

- Crime prediction models  
- Risk scoring systems  
- Behavioral analysis  
- Graph-based intelligence  
- Explainable AI (XAI)  

---

# 🚀 Future Work

## Geo / POI Enrichment
- OpenStreetMap integration  
- Nearby points of interest  
- Spatial risk features  

## Graph Intelligence
- Neo4j integration  
- Actor relationship networks  

## Entity Resolution
- Cross-dataset identity linking  

---

# 👤 Author

Ayman Sharara  
Data Scientist | AI Researcher | Crime Intelligence Systems  

---

# 🤝 Contributions

This project is open for learning and improvement.

You can:

- Fork the repository  
- Suggest improvements  
- Extend the pipeline  

---

# 📬 Feedback

Contributions and feedback are welcome.