# GridMon: AI-Powered Distributed System Monitor

**Version 1.0** | Real-time infrastructure monitoring with integrated anomaly detection

GridMon is a full-stack, distributed monitoring system designed to track high-performance computing metrics in real-time. It integrates an unsupervised machine learning model (Isolation Forest) directly into the ingestion pipeline to detect and flag anomalies—such as stress tests, crypto-mining malware, or hardware failures—the instant they occur.

---

## Features

**Real-Time Telemetry**  
Captures CPU, memory, and disk usage from a lightweight Python agent running on target machines.

**AI Anomaly Detection**  
Uses an unsupervised machine learning model (Scikit-Learn Isolation Forest) to learn normal system behavior and flag statistical outliers automatically.

**Persistent Logging**  
Stores every heartbeat in a local SQLite database for historical analysis and debugging.

**Live Dashboard**  
React-based frontend providing interactive visualization of live telemetry and anomaly states.

**Distributed Architecture**  
Decoupled agent, server, and dashboard components allow monitoring of remote machines across the local network.

---

## Architecture Overview

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Agent     │ ──HTTP──▶│   Backend   │◀──HTTP──│  Dashboard  │
│  (Python)   │         │  (FastAPI)  │         │   (React)   │
│             │         │      +      │         │             │
│  psutil     │         │  AI Engine  │         │  Recharts   │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │   SQLite    │
                        │  Database   │
                        └─────────────┘
```

**Component Responsibilities:**

- **Agent**: Lightweight collector running on each monitored machine, gathering system metrics every few seconds
- **Backend**: REST API server handling data ingestion, AI inference, and database operations
- **Database**: Local file-based storage (SQLite) for all telemetry logs
- **AI Engine**: Isolation Forest model for real-time anomaly scoring
- **Dashboard**: Interactive web interface for visualizing metrics and anomaly alerts

---

## Project Structure

```
GridMon/
├── agent/
│   └── monitor.py          # Metrics collector and sender
├── backend/
│   ├── server.py           # REST API + AI integration
│   ├── ai_engine.py        # Model training script
│   ├── training_data.csv   # Historical data for training
│   └── model.pkl           # Serialized AI model (binary)
├── frontend/
│   ├── src/
│   │   └── App.jsx         # Dashboard logic and UI
│   └── package.json        # Frontend dependencies
└── README.md
```

---

## Quick Start Guide

### Prerequisites

- Python 3.9 or higher
- Node.js and npm
- Basic familiarity with terminal/command line

### 1. Backend Setup

The backend handles data ingestion and AI analysis.

```bash
cd backend
pip install fastapi uvicorn scikit-learn pandas sqlalchemy

# Start the server (creates gridmon.db automatically on first run)
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be accessible at `http://localhost:8000`.

### 2. Agent Setup

Run the agent on each machine you want to monitor.

```bash
cd agent
pip install psutil requests

# Ensure SERVER_URL in monitor.py matches your backend IP
python monitor.py
```

The agent will begin sending telemetry data every few seconds.

### 3. Dashboard Setup

Launch the visualization interface.

```bash
cd frontend
npm install
npm run dev -- --host
```

Access the dashboard at `http://localhost:5173`.

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent | Python, psutil | Lightweight metrics collection |
| Backend | FastAPI, Uvicorn | REST API for ingestion and AI scoring |
| Database | SQLite (SQLAlchemy) | Local file-based storage |
| AI Engine | Scikit-Learn | Isolation Forest anomaly detection |
| Frontend | React, Recharts | Interactive data visualization |

---

## Current Limitations

While functional, the v1.0 prototype has several critical bottlenecks that prevent production deployment:

**Minimal Training Data**  
The AI model (model.pkl) was trained on only ~1,000 data points (approximately 15 minutes of usage). This leads to "paranoid AI" behavior, where legitimate high-load tasks are often misclassified as anomalies.

**Database Locking**  
SQLite is a file-based database that cannot handle concurrent writes from multiple agents. If two agents send logs simultaneously, the database locks and the system crashes.

**Synchronous Blocking**  
The backend runs AI inference and database writes in the same thread. During high load, this causes API latency to spike, slowing down the monitoring itself.

**No Data Retention Policy**  
The database grows indefinitely. In a real data center, this would fill the disk within days.

**Hardcoded Configuration**  
IP addresses and port numbers are hardcoded in the agent and frontend, making deployment to new environments tedious and error-prone.

---

## Future Roadmap (v2.0)

To address the limitations above, the following upgrades are planned:

**Migration to InfluxDB**  
Replace SQLite with a dedicated time-series database to handle high-velocity writes and automatic data expiry.

**Grafana Integration**  
Replace the React dashboard with Grafana for enterprise-grade visualization, alerting, and plugin support.

**Asynchronous Processing**  
Move AI inference to a background worker (using Redis/Celery) to prevent API blocking and improve throughput.

**Expanded Training Set**  
Collect 24 hours of diverse workload data to retrain the Isolation Forest for improved accuracy and reduced false positives.

**Configuration Management**  
Implement environment variables and configuration files to eliminate hardcoded values and simplify deployment.

**Multi-Tenancy Support**  
Add user authentication and per-organization data isolation for shared hosting environments.

---

## How It Works

**Data Collection**  
The agent uses Python's `psutil` library to gather CPU usage, memory consumption, and disk I/O metrics. These metrics are packaged as JSON and sent to the backend via HTTP POST requests.

**Anomaly Detection**  
When the backend receives telemetry data, it passes the metrics through a pre-trained Isolation Forest model. The model assigns an anomaly score based on how different the current metrics are from the learned normal behavior. A score above a threshold triggers an anomaly flag.

**Storage and Visualization**  
All telemetry data—including timestamps, metrics, and anomaly flags—is stored in SQLite. The dashboard queries this data via the backend's REST API and displays it using interactive charts.

---

## Educational Purpose

GridMon was created for the "Build an AI Center" educational track. It demonstrates:

- Integrating machine learning models into production-like systems
- Designing distributed architectures with multiple communicating components
- Building full-stack applications with modern web technologies
- Understanding the trade-offs between rapid prototyping and production-ready systems

---

## License

MIT License. See LICENSE file for details.

---

## Contributing

This is an educational project. Contributions, bug reports, and feature requests are welcome via GitHub issues and pull requests.

---

## Support

For questions or issues:

- Open an issue on GitHub
- Consult the inline code documentation
- Review the v2.0 roadmap for planned improvements
