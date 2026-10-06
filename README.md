# AtmoSync: Micro-Climate Arbitrage Analytics

## Supply Chain Intelligence for Perishable Agricultural Shipments

AtmoSync is a supply-chain intelligence and analytics project designed to monitor environmental conditions inside agricultural shipment containers and identify potential spoilage risks.

The system combines simulated IoT telemetry, Apache Kafka, data processing, spoilage-risk analytics, Snowflake, and an interactive Streamlit dashboard to provide a centralized view of container health and risk-aware market decisions.

---

## 1. Problem Statement

Traditional supply-chain analytics often rely on standard transit times and broad weather information.

However, environmental conditions can vary significantly between individual shipment containers.

For example, a container carrying mangoes may experience a temporary temperature or humidity increase during transportation. If the condition persists, the quality of the agricultural commodity may be affected.

AtmoSync addresses this problem by monitoring container-level environmental telemetry and converting these observations into actionable risk intelligence.

---

## 2. Proposed Solution

AtmoSync provides a supply-chain control tower that:

* Collects container telemetry such as temperature, humidity, and vibration.
* Processes telemetry through a Kafka streaming pipeline.
* Identifies environmental risk conditions.
* Calculates a project-defined Spoilage Score.
* Stores telemetry and analytical views in Snowflake.
* Provides container-level risk intelligence.
* Compares alternative markets for potentially risky shipments.
* Estimates potential arbitrage benefit.
* Provides operational recommendations through a Streamlit dashboard.

---

## 3. System Architecture

```text
IoT Simulator
      ↓
Apache Kafka
      ↓
Kafka Consumer
      ↓
Data Processing & Risk Analysis
      ↓
Spoilage Score
      ↓
Snowflake Data Warehouse
      ↓
Streamlit Control Tower
      ↓
┌──────────────────────────────────────┐
│ Executive Overview                   │
│ Container Intelligence               │
│ Analytics                            │
│ Market & Spoilage Arbitrage          │
└──────────────────────────────────────┘
      ↓
Operational Decision
```

---

## 4. Core Modules

### 4.1 IoT Telemetry Simulator

The project uses a Python-based simulator to generate container telemetry.

The simulated data contains:

* Timestamp
* Container ID
* Commodity
* Origin
* Destination
* Temperature
* Humidity
* Vibration

The simulator generates sample telemetry representing conditions that may occur during agricultural transportation.

---

### 4.2 Apache Kafka

Apache Kafka is used as the telemetry streaming layer.

The project uses the Kafka topic:

```text
atmosync-telemetry
```

The Kafka producer publishes container telemetry records, while the Kafka consumer receives the records for downstream processing.

---

### 4.3 Data Processing and Risk Analysis

The telemetry data is processed to identify environmental risk conditions.

Project-defined thresholds:

```text
Temperature > 30°C
OR
Humidity > 75%
```

When either condition is satisfied, the telemetry reading is considered an environmental risk condition.

---

## 5. Spoilage Score

AtmoSync uses a project-defined **Spoilage Score** as an environmental risk indicator.

| Environmental Condition       | Score |
| ----------------------------- | ----: |
| Normal conditions             |     0 |
| Temperature OR humidity risk  |    40 |
| Temperature AND humidity risk |    80 |

Risk levels:

```text
0  → LOW
40 → MEDIUM
80 → HIGH
```

### Important Interpretation

The Spoilage Score represents **estimated environmental risk exposure**.

It is **not an actual percentage of physically spoiled goods**.

For example, a score of 80 does not mean that 80% of the commodity has spoiled. It represents a high-risk environmental condition according to the project's prototype scoring model.

---

## 6. Snowflake Data Warehouse

Snowflake is used as the cloud data warehouse for storing processed container telemetry and creating analytical views.

### Database

```text
ATMOSYNC_DB
```

### Schema

```text
RAW_DATA
```

### Main Table

```text
CONTAINER_TELEMETRY
```

### Analytical Views

```text
CONTAINER_RISK_VIEW
DASHBOARD_CONTAINER_SUMMARY
```

The analytical views support container-level risk analysis and dashboard reporting.

---

## 7. Market & Spoilage Arbitrage

One of the key concepts of AtmoSync is **Spoilage Arbitrage**.

When a shipment has elevated environmental risk, the system evaluates whether an alternative market could provide a better economic outcome.

The prototype considers:

* Current market price
* Alternative market price
* Shipment quantity
* Current logistics cost
* Alternative logistics cost
* Current spoilage risk

### Decision Logic

```text
Environmental Risk
        ↓
Spoilage Score
        ↓
Risk-Adjusted Current Value
        ↓
Compare Alternative Markets
        ↓
Calculate Arbitrage Benefit
        ↓
Operational Recommendation
```

The dashboard can recommend actions such as:

```text
REROUTE RECOMMENDED
MONITOR & CONSIDER REROUTE
ALTERNATIVE MARKET AVAILABLE
CONTINUE CURRENT ROUTE
```

The market prices, quantities, and logistics values used in the current prototype are scenario-based analytical inputs and should not be interpreted as live market data.

---

## 8. Arbitrage Calculation

The prototype uses the following calculations:

```text
Current Risk-Adjusted Value
=
Current Market Value ×
(1 − Spoilage Score / 100)
```

```text
Alternative Net Value
=
Alternative Market Value −
Alternative Logistics Cost
```

```text
Arbitrage Benefit
=
Alternative Net Value −
Current Risk-Adjusted Value
```

A positive arbitrage benefit indicates that the alternative market provides a potentially better economic outcome under the prototype assumptions.

---

## 9. Streamlit Dashboard

AtmoSync provides an interactive supply-chain control tower built using Streamlit.

### Dashboard Pages

#### Executive Overview

Provides a high-level view of the shipment fleet.

Includes:

* Total containers
* High-risk containers
* Medium-risk containers
* Average spoilage score
* Risk events
* Fleet risk distribution
* Environmental exposure
* Active alerts
* Telemetry status

---

#### Container Intelligence

Provides detailed information for an individual container.

Includes:

* Container selection
* Commodity
* Origin
* Destination
* Risk level
* Spoilage Score
* Temperature trend
* Humidity trend
* Vibration trend
* Risk trend
* Telemetry readings
* Operational alerts

---

#### Analytics

Provides analytical views across the shipment fleet.

Includes:

* Container risk comparison
* Environmental conditions
* Temperature distribution
* Humidity distribution
* Risk events
* Commodity intelligence
* Route intelligence
* Container risk matrix
* Operational insights

---

#### Market & Spoilage Arbitrage

Provides risk-aware market decision support.

Includes:

* Commodity selection
* Current shipment
* Current market
* Current risk
* Alternative market
* Alternative price
* Potential arbitrage benefit
* Market comparison
* Operational recommendation

---

## 10. Technology Stack

| Technology   | Purpose                                     |
| ------------ | ------------------------------------------- |
| Python       | Data processing and application development |
| Pandas       | Data manipulation and analysis              |
| NumPy        | Numerical operations                        |
| Apache Kafka | Telemetry streaming                         |
| Snowflake    | Cloud data warehouse                        |
| Streamlit    | Interactive dashboard                       |
| Plotly       | Data visualization                          |
| Git          | Version control                             |
| GitHub       | Source-code repository                      |

---

## 11. Project Structure

```text
AtmoSync/
│
├── backend/
│   ├── kafka_consumer.py
│   └── snowflake_connection.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── architecture.md
│
├── ml/
│
├── notebooks/
│   ├── eda.py
│   ├── exposure_analysis.py
│   ├── validate_dataset.py
│   ├── spoilage_score.py
│   └── container_risk_summary.py
│
├── simulator/
│   ├── iot_simulator.py
│   └── kafka_producer.py
│
├── sql/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 12. Data Analytics Workflow

The analytical workflow used in the project is:

```text
Raw Telemetry
      ↓
Data Validation
      ↓
Exploratory Data Analysis
      ↓
Environmental Risk Detection
      ↓
Exposure Analysis
      ↓
Spoilage Score Calculation
      ↓
Container Risk Summary
      ↓
Market Analysis
      ↓
Dashboard Visualization
```

---

## 13. Running the Project

### Step 1: Activate the Virtual Environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

---

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### Step 3: Generate Telemetry

Run the IoT simulator:

```powershell
python simulator\iot_simulator.py
```

---

### Step 4: Run Kafka Producer

Start Kafka and then run:

```powershell
python simulator\kafka_producer.py
```

---

### Step 5: Run Kafka Consumer

In another terminal:

```powershell
python backend\kafka_consumer.py
```

The consumer processes telemetry from the Kafka topic and stores the processed records for downstream analysis.

---

### Step 6: Run the Dashboard

```powershell
streamlit run dashboard\app.py
```

The Streamlit dashboard will open in the browser.

---

## 14. Key Project Outputs

The project produces analytical datasets including:

```text
container_telemetry.csv
telemetry_with_exposure.csv
telemetry_with_spoilage_score.csv
container_risk_summary.csv
kafka_processed_telemetry.csv
market_opportunities.csv
```

These datasets support the different stages of the AtmoSync analytics pipeline.

---

## 15. Current Prototype Scope

AtmoSync is currently implemented as a prototype using simulated IoT telemetry and scenario-based market information.

The prototype demonstrates the complete analytical workflow from telemetry generation to risk assessment and decision support.

The current system does not claim to measure actual physical commodity spoilage or provide live market prices.

---

## 16. Future Scope

Future versions of AtmoSync could include:

* Real IoT sensor integration.
* Continuous Kafka streaming.
* Real-time Snowflake ingestion.
* Live weather APIs.
* Live commodity market prices.
* GPS-based route intelligence.
* Machine-learning-based spoilage prediction.
* Remaining Shelf Life prediction.
* Automated route optimization.
* Real-time alert notifications.
* Cloud deployment.
* Role-based supply-chain dashboards.
* Integration with logistics and warehouse management systems.

---

## 17. Project Objective

The primary objective of AtmoSync is to transform container-level environmental telemetry into actionable supply-chain intelligence.

Instead of only asking:

> "Where is the shipment?"

AtmoSync aims to answer:

> "Is the shipment at risk, what is causing the risk, and would another market or route provide a better outcome?"

---

## 18. Conclusion

AtmoSync demonstrates how streaming telemetry, data analytics, cloud data warehousing, and interactive visualization can be combined to create a risk-aware supply-chain intelligence platform for perishable agricultural commodities.

The project connects environmental monitoring with economic decision support through the concepts of **Spoilage Score** and **Spoilage Arbitrage**.

The resulting control tower provides a unified view of shipment conditions, container-level risk, analytical insights, and potential market decisions.
