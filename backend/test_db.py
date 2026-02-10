from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# --- PASTE YOUR CONFIG HERE ---
url = "http://localhost:8086"
token = "PASTE_YOUR_TOKEN_HERE"
org = "GridMon_Corp"
bucket = "grid_metrics"

print("1. Connecting...")
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

print("2. Writing test data...")
try:
    p = {
        "measurement": "test",
        "fields": {"val": 1.0},
        "time": datetime.datetime.utcnow(),
    }
    write_api.write(bucket=bucket, org=org, record=p)
    print("✅ SUCCESS! InfluxDB is working.")
except Exception as e:
    print(f"❌ FAILED: {e}")
