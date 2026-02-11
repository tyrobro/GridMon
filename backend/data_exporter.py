import psutil
import pandas as pd
import time

print("collecting data for training purposes.")
print("keep using your computer as you would.")

data = []
try:
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        data.append([cpu, ram, disk])

except KeyboardInterrupt:
    print("Stopping early...")

df = pd.DataFrame(data, columns=["cpu_usage", "memory_usage", "disk_usage"])
df.to_csv("training_data_2.csv", index=False)
print("Data collection complete. File saved: training_data_2.csv")
