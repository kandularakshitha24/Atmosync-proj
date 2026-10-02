from kafka import KafkaProducer
import json
import random
import time

from iot_simulator import SHIPMENTS, generate_sensor_data


KAFKA_SERVER = "localhost:9092"
TOPIC = "atmosync-telemetry"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


print("AtmoSync Kafka Producer Started")
print("-" * 60)


for reading_number in range(20):

    container_id = random.choice(list(SHIPMENTS.keys()))

    data = generate_sensor_data(container_id)

    producer.send(
        TOPIC,
        value=data
    )

    print("Sent:", data)

    time.sleep(0.5)


producer.flush()
producer.close()


print("-" * 60)
print("Kafka Producer completed.")