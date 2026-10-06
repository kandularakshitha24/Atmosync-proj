# AtmoSync: Micro-Climate Arbitrage Analytics

## Supply Chain Intelligence for Perishable Agricultural Shipments

AtmoSync is a supply-chain intelligence and analytics project designed to monitor environmental conditions inside agricultural shipment containers and identify potential spoilage risks.

The system combines simulated IoT telemetry, Apache Kafka, data processing, spoilage-risk analytics, machine learning, Snowflake, and an interactive Streamlit dashboard to provide a centralized view of container health and risk-aware market decisions.

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
* Predicts environmental spoilage-risk levels using a Random Forest machine learning model.
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
Random Forest ML Risk Prediction
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

## 6. Machine Learning Risk Prediction

AtmoSync includes a prototype machine learning component for predicting environmental spoilage-risk levels for monitored shipments.

### 6.1 Machine Learning Model

The project uses a **Random Forest Classifier** to predict three environmental risk categories:

```text
LOW
MEDIUM
HIGH
```

### 6.2 Input Features

The model uses the following container telemetry features:

* Temperature
* Humidity
* Vibration

### 6.3 ML Workflow

```text
Container Telemetry
        ↓
Feature Selection
        ↓
Temperature + Humidity + Vibration
        ↓
Random Forest Classifier
        ↓
Predicted Risk Level
        ↓
LOW / MEDIUM / HIGH
```

### 6.4 Model Training

The model is trained using the processed telemetry dataset:

```text
data/processed/telemetry_with_spoilage_score.csv
```

The training pipeline includes:

* Feature selection
* Label encoding
* Train-test split
* Random Forest model training
* Model evaluation
* Model serialization

The trained model is stored in:

```text
ml/models/spoilage_risk_model.pkl
```

The corresponding label encoder is stored in:

```text
ml/models/risk_label_encoder.pkl
```

### 6.5 Prototype Evaluation

The current prototype was trained using a small simulated telemetry dataset.

The model achieved **100% accuracy on the prototype test split**.

This result should not be interpreted as production-level model performance because:

* The dataset is small.
* The telemetry is simulated.
* The risk labels were generated using project-defined environmental rules.

Therefore, the current ML model demonstrates the complete machine learning pipeline from feature preparation and model training to prediction and dashboard integration rather than production-grade spoilage prediction.

### 6.6 Dashboard Integration

The trained Random Forest model is integrated into the Streamlit dashboard.

The **AI Risk Prediction** section displays the predicted risk distribution across monitored telemetry readings.

Example dashboard categories:

```text
AI HIGH RISK
AI MEDIUM RISK
AI LOW RISK
```

The ML prediction is presented separately from the rule-based Spoilage Score used by the current analytics pipeline.

### 6.7 ML Prediction Example

A sample telemetry input containing:

```text
Temperature : 34.0°C
Humidity    : 82.0%
Vibration   : 0.30
```

is processed by the trained model and produces:

```text
Predicted Spoilage Risk: HIGH
```

### 6.8 Future ML Improvements

Future versions can improve the machine learning component by using:

* Larger real-world telemetry datasets
* Historical spoilage outcomes
* Commodity-specific environmental thresholds
* Transit duration
* Weather conditions
* Logistics conditions
* Market and route information
* Remaining Shelf Life prediction
* Model monitoring and retraining

---

## 7. Snowflake Data Warehouse

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

## 8. Market & Spoilage Arbitrage

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

## 9. Arbitrage Calculation

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

## 10. Streamlit Dashboard

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
* AI risk prediction
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

## 11. Technology Stack

| Technology   | Purpose                                           |
| ------------ | ------------------------------------------------- |
| Python       | Data processing and application development       |
| Pandas       | Data manipulation and analysis                    |
| NumPy        | Numerical operations                              |
| Scikit-learn | Machine learning and Random Forest classification |
| Joblib       | ML model serialization and loading                |
| Apache Kafka | Telemetry streaming                               |
| Snowflake    | Cloud data warehouse                              |
| Streamlit    | Interactive dashboard                             |
| Plotly       | Data visualization                                |
| Git          | Version control                                   |
| GitHub       | Source-code repository                            |

---

## 12. Project Structure

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
│   ├── models/
│   │   ├── spoilage_risk_model.pkl
│   │   └── risk_label_encoder.pkl
│   ├── train_model.py
│   └── predict_risk.py
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

## 13. Data Analytics Workflow

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
Machine Learning Risk Prediction
      ↓
Market Analysis
      ↓
Dashboard Visualization
```

---

## 14. Running the Project

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

### Step 6: Train the Machine Learning Model

Run:

```powershell
python ml\train_model.py
```

The training script:

* Loads the processed telemetry dataset.
* Selects temperature, humidity, and vibration features.
* Encodes the risk labels.
* Splits the dataset into training and testing sets.
* Trains the Random Forest classifier.
* Evaluates the model.
* Saves the trained model and label encoder.

---

### Step 7: Test ML Prediction

Run:

```powershell
python ml\predict_risk.py
```

This loads the trained model and predicts the environmental risk level for a sample telemetry input.

---

### Step 8: Run the Dashboard

```powershell
streamlit run dashboard\app.py
```

The Streamlit dashboard will open in the browser.

---

## 15. Key Project Outputs

The project produces analytical datasets including:

```text
container_telemetry.csv

telemetry_with_exposure.csv

telemetry_with_spoilage_score.csv

container_risk_summary.csv

kafka_processed_telemetry.csv

market_opportunities.csv
```

The machine learning component produces:

```text
spoilage_risk_model.pkl

risk_label_encoder.pkl
```

These datasets and model artifacts support the different stages of the AtmoSync analytics pipeline.

---

## 16. Current Prototype Scope

AtmoSync is currently implemented as a prototype using simulated IoT telemetry and scenario-based market information.

The prototype demonstrates the complete analytical workflow from telemetry generation to risk assessment, machine learning risk prediction, and decision support.

The current system does not claim to measure actual physical commodity spoilage or provide live market prices.

The machine learning component is a prototype baseline trained on a small simulated dataset and should not be interpreted as production-grade spoilage prediction.

---

## 17. Future Scope

Future versions of AtmoSync could include:

* Real IoT sensor integration.
* Continuous Kafka streaming.
* Real-time Snowflake ingestion.
* Live weather APIs.
* Live commodity market prices.
* GPS-based route intelligence.
* Larger real-world ML training datasets.
* Historical spoilage outcome integration.
* Remaining Shelf Life prediction.
* Automated route optimization.
* Real-time alert notifications.
* Model monitoring and automated retraining.
* Cloud deployment.
* Role-based supply-chain dashboards.
* Integration with logistics and warehouse management systems.

---

## 18. Project Objective

The primary objective of AtmoSync is to transform container-level environmental telemetry into actionable supply-chain intelligence.

Instead of only asking:

> "Where is the shipment?"

AtmoSync aims to answer:

> "Is the shipment at risk, what is causing the risk, and would another market or route provide a better outcome?"

---

## 19. Conclusion

AtmoSync demonstrates how streaming telemetry, data analytics, machine learning, cloud data warehousing, and interactive visualization can be combined to create a risk-aware supply-chain intelligence platform for perishable agricultural commodities.

The project connects environmental monitoring with economic decision support through the concepts of **Spoilage Score** and **Spoilage Arbitrage**.

The Random Forest machine learning component extends the system by providing prototype environmental risk predictions using temperature, humidity, and vibration telemetry.

The resulting control tower provides a unified view of shipment conditions, container-level risk, AI-assisted risk prediction, analytical insights, and potential market decisions.
