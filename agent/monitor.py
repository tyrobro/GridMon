import psutil
import time
import csv
import os
from datetime import datetime

file = 'logs.csv'
with open(file, 'w', newline = '') as fp:
    write = csv.writer(fp)
    write.writerow(['timestamp', 'cpu_usage', 'memory_usage'])
    
while True:
    cpu_usage = psutil.cpu_percent(interval = 1)
    memory_usage = psutil.virtual_memory().percent
    now = datetime.now()
    now_string = datetime.now().isoformat()
    data_packet = {
        "Memory Usage" : memory_usage,
        "CPU Usage" : cpu_usage,
        "unit" : "percent",
        "time" : now_string,
        "status" : "OK"
    }
    with open(file, 'a', newline = '') as fp:
        write = csv.writer(fp)
        write.writerow([now_string, cpu_usage, memory_usage])
    time.sleep(1)