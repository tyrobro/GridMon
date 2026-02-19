import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import os

print("GridMon AI Validation Suite")

MODEL_PATH = "model.pkl"
if not os.path.exists(MODEL_PATH):
    print("Error: model.pkl not found. Train the model first!")
    exit()

model = joblib.load(MODEL_PATH)

np.random.seed(7)

normal_cpu = np.random.uniform(10, 40, 950)
normal_ram = np.random.uniform(30, 60, 950)
normal_disk = np.random.uniform(10, 30, 950)
normal_labels = np.ones(950)

anomaly_cpu = np.random.uniform(85, 100, 50)
anomaly_ram = np.random.uniform(80, 100, 50)
anomaly_disk = np.random.uniform(80, 100, 50)
anomaly_labels = np.full(50, -1)

X_test = pd.DataFrame(
    {
        "cpu_usage": np.concatenate([normal_cpu, anomaly_cpu]),
        "memory_usage": np.concatenate([normal_ram, anomaly_ram]),
        "disk_usage": np.concatenate([normal_disk, anomaly_disk]),
    }
)
y_true = np.concatenate([normal_labels, anomaly_labels])

print("Testing against 1,000 data points...")
y_pred = model.predict(X_test)

print("\n--- AI Performance Metrics --- 📊")

# Confusion Matrix shows True Positives, False Positives, etc.
print("\nConfusion Matrix:")
cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
print(f"True Normal: {cm[0][0]}  | False Anomaly (Oops): {cm[0][1]}")
print(f"False Normal (Missed): {cm[1][0]} | True Anomaly: {cm[1][1]}")

print("\nClassification Report:")
print(
    classification_report(y_true, y_pred, target_names=["Anomaly (-1)", "Normal (1)"])
)
