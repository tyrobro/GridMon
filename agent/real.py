import time
import psutil
import requests
import socket

SERVER_URL = "https://gridmon-api.onrender.com/log"

HOSTNAME = socket.gethostname()

print(f"Starting GridMon Physical Agent on node: {HOSTNAME}...")

session = requests.Session()

while True:
    try:
        payload = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "host_name": HOSTNAME,
            "latency": 0.0,
        }

        response = session.post(SERVER_URL, json=payload, timeout=5)

        if response.status_code == 200:
            print(
                f"[{HOSTNAME}] Sent REAL telemetry -> CPU: {payload['cpu_usage']}% | RAM: {payload['memory_usage']}%"
            )
        else:
            print(f"[{HOSTNAME}] API Error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Network error (API might be sleeping): {e}")

    time.sleep(5)
