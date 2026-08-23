# AccuKnox Technical Assessment

This repository contains my solutions for the AccuKnox technical assessment.

## Problem Statements

### PS1 — Wisecow Kubernetes Deployment

Deploying the Wisecow application as a Kubernetes workload with containerization, HTTPS/TLS, and CI/CD.

#### Implemented

- Dockerized the Wisecow application
- Created Kubernetes Deployment
- Created Kubernetes Service
- Created Kubernetes Ingress
- Enabled HTTPS/TLS communication
- Created a self-signed TLS certificate for local deployment
- Published the Docker image to GitHub Container Registry (GHCR)
- Implemented GitHub Actions CI pipeline
- Implemented continuous deployment to Minikube
- Configured a GitHub Actions self-hosted runner
- Verified successful Kubernetes rollout
- Verified the deployed application through HTTPS

#### Technologies

- Docker
- Kubernetes
- Minikube
- GitHub Actions
- GitHub Container Registry
- Bash
- Nginx Ingress
- OpenSSL
- HTTPS/TLS

#### Solution

[View PS1 — Wisecow](./PS1/wisecow)

---

### PS2 — Python Monitoring Solutions

Two objectives from the provided problem statement were implemented using Python.

#### Objective 1 — System Health Monitoring Script

The script monitors the health of a Linux system and checks:

- CPU usage
- Memory usage
- Disk usage
- Running process count

Configurable thresholds are used to identify abnormal conditions. When a threshold is exceeded, an alert is displayed in the console and recorded in a log file.

#### Objective 2 — Application Health Checker

The application health checker verifies whether an application is functioning correctly by checking:

- HTTP/HTTPS connectivity
- HTTP status code
- Response time
- Application availability
- Connection and request errors

The application is reported as `UP` when it responds successfully and `DOWN` when it is unavailable or fails the health check.

#### Testing

Automated tests were implemented using `pytest`.

The health-checking test suite verifies both:

- Application available / UP condition
- Application unavailable / DOWN condition

All implemented tests passed successfully.

#### Technologies

- Python
- psutil
- pytest
- HTTP/HTTPS
- JSON configuration
- Python logging

#### Solution

[View PS2 — Python Monitoring Solutions](./PS2)

---

## Repository Structure


accuknox-assessment/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── PS1/
│   └── wisecow/
│       ├── Dockerfile
│       ├── README.md
│       ├── wisecow.sh
│       └── k8s/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
│
└── PS2/
    ├── README.md
    ├── application_health_checker.py
    ├── system_health_monitor.py
    ├── config.json
    ├── requirements.txt
    ├── tests/
    │   └── test_health_checker.py
    └── logs/
        └── .gitkeep


## CI/CD

The PS1 Wisecow deployment includes a GitHub Actions CI/CD pipeline.

The pipeline:

1. Checks out the repository
2. Builds the Wisecow Docker image
3. Authenticates with GitHub Container Registry
4. Pushes the image to GHCR
5. Uses the image commit SHA for versioned deployment
6. Deploys the image to the Minikube Kubernetes cluster through a self-hosted runner
7. Waits for the Kubernetes rollout to complete
8. Verifies the deployed pods and service
9. Performs an HTTPS application health check

## Security

PS1 includes HTTPS/TLS communication for the Wisecow application.

The TLS certificate is generated locally for the Minikube environment and the private key is excluded from version control.

PS2 includes error handling, configurable monitoring thresholds, and automated health-check tests.

## Problem Statement 3

The KubeArmor zero-trust security challenge was optional and was not implemented as part of this submission.

## Author

**Rahul Sharma**

MCA — Cloud Computing & DevOps
