from kafka import KafkaConsumer
import json
import csv
import os


KAFKA_SERVER = "localhost:9092"
TOPIC = "atmosync-telemetry"

TEMPERATURE_THRESHOLD = 30
HUMIDITY_THRESHOLD = 75

OUTPUT_FILE = "data/processed/kafka_processed_telemetry.csv"


# Create output directory if it does not exist
os.makedirs("data/processed", exist_ok=True)


# Create CSV file and header if it does not exist
if not os.path.exists(OUTPUT_FILE):
	with open(OUTPUT_FILE, "w", newline="") as file:
		writer = csv.writer(file)

		writer.writerow([
			"timestamp",
			"container_id",
			"commodity",
			"origin",
			"destination",
			"temperature",
			"humidity",
			"vibration",
			"temperature_risk",
			"humidity_risk",
			"risk_status"
		])


consumer = KafkaConsumer(
	TOPIC,
	bootstrap_servers=KAFKA_SERVER,
	auto_offset_reset="earliest",
	enable_auto_commit=True,
	group_id="atmosync-risk-consumer-v1",
	value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)


print("AtmoSync Kafka Consumer Started")
print("-" * 60)


for message in consumer:

	data = message.value

	temperature = data["temperature"]
	humidity = data["humidity"]

	temperature_risk = temperature > TEMPERATURE_THRESHOLD
	humidity_risk = humidity > HUMIDITY_THRESHOLD

	if temperature_risk or humidity_risk:
		risk_status = "RISK"
	else:
		risk_status = "NORMAL"


	with open(OUTPUT_FILE, "a", newline="") as file:

		writer = csv.writer(file)

		writer.writerow([
			data["timestamp"],
			data["container_id"],
			data["commodity"],
			data["origin"],
			data["destination"],
			temperature,
			humidity,
			data["vibration"],
			temperature_risk,
			humidity_risk,
			risk_status
		])


	print(
		f"Container: {data['container_id']} | "
		f"Commodity: {data['commodity']} | "
		f"Temperature: {temperature}°C | "
		f"Humidity: {humidity}% | "
		f"Status: {risk_status}"
	)
