import os
import time
import json
import pandas as pd
from redis_config import get_redis_connection
from message_utils import deserialize_message, serialize_message, create_message
from pathlib import Path

NODE_ID = os.getenv("NODE_ID", "worker")

# Ensure a directory exists for output
output_dir = Path("/data/worker_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

def process_sensor_batch(data):
    df = pd.DataFrame(data)

    # Group by device_id
    grouped = df.groupby("device_id")

    results = []
    for device, group in grouped:
        stats = {
            "device_id": device,
            "mean_temperature": group["temperature"].mean(),
            "std_temperature": group["temperature"].std(),
            "min_temperature": group["temperature"].min(),
            "max_temperature": group["temperature"].max(),
            "mean_pressure": group["pressure"].mean(),
            "std_pressure": group["pressure"].std(),
            "min_pressure": group["pressure"].min(),
            "max_pressure": group["pressure"].max(),
            "mean_voltage": group["voltage"].mean(),
            "std_voltage": group["voltage"].std(),
            "min_voltage": group["voltage"].min(),
            "max_voltage": group["voltage"].max(),
            "mean_current": group["current"].mean(),
            "std_current": group["current"].std(),
            "min_current": group["current"].min(),
            "max_current": group["current"].max(),
            "num_readings": len(group),
        }
        results.append(stats)

    # Save locally
    out_file = output_dir / f"{NODE_ID}_results.csv"
    pd.DataFrame(results).to_csv(out_file, mode="a", index=False, header=not out_file.exists())

    return results

def worker_loop():
    redis_conn = get_redis_connection()
    print(f"{NODE_ID}: Worker started and waiting for sensor data...")

    while True:
        task = redis_conn.blpop("task_queue", timeout=5)
        if task:
            _, message_str = task
            msg = deserialize_message(message_str)
            print(f"{NODE_ID}: Received batch from {msg['sender']}")
            result = process_sensor_batch(msg["payload"])

            # Push to result queue (optional for dashboard)
            result_msg = create_message(NODE_ID, result, message_type="result")
            redis_conn.rpush("result_queue", serialize_message(result_msg))

            print(f"{NODE_ID}: Processed batch and stored locally.")
        else:
            print(f"{NODE_ID}: No tasks. Retrying...")
            time.sleep(2)

if __name__ == "__main__":
    worker_loop()
