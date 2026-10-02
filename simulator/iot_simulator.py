import random
import time
import os
from datetime import datetime

import pandas as pd


# Fixed shipment information
SHIPMENTS = {
	"C001": {
		"commodity": "Tomato",
		"origin": "Hyderabad",
		"destination": "Mumbai"
	},
	"C002": {
		"commodity": "Mango",
		"origin": "Bengaluru",
		"destination": "Chennai"
	},
	"C003": {
		"commodity": "Apple",
		"origin": "Pune",
		"destination": "Hyderabad"
	},
	"C004": {
		"commodity": "Banana",
		"origin": "Chennai",
		"destination": "Mumbai"
	},
	"C005": {
		"commodity": "Potato",
		"origin": "Hyderabad",
		"destination": "Pune"
	}
}


def generate_sensor_data(container_id):
	shipment = SHIPMENTS[container_id]

	temperature = round(random.uniform(20, 35), 2)
	humidity = round(random.uniform(50, 90), 2)
	vibration = round(random.uniform(0.05, 0.50), 2)

	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return {
		"timestamp": timestamp,
		"container_id": container_id,
		"commodity": shipment["commodity"],
		"origin": shipment["origin"],
		"destination": shipment["destination"],
		"temperature": temperature,
		"humidity": humidity,
		"vibration": vibration
	}


if __name__ == "__main__":

	print("AtmoSync IoT Simulator Started")
	print("-" * 60)

	records = []

	for _ in range(100):

		container_id = random.choice(list(SHIPMENTS.keys()))

		data = generate_sensor_data(container_id)

		records.append(data)

		print(data)

		time.sleep(0.1)

	# Convert generated records into a DataFrame
	df = pd.DataFrame(records)

	# Create the raw data directory if it doesn't exist
	os.makedirs("data/raw", exist_ok=True)

	# Save the telemetry data
	output_file = "data/raw/container_telemetry.csv"
	df.to_csv(output_file, index=False)

	print("-" * 60)
	print("Telemetry generation completed.")
	print(f"Total records generated: {len(df)}")
	print(f"Data saved to: {output_file}")
