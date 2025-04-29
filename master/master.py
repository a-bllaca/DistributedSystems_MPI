import random
import pandas as pd
import time
import os
from redis_config import get_redis_connection
from message_utils import create_message, serialize_message

NODE_ID = "master"
DEVICE_IDS = [f"device_{i}" for i in range(1, 21)]  # 20 devices
SENSOR_FIELDS = ["temperature", "pressure", "voltage", "current"]

def generate_sensor_data(batch_size=50):
    data = []
    for _ in range(batch_size):
        record = {
            "device_id": random.choice(DEVICE_IDS),
            "timestamp": pd.Timestamp.now().isoformat(),
            "temperature": random.uniform(20.0, 100.0),
            "pressure": random.uniform(1.0, 5.0),
            "voltage": random.uniform(110.0, 240.0),
            "current": random.uniform(0.1, 15.0),
        }
        data.append(record)
    return data

def push_tasks_loop():
    redis_conn = get_redis_connection()

    while True:
        batch = generate_sensor_data()
        msg = create_message(NODE_ID, batch, message_type="task")
        redis_conn.rpush("task_queue", serialize_message(msg))
        print(f"Master: Sent batch of {len(batch)} sensor readings.")
        time.sleep(5)  # Simulate batch every 5 seconds

if __name__ == "__main__":
    print("Master: Starting sensor data simulation")
    push_tasks_loop()
