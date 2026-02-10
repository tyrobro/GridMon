import psutil
import requests
import time

SERVER_URL = "http://127.0.0.1:8000/log"

print(f"Agent active. Streaming to {SERVER_URL}")

while True:
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        payload = {"cpu_usage": cpu, "memory_usage": ram, "disk_usage": disk}

        response = requests.post(SERVER_URL, json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            status = "ANOMALY" if data.get("anomaly") else "Normal"
            print(f"[{status}] CPU: {cpu}% | RAM: {ram}%")
        else:
            print(f"Server Error ({response.status_code}): {response.text}")

        time.sleep(1)

    except requests.exceptions.ConnectionError:
        print("Server is offline. Retrying in 5s...")
        time.sleep(5)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        time.sleep(2)
