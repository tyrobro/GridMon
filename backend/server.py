from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import joblib
import pandas as pd
import os
from datetime import datetime, timezone

app = FastAPI()

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "b0MhbTatD-FdDY9jtiP2dUgdEeW1WfgNflbnN2V8TQT-cKdubGCK0K1u1HxZV3la_MV2W3md-TQb8PRlWR3IoQ=="
INFLUX_ORG = "GridMon"
INFLUX_BUCKET = "grid_metrics"


try:
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("Database connected to InfluxDB")
except Exception as e:
    print(f"Database Error: {e}")

MODEL_PATH = "model.pkl"
model = None
if os.path.exists(MODEL_PATH):
    print("AI Engine: Loading model...")
    model = joblib.load(MODEL_PATH)
    print("AI Engine: Online")
else:
    print("AI Engine: Model not found.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LogRequest(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float


@app.post("/log")
def receive_log(log_data: LogRequest):

    is_anomaly = False
    if model:
        features = pd.DataFrame(
            [[log_data.cpu_usage, log_data.memory_usage]],
            columns=["cpu_usage", "memory_usage"],
        )
        prediction = model.predict(features)[0]

        if prediction == -1:
            is_anomaly = True
            print(
                f"NOMALY DETECTED! CPU: {log_data.cpu_usage}% | RAM: {log_data.memory_usage}%"
            )
        else:
            print(f"Normal: {log_data.cpu_usage}%")

    point = (
        Point("system_metrics")
        .tag("host", "my_primary_pc")
        .field("cpu", log_data.cpu_usage)
        .field("memory", log_data.memory_usage)
        .field("disk", log_data.disk_usage)
        .field("anomaly_detected", 1 if is_anomaly else 0)
        .time(datetime.now(timezone.utc))
    )
    try:
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"Logged to InfluxDB: {log_data.cpu_usage}")
    except Exception as e:
        print(f"Write Error: {e}")

    return {"stats": "Logged", "anomaly": is_anomaly}
