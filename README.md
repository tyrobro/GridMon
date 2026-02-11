# 🛡️ GridMon: Enterprise Distributed System Monitor

**GridMon** is a real-time, AI-powered observability platform designed to monitor distributed infrastructure. It ingests high-frequency telemetry (CPU, RAM, Disk) from multiple servers, detects anomalies using an Isolation Forest (Machine Learning), and visualizes the health of the fleet.

---

## 🚀 Architecture

1. **Agent Layer:** Python-based collectors (`psutil`) running on edge nodes.
2. **Ingestion Layer:** FastAPI backend that validates and tags incoming streams.
3. **Intelligence Layer:** Scikit-Learn Isolation Forest (v2.0) detecting 3D anomalies in real-time.
4. **Storage Layer:** InfluxDB v2 (Time-Series Database) for high-speed persistence.
5. **Visualization:** Grafana (Coming Soon).

---

## 🛠️ Setup & Installation

### 1. Prerequisites

- Python 3.9+
- InfluxDB v2.x (Running on `localhost:8086`)

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

---

## 🏃 Running the System

### Step 1: Start the Backend (The Brain)

```bash
uvicorn backend.server:app --reload
```

The backend will start on `http://localhost:8000` and handle:
- Data ingestion from agents
- Real-time anomaly detection
- Data persistence to InfluxDB

### Step 2: Start the Agent (Single Node Mode)

```bash
python agent/monitor.py
```

This starts a single agent that monitors the local machine and sends telemetry to the backend every few seconds.

### Step 3: Start the Fleet Simulator (Load Testing)

```bash
python agent/fleet_simulator.py
```

Simulates 10 concurrent servers sending data to test system performance under load.

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
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent | Python, psutil | Lightweight metrics collection |
| Backend | FastAPI, Uvicorn | REST API for ingestion and AI scoring |
| Database | InfluxDB v2 | Time-series data storage |
| AI Engine | Scikit-Learn | Isolation Forest anomaly detection |
| Visualization | Grafana (planned) | Enterprise-grade dashboards |

---

## 🎯 Key Features

**Real-Time Anomaly Detection**  
Machine learning model flags statistical outliers (stress tests, crypto-mining, hardware failures) the instant they occur.

**Distributed Architecture**  
Decoupled components allow monitoring of remote machines across networks. Agents, backend, and database can run on separate hosts.

**Time-Series Optimized**  
InfluxDB handles high-velocity writes and provides automatic data retention policies, eliminating the storage growth problem of v1.0.

**Production-Ready Stack**  
Migration from SQLite to InfluxDB enables concurrent writes from multiple agents without database locking.

---

## 📊 How It Works

### Data Collection
Agents use Python's `psutil` library to gather CPU usage, memory consumption, and disk I/O metrics. These metrics are packaged as JSON and sent to the backend via HTTP POST requests.

### Anomaly Detection
When the backend receives telemetry data, it passes the metrics through a pre-trained Isolation Forest model. The model assigns an anomaly score based on how different the current metrics are from learned normal behavior. Scores above the threshold trigger anomaly flags.

### Storage and Analysis
All telemetry data—including timestamps, metrics, and anomaly flags—is stored in InfluxDB for historical analysis, trend detection, and future visualization in Grafana.

---

## 🚦 System Requirements

- **CPU:** 2+ cores recommended for backend
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 10GB for InfluxDB data retention
- **Network:** Low-latency connection between agents and backend

---

## 🔮 Roadmap

**v2.0 (Current)**
- ✅ InfluxDB integration for time-series storage
- ✅ Fleet simulator for load testing
- ✅ Improved Isolation Forest model
- 🚧 Grafana dashboard integration

**v3.0 (Planned)**
- Asynchronous processing with Redis/Celery
- Multi-tenancy with authentication
- Custom alerting rules and webhooks
- Distributed tracing integration

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
- Consult the inline code documentation
- Review the architecture diagram above

---

## 🏆 Educational Purpose

GridMon was created for the "Build an AI Center" educational track. It demonstrates:

- Integrating machine learning models into production-like systems
- Designing distributed architectures with multiple communicating components
- Building full-stack applications with modern web technologies
- Understanding the trade-offs between rapid prototyping and production-ready systems
