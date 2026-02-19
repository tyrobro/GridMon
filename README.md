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

## 📊 Performance Specs (Verified v2.2)

| Metric | Measurement | Status |
|:-------|:------------|:-------|
| **Throughput** | 10+ messages/second (Steady state) | ✅ Optimal |
| **Latency (p95)** | < 30ms (TCP Connection Pooling) | ✅ Real-time |
| **Detection Rate** | 100% on simulated 95% CPU spikes | ✅ Validated |

---

## 🚀 Key Engineering Upgrades

**Security Hardening:** All database credentials abstracted to environment variables (`.env`).

**Fault Tolerance:** Graceful error handling and active logging (`server_errors.log`) prevent API crashes during InfluxDB downtimes.

**Network Optimization:** Implemented `requests.Session()` in the agent layer to eliminate TCP handshake overhead, reducing baseline latency by 80%.

**Progress Tracking:** Active latency hunting documented in `progress.md`.

---

## 🛠️ Setup & Execution

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

### 3. Configuration

Create a `.env` file in the project root with your InfluxDB credentials:

```bash
INFLUX_TOKEN=your_influxdb_token_here
INFLUX_ORG=GridMon
INFLUX_BUCKET=grid_metrics
INFLUX_URL=http://localhost:8086
```

### 4. Running the System

**Step 1: Start InfluxDB**  
Ensure the InfluxDB server is running on `localhost:8086`.

**Step 2: Start the Backend**
```bash
uvicorn backend.server:app --reload
```

The backend will start on `http://localhost:8000` with:
- Automatic credential loading from `.env`
- Error logging to `server_errors.log`
- Graceful degradation on database failures

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
├── .env.example             # Template for environment variables
├── server_errors.log        # Error tracking and debugging
├── progress.md              # Development and optimization log
├── requirements.txt
└── README.md
```

**Key Directories:**
- `/agent` - Fleet simulator with TCP connection pooling
- `/backend` - FastAPI server with error handling and logging
- `/grafana` - Flux queries for Throughput, Latency, and Anomaly Tracking

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent | Python, psutil, requests.Session | Optimized metrics collection |
| Backend | FastAPI, Uvicorn | REST API with error handling |
| Database | InfluxDB v2 | Time-series data storage |
| AI Engine | Scikit-Learn | Isolation Forest anomaly detection |
| Visualization | Grafana | Professional dashboards and monitoring |
| Security | python-dotenv | Environment-based credential management |

---

## 🎯 Key Features

**Real-Time Anomaly Detection**  
Machine learning model flags statistical outliers (stress tests, crypto-mining, hardware failures) through multi-dimensional analysis with <30ms latency.

**Production-Grade Reliability**  
Error handling prevents cascading failures. When InfluxDB is unavailable, the system logs errors and continues operating rather than crashing.

**Network Optimization**  
TCP connection pooling with `requests.Session()` reduces per-request overhead by 80%, enabling sub-30ms p95 latency.

**Security Best Practices**  
All credentials stored in environment variables with `.env.example` template for secure deployment across environments.

**Distributed Architecture**  
Decoupled components allow monitoring of remote machines across networks. Agents, backend, and database can run on separate hosts.

**Time-Series Optimized**  
InfluxDB handles high-velocity writes and provides automatic data retention policies with proper tagging for efficient querying.

---

## 📈 How It Works

### Data Collection
Agents use Python's `psutil` library to gather CPU usage, memory consumption, and disk I/O metrics. These metrics are packaged as JSON and sent to the backend via HTTP POST requests using persistent TCP connections.

### 3D Anomaly Detection
When the backend receives telemetry data, it passes the metrics through a pre-trained Isolation Forest model. The model analyzes the 3-dimensional feature space (CPU, Memory, Disk) to identify anomalies that wouldn't be caught by single-metric thresholds.

**Example:** A system with moderate CPU (60%) and moderate memory (55%) might seem normal, but when combined with very low disk activity (5%), it could indicate a hung process or deadlock. The Isolation Forest detects these multi-dimensional outliers.

### Error Handling & Logging
All InfluxDB operations are wrapped in try-except blocks. Database failures are logged to `server_errors.log` with timestamps and error details, allowing the system to continue operating and alerting operators to connectivity issues.

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
Moving from `SYNCHRONOUS` to `BATCH` writes in InfluxDB to further reduce latency and increase throughput.

**Predictive Maintenance**  
Implementing an LSTM-based model to predict failures before they occur based on historical patterns.

**Containerization**  
Full Docker Compose setup for one-click deployment across development, staging, and production environments.

**Enhanced Authentication**  
JWT-based authentication and role-based access control (RBAC) for multi-tenant deployments.

**Auto-Scaling**  
Dynamic agent discovery and automatic load balancing for enterprise deployments.

---

## 🔒 Security Notes

- Never commit `.env` files to version control
- Rotate InfluxDB tokens regularly
- Use TLS/SSL for production deployments
- Review `server_errors.log` for security events

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
- Review `progress.md` for development history
- Check `server_errors.log` for debugging
- Consult `/grafana` directory for dashboard examples

---

## 🏆 Project Background

GridMon demonstrates the integration of machine learning models into production-grade distributed systems. It showcases:

- Real-time data ingestion and processing
- Unsupervised anomaly detection in multi-dimensional space
- Production reliability patterns (error handling, logging, graceful degradation)
- Network optimization techniques (TCP connection pooling)
- Security best practices (environment-based credential management)
- Time-series database optimization
- Professional monitoring and visualization
- Concurrent system testing and validation

Built as part of the "Build an AI Center" educational track, GridMon bridges the gap between academic machine learning and production system engineering.