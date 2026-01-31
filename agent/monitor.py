import psutil
import time
import csv
import requests
from datetime import datetime

file = "logs.csv"
with open(file, "w", newline="") as fp:
    write = csv.writer(fp)
    write.writerow(["timestamp", "cpu_usage", "memory_usage", "status"])

while True:
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    now = datetime.now()
    now_string = datetime.now().isoformat()
    status = "OK"
    data_packet = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "timestamp": now_string,
        "status": "OK",
    }
    #    with open(file, 'a', newline = '') as fp:
    #      write = csv.writer(fp)
    #      write.writerow([now_string, cpu_usage, memory_usage, status])

    try:
        response = requests.post("http://127.0.0.1:8000/log", json=data_packet)
        print(f"Server says: {response.json()}")
    except:
        print("Server is down.")
    time.sleep(1)
