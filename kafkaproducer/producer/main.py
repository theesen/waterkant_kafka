from confluent_kafka import Producer
import json
from time import sleep
import logging


TOPIC = "waterkant"

print("Starting Kafka Producer")
kafka = Producer({"bootstrap.servers": "kafka:29092"})


def deliveryCallback(err, msg):
    if err is not None:
        print("Something went horribly wrong: {}".format(err))
    else:
        print("Topic: {msg} | Partition: [{prt}] | Key: [{key}]".format(msg=msg.topic(), prt=msg.partition(), key=msg.key()))


i = 0
while True:
    i += 1
    # Check previously send message
    kafka.poll(0)
    data = {"name": "Amazing", "workshop": "kafka", "value": i}
    if i % 2 == 0:
        key = "water"
    elif i % 3 == 0:
        key = "kant"
    else:
        key = "festival"
    payload = json.dumps(data)
    kafka.produce(TOPIC, payload, key, callback=deliveryCallback)
    sleep(1)

# Clean up reamining delivery
kafka.flush()
