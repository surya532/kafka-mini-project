import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "user-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="event-processors",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

for msg in consumer:
    print(
        f"Partition={msg.partition} "
        f"Offset={msg.offset} "
        f"Value={msg.value}"
    )
