import random
import time
import os
from datetime import datetime, timedelta

import pandas as pd


SHIPMENTS = {
	"C001": {"commodity": "Tomato", "origin": "Hyderabad", "destination": "Mumbai"},
	"C002": {"commodity": "Mango", "origin": "Bengaluru", "destination": "Chennai"},
	"C003": {"commodity": "Apple", "origin": "Pune", "destination": "Hyderabad"},
	"C004": {"commodity": "Banana", "origin": "Chennai", "destination": "Mumbai"},
	"C005": {"commodity": "Potato", "origin": "Hyderabad", "destination": "Pune"},
}

RISK_SCENARIOS = {
	"C001": "normal",
	"C002": "temperature_risk",
	"C003": "normal",
	"C004": "humidity_risk",
	"C005": "combined_risk",
}


def generate_sensor_data(container_id, reading_number, timestamp):
	shipment = SHIPMENTS[container_id]
	scenario = RISK_SCENARIOS[container_id]

	temperature = random.uniform(22, 28)
	humidity = random.uniform(55, 70)
	vibration = random.uniform(0.05, 0.30)

	if scenario == "temperature_risk":
		temperature += reading_number * 0.10
	elif scenario == "humidity_risk":
		humidity += reading_number * 0.20
	elif scenario == "combined_risk":
		temperature += reading_number * 0.08
		humidity += reading_number * 0.15

	temperature = min(temperature, 35)
	humidity = min(humidity, 90)

	return {
		"timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
		"container_id": container_id,
		"commodity": shipment["commodity"],
		"origin": shipment["origin"],
		"destination": shipment["destination"],
		"temperature": round(temperature, 2),
		"humidity": round(humidity, 2),
		"vibration": round(vibration, 2),
	}


if __name__ == "__main__":
	print("AtmoSync IoT Simulator Started")
	print("-" * 60)

	records = []
	start_time = datetime.now()

	for reading_number in range(100):
		container_id = random.choice(list(SHIPMENTS.keys()))
		timestamp = start_time + timedelta(seconds=reading_number)
		data = generate_sensor_data(container_id, reading_number, timestamp)
		records.append(data)
		print(data)
		time.sleep(0.05)

	df = pd.DataFrame(records)
	os.makedirs("data/raw", exist_ok=True)
	output_file = "data/raw/container_telemetry.csv"
	df.to_csv(output_file, index=False)

	print("-" * 60)
	print("Telemetry generation completed.")
	print(f"Total records generated: {len(df)}")
	print(f"Data saved to: {output_file}")
