from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/logs")
def get_logs():
    conn = sqlite3.connect("gridmon.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()

    conn.close()

    data = [dict(row) for row in rows]

    return data
