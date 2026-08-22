
# Wisecow — Kubernetes Deployment with CI/CD and TLS

This directory contains the solution for **Problem Statement 1** of the AccuKnox DevOps assessment.

The Wisecow application has been containerized using Docker, deployed to Kubernetes using Minikube, exposed through a Kubernetes Service and NGINX Ingress, and secured using HTTPS/TLS.

A GitHub Actions CI/CD pipeline automatically builds and publishes the Docker image to GitHub Container Registry (GHCR) and deploys the resulting image to the Minikube Kubernetes cluster through a self-hosted GitHub Actions runner.

---

## Problem Statement

Deploy the Wisecow application as a Kubernetes application.

### Requirements

1. Create a Dockerfile and corresponding Kubernetes manifests to deploy the application.
2. Create a GitHub Action that creates a new Docker image when changes are made.
3. Enable secure TLS communication for the Wisecow application.

---

# Architecture

```text
                    GitHub Repository
                           |
                           | Push to main
                           v
                    GitHub Actions CI
                           |
                           v
                    Docker Build
                           |
                           v
                         GHCR
                 GitHub Container Registry
                           |
                           | CI success
                           v
                 GitHub Actions CD Job
                           |
                           v
                Self-Hosted Linux Runner
                           |
                           v
                       Minikube
                           |
                    Kubernetes Cluster
                           |
              +------------+------------+
              |                         |
              v                         v
        Wisecow Pod 1             Wisecow Pod 2
              |                         |
              +------------+------------+
                           |
                           v
                  Kubernetes Service
                           |
                           v
                     NGINX Ingress
                           |
                        HTTPS/TLS
                           |
                           v
                   https://wisecow.local
````

---

# Project Structure

```text
wisecow/
├── Dockerfile
├── .gitignore
├── README.md
├── wisecow.sh
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── tls/
    └── openssl.cnf
```

The TLS certificate and private key are intentionally excluded from Git.

---

# Docker

The application is packaged using the provided Dockerfile.

The image is based on Ubuntu and installs the dependencies required by Wisecow:

* bash
* fortune-mod
* cowsay
* netcat-openbsd

The application listens on port `4499`.

## Build the Docker Image

```bash
docker build -t wisecow:1.0 .
```

## Run the Container

```bash
docker run --name wisecow -p 4499:4499 wisecow:1.0
```

## Test the Container

```bash
curl http://localhost:4499
```

The application returns an HTML response containing a randomly generated piece of wisdom.

---

# Kubernetes Deployment

The Kubernetes deployment is defined in:

```text
k8s/deployment.yaml
```

The deployment runs two Wisecow replicas:

```yaml
replicas: 2
```

Resource requests and limits are also configured:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

## Deploy

```bash
kubectl apply -f k8s/deployment.yaml
```

## Verify

```bash
kubectl get deployment wisecow
kubectl get pods -o wide
```

Expected deployment state:

```text
wisecow   2/2   2   2
```

---

# Kubernetes Service

The Kubernetes Service is defined in:

```text
k8s/service.yaml
```

The service uses the `ClusterIP` type and maps:

```text
Service Port: 80
Target Port : 4499
```

## Deploy the Service

```bash
kubectl apply -f k8s/service.yaml
```

## Verify

```bash
kubectl get service wisecow
kubectl get endpoints wisecow
```

The service routes traffic to the running Wisecow pods.

---

# HTTPS / TLS

Secure communication is implemented using **NGINX Ingress** and a Kubernetes TLS Secret.

The Ingress configuration is located at:

```text
k8s/ingress.yaml
```

The TLS configuration uses:

```text
Hostname: wisecow.local
```

and the Minikube IP.

## Enable Minikube Ingress

```bash
minikube addons enable ingress
```

Verify the ingress controller:

```bash
kubectl get pods -n ingress-nginx
```

Verify the IngressClass:

```bash
kubectl get ingressclass
```

Expected:

```text
NAME    CONTROLLER
nginx   k8s.io/ingress-nginx
```

---

# TLS Certificate

A self-signed certificate is generated for the local development environment.

The OpenSSL configuration is stored in:

```text
tls/openssl.cnf
```

Generate the certificate:

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout tls/tls.key \
  -out tls/tls.crt \
  -config tls/openssl.cnf \
  -extensions req_ext
```

Verify the certificate:

```bash
openssl x509 -in tls/tls.crt -text -noout | grep -A2 "Subject Alternative Name"
```

The certificate contains:

```text
DNS:wisecow.local
IP Address:192.168.49.2
```

The actual Minikube IP can be obtained with:

```bash
minikube ip
```

> The TLS private key and certificate are excluded from Git and are not committed to the repository.

---

# Kubernetes TLS Secret

Create the Kubernetes TLS Secret:

```bash
kubectl create secret tls wisecow-tls \
  --cert=tls/tls.crt \
  --key=tls/tls.key
```

Verify:

```bash
kubectl get secret wisecow-tls
```

Expected:

```text
NAME          TYPE                DATA
wisecow-tls   kubernetes.io/tls   2
```

---

# Local DNS Configuration

For local testing, map the Minikube IP to `wisecow.local`.

Find the Minikube IP:

```bash
minikube ip
```

Example:

```text
192.168.49.2
```

Add the hostname to `/etc/hosts`:

```bash
echo "192.168.49.2 wisecow.local" | sudo tee -a /etc/hosts
```

Verify:

```bash
getent hosts wisecow.local
```

---

# HTTPS Application Test

The Wisecow application can then be accessed through HTTPS:

```bash
curl -k https://wisecow.local
```

The `-k` option is used because the local development certificate is self-signed.

Expected result:

```text
<pre>
...
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
</pre>
```

The wisdom text changes between requests because the application generates random responses.

---

# GitHub Actions CI/CD

The GitHub Actions workflow is located at:

```text
.github/workflows/ci.yml
```

The workflow implements both **Continuous Integration (CI)** and **Continuous Deployment (CD)**.

---

## Continuous Integration

The CI stage:

1. Checks out the repository.
2. Logs into GitHub Container Registry.
3. Builds the Wisecow Docker image.
4. Pushes the image to GHCR.

Images are published using two tags:

```text
ghcr.io/rahulsharma2109/wisecow:latest
```

and:

```text
ghcr.io/rahulsharma2109/wisecow:<commit-sha>
```

The commit SHA tag provides an immutable reference to the exact image produced by a specific Git commit.

---

# GitHub Container Registry

The Docker image is published to:

```text
ghcr.io/rahulsharma2109/wisecow
```

The image can be pulled using:

```bash
docker pull ghcr.io/rahulsharma2109/wisecow:latest
```

The image was successfully tested from the Linux/Minikube environment.

---

# Continuous Deployment

After the CI job successfully builds and publishes the image, the CD job runs automatically.

The deployment job runs on a self-hosted Linux GitHub Actions runner connected to the Minikube environment.

The deployment process is:

```text
Git Push
   |
   v
GitHub Actions
   |
   v
Docker Build
   |
   v
Push Image to GHCR
   |
   v
CI Success
   |
   v
Self-Hosted Runner
   |
   v
kubectl set image
   |
   v
Kubernetes Rollout
   |
   v
Application Verification
```

The deployment updates the Kubernetes Deployment using the exact Git commit SHA image.

Example:

```bash
kubectl set image deployment/wisecow \
  wisecow=ghcr.io/rahulsharma2109/wisecow:<commit-sha>
```

The actual SHA is automatically supplied by GitHub Actions.

---

# Kubernetes Rollout Verification

The CI/CD deployment verifies the Kubernetes rollout:

```bash
kubectl rollout status deployment/wisecow --timeout=180s
```

The deployment is then checked with:

```bash
kubectl get deployment wisecow
kubectl get pods -o wide
kubectl get service wisecow
```

The final deployment successfully ran two Wisecow replicas.

---

# Final Deployment Verification

The deployed Docker image can be verified with:

```bash
kubectl get deployment wisecow \
  -o=jsonpath='{.spec.template.spec.containers[0].image}'; echo
```

Example:

```text
ghcr.io/rahulsharma2109/wisecow:dc97d7f54288ba0d72bfde9f1c61fd815b627da2
```

This confirms that Kubernetes is running the exact image associated with the Git commit that triggered the deployment.

---

# Application Verification

The final application was tested using:

```bash
curl -k https://wisecow.local
```

The request successfully returned the Wisecow HTML response over HTTPS.

The deployment was also verified with:

```bash
kubectl get deployment wisecow
kubectl get pods -o wide
kubectl get service wisecow
```

Final state:

```text
Deployment: 2/2 replicas available
Pods:       Running
Service:    ClusterIP
Ingress:    NGINX
Protocol:   HTTPS
```

---

# Security Considerations

The following security practices were implemented:

* HTTPS/TLS is enabled through NGINX Ingress.
* A Kubernetes TLS Secret stores the TLS certificate and private key.
* The TLS private key is excluded from Git.
* TLS runtime files are excluded using `.gitignore`.
* Docker images are stored in GitHub Container Registry.
* Kubernetes uses an immutable Git commit SHA image tag for deployments.
* Kubernetes resource requests and limits are defined.
* The application is exposed through a Kubernetes Service rather than directly exposing individual pods.
* The GitHub Actions deployment runs through a dedicated self-hosted runner.

---

# Technologies Used

| Technology                | Purpose                      |
| ------------------------- | ---------------------------- |
| Docker                    | Application containerization |
| Kubernetes                | Container orchestration      |
| Minikube                  | Local Kubernetes cluster     |
| kubectl                   | Kubernetes management        |
| NGINX Ingress             | HTTP/HTTPS ingress           |
| OpenSSL                   | TLS certificate generation   |
| GitHub Actions            | CI/CD automation             |
| GitHub Container Registry | Docker image registry        |
| Bash                      | Original Wisecow application |
| Linux                     | Deployment environment       |

---

# Verification Summary

| Requirement                     | Status   |
| ------------------------------- | -------- |
| Dockerfile                      | Complete |
| Docker image                    | Complete |
| Kubernetes Deployment           | Complete |
| Kubernetes Service              | Complete |
| Two application replicas        | Complete |
| NGINX Ingress                   | Complete |
| HTTPS/TLS                       | Complete |
| Kubernetes TLS Secret           | Complete |
| GitHub Actions CI               | Complete |
| GHCR image publishing           | Complete |
| GitHub Actions CD               | Complete |
| Self-hosted deployment runner   | Complete |
| Kubernetes rollout verification | Complete |
| HTTPS application test          | Complete |

---

# Result

The Wisecow application was successfully:

* Containerized using Docker.
* Deployed to Kubernetes using Minikube.
* Configured with two replicas.
* Exposed through a Kubernetes Service.
* Exposed through NGINX Ingress.
* Secured using HTTPS/TLS.
* Published to GitHub Container Registry.
* Automatically built through GitHub Actions.
* Automatically deployed to Minikube through a self-hosted runner.
* Verified using Kubernetes rollout checks.
* Verified through an HTTPS application request.

The implementation therefore satisfies the requested Docker, Kubernetes, CI/CD, and secure TLS requirements for Problem Statement 1.

README. Also, don't paste `tls.key` anywhere into GitHub. Your current setup correctly keeps it out of Git.
```
