import json
import time
from kafka import KafkaProducer
import random

# Simulated transaction types
transaction_types = ["purchase", "withdrawal", "transfer"]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_transaction():
    return {
        "transaction_id": random.randint(100000, 999999),
        "user_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10, 1000), 2),
        "type": random.choice(transaction_types),
        "location": random.choice(["New York", "California", "Texas", "India", "Germany"]),
        "timestamp": time.time()
    }

while True:
    transaction = generate_transaction()
    print("Sending: ", transaction)
    producer.send("bank_transactions", value=transaction)
    time.sleep(1)
