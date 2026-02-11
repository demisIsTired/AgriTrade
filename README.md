# AgriTrade Data Engine

Cloud-ready ETL pipeline correlating Brazilian weather data with agricultural commodity futures prices to generate clean datasets for 7-day price forecasting models.

---

# 📌 Project Overview

**Project Name:** Weather-to-Price ETL Pipeline  
**Author:** Yann Demuyt  

The AgriTrade Data Engine is an automated data pipeline designed to extract, validate, transform, and load live weather and commodity futures data into a structured PostgreSQL database.

The system produces high-quality, validated datasets used for machine learning models to forecast short-term (7-day) agricultural commodity price trends.

---

# 🎯 Objective

Develop a resilient, observable, and production-ready ETL pipeline that:

- Correlates Brazilian weather data with Soybean and Coffee futures
- Ensures strict data validation and quality enforcement
- Provides clean datasets for ML forecasting models
- Is fully containerized and CI/CD integrated

---

# 💡 Core Value Proposition

- **Data Observability** – Monitoring data freshness, volume, and schema integrity  
- **Code Quality** – Strict Python type hints, linting, and 90%+ test coverage  
- **Resilience** – Automated failure detection and circuit breakers to prevent corrupted data  

---

# ⚙️ Functional Requirements

## 1️⃣ Extraction (High Priority)

- Retrieve commodity data via `yfinance` (Soybeans, Coffee)
- Retrieve Brazilian weather data via OpenWeatherMap API

## 2️⃣ Validation (High Priority)

- Schema enforcement using **Pandera**
- Strict data type validation
- Range and sanity checks

## 3️⃣ Transformation (High Priority)

- Merge datasets on date index
- Feature engineering for ML models
- Outlier detection and handling

## 4️⃣ Loading (High Priority)

- Upsert cleaned data into Dockerized PostgreSQL
- Maintain relational schema integrity

## 5️⃣ Forecasting (Medium Priority)

- 7-day price movement prediction
- Models: **XGBoost / Prophet**
- Prediction endpoint (future milestone)

---

# 📊 Data Quality Rules

The pipeline enforces strict quality gates:

### 🕒 Freshness
- Pipeline must complete by **07:00 BRT daily**
- Alert if data is older than 24 hours

### 📦 Completeness
- Fail execution if precipitation or price columns contain NULL values

### 📉 Accuracy
- Rainfall must be ≥ 0
- Fail if commodity price drops > 50% in one day
- Outlier detection logic applied during transformation

---

# 🏗 Architecture

## Layered Data Design

1. **Ingestion Layer**
   - Python scripts
   - `yfinance`
   - `requests`

2. **Processing Layer**
   - Pandas
   - Pandera
   - Feature engineering

3. **Storage Layer**
   - PostgreSQL (Dockerized)
   - Structured relational schema

4. **Orchestration Layer**
   - GitHub Actions (CI scheduling)
   - Cron (optional local scheduling)

---

# 🛠 Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.12+ |
| Validation | Pandera, Pydantic |
| Database | PostgreSQL |
| Containerization | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Logging | Loguru |
| ML | XGBoost / Prophet |
| Testing | Pytest |

---

# 🧪 Quality Assurance Strategy

## Automated Testing Pyramid

### Unit Tests (Pytest)
- Transformation logic
- Feature engineering
- API mocking

### Integration Tests
- PostgreSQL insert validation
- Container communication

### Data Validation Tests
- Pandera schema enforcement
- Fail-fast behavior on schema shifts

---

## Code Quality Enforcement

- **Ruff** for linting & formatting
- **Pre-commit hooks**
- Target **>90% test coverage**
- Strict Python type hints

---

# 🚀 Deployment & DevOps

## Containerized Architecture

- ETL service container
- PostgreSQL container
- Docker Compose orchestration
- Persistent volumes for database durability

## CI/CD Pipeline

1. Push → Run lint + unit tests  
2. Merge → Build Docker image  
3. Deploy → GitHub Actions workflow  

---

# 🗺 Roadmap

## M1 – Core Pipeline
- Functional ETL script
- Database schema design

## M2 – Data Validation
- Pandera schema enforcement
- Automated error logging

## M3 – Containerization
- Docker Compose setup
- Volume persistence
- Environment variable management

## M4 – CI/CD & QA
- Automated test suite
- Ruff integration
- GitHub Actions pipeline

## M5 – Analytics & ML
- Feature engineering improvements
- 7-day forecasting model
- Prediction API endpoint
- Dashboard integration (future enhancement)

---

# 📈 Future Improvements

- Real-time streaming ingestion
- Advanced anomaly detection
- Dashboard visualization layer
- Cloud deployment (AWS/GCP)
- Model retraining automation

---

# 📄 License

No license (yet)

---

# 📬 Contact

**Yann Demuyt**  
Epitech  
Project: AgriTrade Data Engine
