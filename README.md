# CRIMEX v1 — LA Incident Behavioral Intelligence Dataset

## 📌 Overview

CRIMEX v1 is a large-scale enriched criminal incident dataset derived from the Los Angeles Open Crime Data.

It transforms raw incident records into a **behavioral intelligence dataset** by adding multiple feature layers:
- Temporal intelligence
- Behavioral profiling
- Contextual risk signals
- Graph-inspired features
- Data quality and explainability metrics

The dataset is designed for **machine learning, crime analytics, and research applications**.

---

## 📊 Dataset Summary

- **Total records:** ~1,004,894
- **Total features:** 150+
- **Location:** Los Angeles, USA
- **Time span:** Based on source data
- **Format:** Parquet (full), CSV (sample)

---

## 🧠 Feature Categories

### 1. Core Incident Data
- Case ID, crime type, timestamps
- Victim attributes
- Weapon and premise information

### 2. Temporal Features
- Hour, day, weekday, weekend
- Seasonal indicators
- Time-based patterns

### 3. Behavioral Intelligence
- Modus operandi complexity
- Multi-step behavior indicators
- Behavioral risk scoring
- Criminal sophistication proxy

### 4. Contextual Risk Signals
- Opportunity context
- Guardianship proxy
- Routine activity theory features
- Environmental stress indicators (proxy-based)

### 5. Graph-Inspired Features
- Behavior signature keys
- Connectivity approximations
- Centrality and exposure proxies

### 6. Explainability Layer
- Risk explanation text
- Interpretable feature contributions
- Risk categorization codes

### 7. Data Quality
- Completeness score
- Consistency flags
- Enrichment confidence

---

## 🌍 Geo Information

- Latitude/Longitude included
- Missing coordinates partially recovered via geocoding
- Geo/POI enrichment planned in future versions

---

## 🚧 Limitations

- Derived from a single city (Los Angeles)
- Some features are heuristic or proxy-based
- No full POI/environment enrichment yet (planned in v2)
- Actor-level linking not included in this version

---

## 🚀 Use Cases

- Crime prediction modeling
- Risk scoring systems
- Behavioral pattern analysis
- Graph-based crime analysis
- Anomaly detection
- Explainable AI research

---

## ⚖️ Data Source & License

This dataset is derived from:

- Los Angeles Open Data Portal  
  https://data.lacity.org

Users must comply with the original data source license.

CRIMEX v1 provides **feature-engineered transformations** and does not modify original legal ownership.

---

## 🔮 Future Versions

- CRIMEX v2: Geo/POI enrichment using OpenStreetMap (local stack)
- CRIMEX v3: Multi-source integration (OpenSanctions, Interpol, etc.)
- CRIMEX v4: Global crime intelligence graph

---

## 👤 Author

Ayman Sharara  
Data Scientist | AI Researcher | Crime Intelligence Systems

---

## 📬 Feedback

Contributions and feedback are welcome.