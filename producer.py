import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8"),
)

events = [
    {"user_id": "u1", "event_type": "click", "page": "/home"},
    {"user_id": "u2", "event_type": "view", "page": "/pricing"},
    {"user_id": "u1", "event_type": "purchase", "page": "/checkout"},
]

while True:
    for e in events:
        producer.send(
            "user-events",
            key=e["user_id"],   # key decides partition
            value=e
        )
        print("Produced:", e)
        time.sleep(1)
