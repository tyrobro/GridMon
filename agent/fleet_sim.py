import requests
import time
import random
import multiprocessing

SERVER_URL = "http://127.0.0.1:8000/log"


def run_fake_server(server_id):
    name = f"compute-node-{server_id:02d}"
    base_cpu = random.uniform(10, 30)

    while True:
        cpu = max(0, min(100, base_cpu + random.uniform(-5, 5)))
        ram = random.uniform(40, 60)
        disk = 20.0

        if random.random() < 0.01:
            cpu = 95.0
            print(f"🔥 {name} spiked to 95%!")

        payload = {
            "cpu_usage": cpu,
            "memory_usage": ram,
            "disk_usage": disk,
            "host_name": name,
        }

        try:
            requests.post(SERVER_URL, json=payload, timeout=1)
        except:
            pass
        time.sleep(1)


if __name__ == "__main__":
    print("🛰️ Launching 10 virtual servers...")
    for i in range(10):
        multiprocessing.Process(target=run_fake_server, args=(i,)).start()
