import pandas as pd
import os


# Load telemetry dataset
input_file = "data/raw/container_telemetry.csv"

df = pd.read_csv(input_file)


# Convert timestamp from string to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])


# Sort records by container and time
df = df.sort_values(["container_id", "timestamp"]).reset_index(drop=True)


# Project-defined risk conditions
TEMPERATURE_THRESHOLD = 30
HUMIDITY_THRESHOLD = 75


# Identify whether each reading is a risk condition
df["temperature_risk"] = df["temperature"] > TEMPERATURE_THRESHOLD
df["humidity_risk"] = df["humidity"] > HUMIDITY_THRESHOLD

df["risk_condition"] = (
	df["temperature_risk"] |
	df["humidity_risk"]
)


# Calculate time difference between consecutive readings
df["time_difference_seconds"] = (
	df.groupby("container_id")["timestamp"]
	.diff()
	.dt.total_seconds()
	.fillna(0)
)


# Calculate cumulative exposure duration
df["exposure_duration_seconds"] = (
	df.groupby("container_id")["time_difference_seconds"]
	.cumsum()
)


# Keep exposure duration only while the container is in a risk condition
df["risk_exposure_seconds"] = (
	df["time_difference_seconds"]
	.where(df["risk_condition"], 0)
)


# Calculate total risk exposure for each container
container_exposure = (
	df.groupby("container_id")["risk_exposure_seconds"]
	.sum()
	.reset_index()
)


container_exposure.rename(
	columns={
		"risk_exposure_seconds": "total_risk_exposure_seconds"
	},
	inplace=True
)


# Display results
print("\n===== EXPOSURE ANALYSIS =====")

print("\nRisk thresholds:")
print(f"Temperature > {TEMPERATURE_THRESHOLD}°C")
print(f"Humidity > {HUMIDITY_THRESHOLD}%")

print("\n===== RISK RECORDS =====")
print(
	df[
		[
			"timestamp",
			"container_id",
			"temperature",
			"humidity",
			"temperature_risk",
			"humidity_risk",
			"risk_condition"
		]
	].head(20)
)


print("\n===== TOTAL RISK EXPOSURE BY CONTAINER =====")

print(container_exposure)


# Create processed data directory
os.makedirs("data/processed", exist_ok=True)


# Save processed telemetry
output_file = "data/processed/telemetry_with_exposure.csv"

df.to_csv(output_file, index=False)


print("\n===== PROCESSING COMPLETED =====")
print(f"Processed records: {len(df)}")
print(f"Saved to: {output_file}")
