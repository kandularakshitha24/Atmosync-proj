# AtmoSync Architecture

## Micro-Climate Arbitrage Analytics

AtmoSync is a supply-chain intelligence system designed to identify
environmental risk in agricultural shipments and support
risk-aware market and routing decisions.

The system combines simulated IoT telemetry, Apache Kafka,
data processing, machine learning, Snowflake, and a Streamlit
control tower.

---

## System Architecture

```text
IoT Simulator
      ↓
Apache Kafka
      ↓
Kafka Consumer
      ↓
Data Processing
      ↓
Environmental Risk Analysis
      ↓
Spoilage Score
      ↓
Random Forest ML Risk Prediction
      ↓
Snowflake Data Warehouse
      ↓
Streamlit Control Tower
      ↓
Container Intelligence
      ↓
Analytics
      ↓
Market & Spoilage Arbitrage
      ↓
Operational Decision