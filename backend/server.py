import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import joblib
from datetime import datetime, timezone
import warnings

logging.basicConfig(
    filename="server_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
load_dotenv()

app = FastAPI()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

if not INFLUX_TOKEN:
    raise ValueError("INFLUX_TOKEN is missing from .env file!")

try:
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api(write_options=ASYNCHRONOUS)
except Exception as e:
    print(f"Database Error: {e}")

MODEL_PATH = "backend/model.pkl"
model = None
if os.path.exists(MODEL_PATH):
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
    host_name: str
    latency: float = 0.0


@app.post("/log")
def receive_log(log_data: LogRequest):

    is_anomaly = False
    if model:
        try:
            raw_features = [
                [log_data.cpu_usage, log_data.memory_usage, log_data.disk_usage]
            ]

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                prediction = model.predict(raw_features)[0]
            if prediction == -1:
                is_anomaly = True
                print(
                    f"ANOMALY DETECTED:{log_data.host_name}! CPU: {log_data.cpu_usage}% | RAM: {log_data.memory_usage}% | DISK: {log_data.disk_usage}%"
                )
        except Exception as e:
            logging.error(f"AI Inference Error: {e}")

    point = (
        Point("system_metrics")
        .tag("host", log_data.host_name)
        .field("cpu", log_data.cpu_usage)
        .field("memory", log_data.memory_usage)
        .field("disk", log_data.disk_usage)
        .field("latency", log_data.latency)
        .field("anomaly_detected", 1 if is_anomaly else 0)
        .time(datetime.now(timezone.utc))
    )
    try:
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        return {"stats": "Logged", "anomaly": is_anomaly}
    except InfluxDBError as e:
        logging.error(f"InfluxDB Write Error: {e}")
        raise HTTPException(status_code=503, detail="Database Unavailable")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
