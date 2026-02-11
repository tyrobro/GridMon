# 🛡️ GridMon: Enterprise Distributed System Monitor

GridMon is a real-time, AI-powered observability platform designed to monitor distributed infrastructure. It ingests high-frequency telemetry from multiple servers, utilizes a 3D Isolation Forest for anomaly detection, and visualizes system health through a professional Grafana dashboard.

---

## 🚀 Architecture

1. **Agent Layer:** Python-based collectors running on edge nodes.
2. **Ingestion Layer:** FastAPI backend that validates and tags incoming streams.
3. **Intelligence Layer:** Scikit-Learn Isolation Forest (v2.0) detecting 3D anomalies in real-time.
4. **Storage Layer:** InfluxDB v2 (Time-Series Database) for high-speed persistence.
5. **Visualization:** Grafana-based Mission Control Center.

---

## 📊 Performance Benchmarks (Verified v2.1)

Based on a 10-node simulated fleet, the following metrics were observed under steady-state operation:

- **Throughput:** ~7–10 messages/second (Total System Ingestion)
- **End-to-End Latency:** 100ms – 200ms (Synchronous Mode)
- **AI Reliability:** 100% detection rate for simulated 95% CPU spikes within a 1% contamination threshold

---

## 🛠️ Setup & Installation

### 1. Prerequisites

- Python 3.9+
- InfluxDB v2.x (Running on `localhost:8086`)
- Grafana (Running on `localhost:3000`)

### 2. Installation

```bash
git clone https://github.com/tyrobro/GridMon.git
cd GridMon
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Running the System

**Step 1: Start InfluxDB**  
Ensure the InfluxDB server is running and your token is updated in `backend/server.py`.

**Step 2: Start the Backend (The Brain)**
```bash
uvicorn backend.server:app --reload
```

**Step 3: Start the Fleet Simulator**  
Simulates 10 concurrent servers with randomized performance "personalities" and anomaly events.
```bash
python agent/fleet_simulator.py
```

---

## 🧠 AI Engine v2.0

Unlike standard threshold alerts, GridMon uses an unsupervised **Isolation Forest** model trained on a 3-dimensional feature vector:

- CPU Usage (%)
- Memory Usage (%)
- Disk Usage (%)

This allows the system to identify complex anomalies where a single metric might look "normal" but the combination of the three indicates system distress (e.g., high disk I/O with low CPU).

---

## 📂 Project Structure

```
GridMon/
├── agent/
│   ├── monitor.py           # Single-node telemetry agent
│   └── fleet_simulator.py   # Multi-node load testing simulator
├── backend/
│   ├── server.py            # FastAPI ingestion & AI engine
│   ├── ai_engine.py         # Model training script
│   ├── training_data.csv    # Historical training data
│   └── model.pkl            # Serialized Isolation Forest model
├── grafana/
│   └── queries/             # Flux queries for dashboards
├── requirements.txt
└── README.md
```

**Key Directories:**
- `/agent` - Contains the fleet simulator and latency-tracking logic
- `/backend` - FastAPI server, InfluxDB integration, and `model.pkl`
- `/grafana` - Flux queries for Throughput, Latency, and Anomaly Tracking

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent | Python, psutil | Lightweight metrics collection |
| Backend | FastAPI, Uvicorn | REST API for ingestion and AI scoring |
| Database | InfluxDB v2 | Time-series data storage |
| AI Engine | Scikit-Learn | Isolation Forest anomaly detection |
| Visualization | Grafana | Professional dashboards and monitoring |

---

## 🎯 Key Features

**Real-Time Anomaly Detection**  
Machine learning model flags statistical outliers (stress tests, crypto-mining, hardware failures) the instant they occur through multi-dimensional analysis.

**Distributed Architecture**  
Decoupled components allow monitoring of remote machines across networks. Agents, backend, and database can run on separate hosts.

**Time-Series Optimized**  
InfluxDB handles high-velocity writes and provides automatic data retention policies, eliminating the storage growth problem.

**Production-Ready Stack**  
Migration from SQLite to InfluxDB enables concurrent writes from multiple agents without database locking.

**Fleet Simulation**  
Built-in load testing with 10 concurrent virtual servers generating realistic workload patterns and anomaly events.

---

## 📈 How It Works

### Data Collection
Agents use Python's `psutil` library to gather CPU usage, memory consumption, and disk I/O metrics. These metrics are packaged as JSON and sent to the backend via HTTP POST requests.

### 3D Anomaly Detection
When the backend receives telemetry data, it passes the metrics through a pre-trained Isolation Forest model. The model analyzes the 3-dimensional feature space (CPU, Memory, Disk) to identify anomalies that wouldn't be caught by single-metric thresholds.

**Example:** A system with moderate CPU (60%) and moderate memory (55%) might seem normal, but when combined with very low disk activity (5%), it could indicate a hung process or deadlock. The Isolation Forest detects these multi-dimensional outliers.

### Storage and Visualization
All telemetry data—including timestamps, metrics, and anomaly flags—is stored in InfluxDB with proper tagging for efficient querying. Grafana dashboards provide real-time visualization of:
- System health metrics
- Anomaly detection events
- Throughput and latency statistics
- Fleet-wide performance trends

---

## 🚦 System Requirements

- **CPU:** 2+ cores recommended for backend
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 10GB for InfluxDB data retention
- **Network:** Low-latency connection between agents and backend

---

## 🔮 Future Roadmap

**Asynchronous Ingestion**  
Moving from `SYNCHRONOUS` to `BATCH` writes in InfluxDB to reduce p95 latency to <10ms.

**Predictive Maintenance**  
Implementing an LSTM-based model to predict failures before they occur based on historical patterns.

**Containerization**  
Full Docker Compose setup for one-click deployment across development, staging, and production environments.

**Enhanced Security**  
JWT-based authentication, TLS encryption, and role-based access control (RBAC).

**Auto-Scaling**  
Dynamic agent discovery and automatic load balancing for enterprise deployments.

---

## 📝 License

MIT License. See LICENSE file for details.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome via GitHub issues and pull requests.

---

## 💬 Support

For questions or issues:

- Open an issue on GitHub
- Review the architecture documentation
- Check the `/grafana` directory for dashboard examples

---

## 🏆 Project Background

GridMon demonstrates the integration of machine learning models into production-grade distributed systems. It showcases:

- Real-time data ingestion and processing
- Unsupervised anomaly detection in multi-dimensional space
- Time-series database optimization
- Professional monitoring and visualization
- Concurrent system testing and validation

Built as part of the "Build an AI Center" educational track, GridMon bridges the gap between academic machine learning and production system engineering.
