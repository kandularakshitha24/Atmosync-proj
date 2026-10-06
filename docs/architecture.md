 # AtmoSync Architecture

## Micro-Climate Arbitrage Analytics

AtmoSync is a supply-chain intelligence system designed to identify environmental risk in agricultural shipments and support risk-aware market and routing decisions.

## Data Flow

IoT Simulator  
↓  
Kafka Telemetry Stream  
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
Container Intelligence + Analytics + Market & Arbitrage  
↓  
Operational Decision

## Major Components

### 1. IoT Simulator

The IoT simulator generates container telemetry including:

- Temperature
- Humidity
- Vibration
- Container ID
- Commodity
- Origin
- Destination
- Timestamp

### 2. Apache Kafka

Kafka provides the telemetry streaming layer.

The project uses the topic:

`atmosync-telemetry`

### 3. Kafka Consumer

The consumer receives telemetry from Kafka and stores the processed stream as structured data for downstream analysis.

### 4. Risk Analysis

Environmental conditions are evaluated against project-defined risk thresholds.

Temperature above 30°C or humidity above 75% is treated as an environmental risk condition.

### 5. Spoilage Score

The project uses a risk indicator based on environmental conditions:

- 0 = Low
- 40 = Medium
- 80 = High

The score represents estimated environmental risk exposure. It is not a measured percentage of actual physical spoilage.

### 6. Snowflake

Snowflake is used as the cloud data warehouse for storing container telemetry and creating analytical views.

### 7. Streamlit Dashboard

The Streamlit dashboard provides:

- Executive Overview
- Container Intelligence
- Analytics
- Live Telemetry Status
- Market & Spoilage Arbitrage

### 8. Market & Spoilage Arbitrage

The arbitrage module compares the current destination with alternative markets.

The model considers:

- Market price
- Quantity
- Logistics cost
- Current spoilage risk

The result is used to estimate potential arbitrage benefit and provide an operational recommendation.

## Final Decision Flow

Environmental Risk  
→ Spoilage Score  
→ Risk Assessment  
→ Market Comparison  
→ Arbitrage Benefit  
→ Operational Recommendation
