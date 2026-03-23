# GridMon: Distributed Hardware Telemetry & ML Anomaly Detection

GridMon is a distributed systems observability platform that streams real-time hardware telemetry from edge agents to a cloud-hosted API for machine learning-based anomaly detection. The system processes bare-metal metrics (CPU, RAM, Disk) through an Isolation Forest model before persisting data to a serverless time-series database.

Built with a focus on low-latency systems engineering, asynchronous data ingestion, and distributed cloud architecture.

---

## 🏗️ System Architecture

**Edge Layer (Physical Agents)**  
Lightweight Python daemons using `psutil` to collect motherboard-level metrics from remote machines. Agents utilize `requests.Session()` for TCP connection pooling to minimize network handshake overhead during high-frequency streaming.

**API Layer (Ingestion Engine)**  
Stateless FastAPI backend deployed to cloud infrastructure. Handles inbound traffic asynchronously while routing CPU-intensive ML inference and database writes to background thread pools to prevent event-loop blocking.

**Intelligence Layer (ML Engine)**  
Isolation Forest model (scikit-learn) trained on 24-hour baseline telemetry. Maps incoming payloads into 3D feature space [CPU, RAM, Disk] to detect hardware stress and anomalies in real-time.

**Storage Layer (Database)**  
InfluxDB Cloud (Serverless) handles continuous time-series data ingestion for long-term storage and visualization via Grafana.

---

## ⚡ Performance & Latency Analysis

A core engineering challenge was reducing end-to-end telemetry ingestion latency:

**Initial Baseline:** ~200ms  
Primary bottlenecks: Synchronous database writes and pandas DataFrame construction overhead during ML inference.

**Optimized Compute Latency:** <10ms  
Achieved through:
- Replacing pandas with raw NumPy arrays for ML inference
- TCP connection pooling at edge agents
- Asynchronous database writes via background thread pools

**Production Network Latency:** ~100ms  
Represents physical transit time and jitter across public internet from geographically distributed edge nodes to cloud provider.

**Total End-to-End Latency:** ~110ms (compute + network)

---

## 📊 Performance Specifications

| Metric | Measurement | Notes |
|:-------|:------------|:------|
| **Compute Latency** | <10ms | ML inference + data validation |
| **Network Latency** | ~100ms | Geographic transit over public internet |
| **Throughput** | 10+ agents concurrent | Tested with distributed fleet |
| **Detection Accuracy** | Validated on 24h baseline | Trained on real hardware data |

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Python 3.13, FastAPI, Uvicorn | Asynchronous API with thread pool executor |
| ML Engine | scikit-learn, NumPy, Joblib | Isolation Forest inference |
| Database | InfluxDB Cloud v2 | Serverless time-series storage |
| Visualization | Grafana, Flux SQL | Real-time dashboard queries |
| Edge Agents | psutil, requests.Session | Optimized metrics collection |
| Testing | pytest, GitHub Actions | Automated integration tests |
| Deployment | Render Cloud | Managed cloud hosting |

---

## 🚀 Deployment Guide

### 1. InfluxDB Cloud Configuration

1. Create account at [InfluxDB Cloud](https://cloud2.influxdata.com/)
2. Navigate to **Load Data → Buckets** and create `grid_metrics` bucket
3. Generate API token via **Load Data → API Tokens**
4. Note your cluster URL (e.g., `https://us-east-1-1.aws.cloud2.influxdata.com`) and organization name

### 2. API Server Deployment (Render)

1. Fork this repository
2. Create account at [Render.com](https://render.com/)
3. Create new **Web Service** linked to repository

**Build Configuration:**
```bash
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.server:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
```
INFLUX_URL=<Your Cluster URL>
INFLUX_TOKEN=<Your API Token>
INFLUX_ORG=<Your Organization>
INFLUX_BUCKET=grid_metrics
```

4. Deploy service and copy provided `*.onrender.com` URL

### 3. Edge Agent Configuration

Install dependencies on target machine:
```bash
pip install requests psutil
```

Update `agent/real_agent.py` with your Render API URL:
```python
SERVER_URL = "https://your-app.onrender.com"
```

Run agent daemon:
```bash
python agent/real_agent.py

# For background execution (Linux/Mac):
nohup python agent/real_agent.py &
```

---

## 📊 Dashboard Configuration

### InfluxDB Data Explorer Setup

1. Open Data Explorer in InfluxDB Cloud
2. **Filter Configuration:**
   - Uncheck any old simulated `compute-node` tags
   - Select your physical machine's hostname in the `host` column
3. **Metric Selection:**
   - Measurement: `system_metrics`
   - Fields: `cpu`, `memory`, or `latency`
4. **Visualization Fix:**
   - Change display mode from "Band" to "Graph" for independent telemetry lines

---

## 🧪 Testing

The project includes automated integration tests for API validation and database routing:

```bash
python -m pytest tests/ -v
```

Tests verify:
- API payload validation
- Database write operations
- Error handling paths
- Anomaly detection logic

---

## 📂 Project Structure

```
GridMon/
├── agent/
│   ├── real_agent.py        # Production edge agent
│   └── fleet_simulator.py   # Load testing simulator
├── backend/
│   ├── server.py            # FastAPI async API
│   ├── ai_engine.py         # Model training script
│   └── model.pkl            # Trained Isolation Forest
├── tests/
│   └── test_api.py          # Integration tests
├── requirements.txt
└── README.md
```

---

## 🎯 Key Engineering Decisions

**Asynchronous Architecture**  
FastAPI's async capabilities handle concurrent connections while background thread pools prevent blocking on CPU-bound operations (ML inference) and I/O-bound operations (database writes).

**TCP Connection Pooling**  
Using `requests.Session()` eliminates per-request TCP handshake overhead, reducing network latency by maintaining persistent connections to the API.

**NumPy Over Pandas**  
Replacing pandas DataFrames with raw NumPy arrays for ML inference reduced compute overhead from ~200ms to <10ms due to eliminated DataFrame construction.

**Serverless Database**  
InfluxDB Cloud eliminates infrastructure management while providing native time-series optimizations and automatic retention policies.

**Thread Pool Execution**  
Database writes execute in background threads to prevent blocking FastAPI's event loop, maintaining low request latency even during database operations.

---

## 🔒 Security Considerations

- All credentials managed via environment variables
- No secrets committed to version control
- API tokens rotated regularly
- HTTPS enforced for all cloud communications
- Agent authentication recommended for production deployments

---

## 🔮 Future Enhancements

**Predictive Analytics**  
Implement LSTM-based time-series forecasting to predict hardware failures before they occur based on degradation patterns.

**Enhanced Authentication**  
JWT-based authentication for agent registration and multi-tenant access control.

**Batch Processing**  
Move from synchronous to batch writes in InfluxDB to further reduce latency and increase throughput.

**Auto-Scaling**  
Dynamic agent discovery and load balancing for enterprise deployments monitoring hundreds of nodes.

**Advanced Alerting**  
Webhook integration for real-time notifications on anomaly detection events.

---

## 📝 License

MIT License. See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome via GitHub issues and pull requests. Please include tests for new features.

---

## 📚 Documentation

- **InfluxDB Setup:** See deployment guide above
- **API Documentation:** Access `/docs` endpoint on deployed server for OpenAPI specification
- **Testing Guide:** See `tests/` directory for integration test examples
- **Troubleshooting:** Check deployment logs and `SERVER_URL` configuration

---

## 🏆 Technical Highlights

This project demonstrates:

- **Distributed Systems:** Multi-node edge computing with centralized cloud coordination
- **Asynchronous Programming:** Non-blocking I/O with FastAPI and background thread execution
- **Performance Engineering:** Latency optimization from 200ms to <10ms compute time
- **Machine Learning Integration:** Real-time inference pipeline with scikit-learn
- **Cloud Architecture:** Serverless database integration with managed API hosting
- **Network Optimization:** TCP connection pooling and persistent HTTP sessions
- **Production Practices:** Environment-based configuration, error handling, automated testing
- **Time-Series Data:** Efficient storage and querying patterns for telemetry streams

Built as a practical exploration of production-grade distributed systems architecture and real-time ML inference pipelines.