# Problem Statement 2 — Python System & Application Monitoring

This directory contains the Python-based solution for Problem Statement 2.

Two objectives were selected:

1. System Health Monitoring Script
2. Application Health Checker

The solution is designed for Linux environments and uses Python to monitor both system-level and application-level health.

---

## Objectives Implemented

### Objective 1 — System Health Monitoring

The `system_health_monitor.py` script monitors:

- CPU usage
- Memory usage
- Root filesystem disk usage
- Number of running processes

Each metric is compared against configurable thresholds defined in `config.json`.

If a threshold is exceeded:

- An `ALERT` status is displayed in the console.
- The alert is written to `logs/health_monitor.log`.

Otherwise, the system is reported as `HEALTHY`.

### Objective 4 — Application Health Checker

The `application_health_checker.py` script checks whether an HTTP/HTTPS application is available.

It reports:

- Application URL
- HTTP status code
- UP/DOWN status
- Response time
- Error information when the application is unavailable

The script considers an application `UP` when a successful HTTP response is received.

Connection failures and HTTP errors are reported as `DOWN`.

---

## Technology Stack

- Python 3
- psutil
- pytest
- Python `urllib`
- Python `ssl`
- Linux
- Bash/Linux command line

---

## Project Structure

```text
PS2/
├── .gitignore
├── README.md
├── config.json
├── requirements.txt
├── system_health_monitor.py
├── application_health_checker.py
├── logs/
│   └── .gitkeep
└── tests/
    └── test_health_checker.py
