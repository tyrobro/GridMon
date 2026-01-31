from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


class Log(BaseModel):
    cpu_usage: float
    memory_usage: float
    timestamp: str
    status: str


def init_db():
    try:
        conn = sqlite3.connect("gridmon.db")
        print("Database created")
    except:
        print("Database not created.")

    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT, node_id VARCHAR(50) DEFAULT 'Laptop1', cpu_usage FLOAT, memory_usage FLOAT, timestamp VARCHAR(50), status VARCHAR(50));"
    )
    conn.commit()
    conn.close()


init_db()

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Headquarters is on, LESGOOOOOOO!!"}


@app.post("/log")
def data_logger(data: Log):
    insert_query = "INSERT INTO logs(cpu_usage, memory_usage, timestamp, status) VALUES (?, ?, ?, ?)"
    conn = sqlite3.connect("gridmon.db")
    cursor = conn.cursor()
    cursor.execute(
        insert_query, (data.cpu_usage, data.memory_usage, data.timestamp, data.status)
    )
    conn.commit()
    conn.close()
    return {"message": "Data Received"}
