# 📉 GridMon Latency Optimization Log

**Goal:** Reduce end-to-end telemetry latency (Agent -> API -> DB) to a stable < 10ms.
**Initial Baseline:** 50ms - 250ms (Highly volatile).

| Step | Optimization | Component | Latency Before | Latency After | Delta |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | Baseline (Synchronous DB, TCP Handshakes) | All | ~200ms avg | - | - |
| 1 | TCP Connection Pooling (`requests.Session`) | Agent Layer | ~200ms | ~25ms | -175ms |
| 2 | Inference Optimization (Removed Pandas) | API Layer | ~25ms | ~15ms | -10ms |
