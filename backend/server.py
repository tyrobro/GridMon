from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from data_exporter import engine, SessionLocal, Base, Log
from sqlalchemy.orm import Session
import joblib
import pandas as pd
import os

app = FastAPI()

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

Base.metadata.create_all(bind=engine)


class LogRequest(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float


@app.post("/log")
def receive_log(log_data: LogRequest):
    db: Session = SessionLocal()

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

    new_log = Log(
        cpu_usage=log_data.cpu_usage,
        memory_usage=log_data.memory_usage,
        disk_usage=log_data.disk_usage,
    )
    db.add(new_log)
    db.commit()
    db.close()

    return {"status": "Logged", "anomaly": is_anomaly}


@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(Log).order_by(Log.timestamp.desc()).limit(20).all()
    db.close()
    return logs
