import psutil
import requests
import time
import datetime

SERVER_URL = "http://127.0.0.1:8000/log"

print(f"Agent creating connection to {SERVER_URL}")

while True:
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        payload = {"cpu_usage": cpu, "memory_usage": ram, "disk_usage": disk}

        response = requests.post(SERVER_URL, json=payload)
        if response.status_code != 200:
            print(f"Server Error ({response.status_code}): {response.text}")
        else:
            print(f"Server says: {response.json()}")
        print(f"Server says: {response.json()}")

        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
