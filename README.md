# Task Tracker DevOps Platform

Production-like DevOps sandbox project demonstrating modern infrastructure, GitOps delivery, Kubernetes operations, observability, and CI/CD practices.

---

# Project Overview

Task Tracker is a microservice application deployed in Kubernetes using GitOps principles.

The project includes:

* FastAPI backend
* Kafka message queue
* PostgreSQL database
* Kafka consumer service
* Frontend UI
* OpenSearch logging stack
* Fluent Bit log collection
* ArgoCD GitOps delivery
* GitHub Actions CI/CD
* Terraform infrastructure provisioning
* Ansible configuration management

---

# Architecture

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Hub
   │
   ▼
ArgoCD
   │
   ▼
Kubernetes Cluster
   │
   ├── Frontend
   ├── Backend
   ├── PostgreSQL
   ├── Kafka
   ├── Consumer
   ├── OpenSearch
   └── Fluent Bit
```

---

# Technology Stack

| Component        | Technology        |
| ---------------- | ----------------- |
| Backend          | FastAPI           |
| Frontend         | HTML / JavaScript |
| Database         | PostgreSQL        |
| Message Broker   | Kafka             |
| Consumer         | Python            |
| Containerization | Docker            |
| Orchestration    | Kubernetes        |
| GitOps           | ArgoCD            |
| CI/CD            | GitHub Actions    |
| Infrastructure   | Terraform         |
| Configuration    | Ansible           |
| Logging          | Fluent Bit        |
| Log Storage      | OpenSearch        |
| Monitoring       | Grafana           |
| Cloud            | Yandex Cloud      |

---

# Environments

| Environment | Branch  | Image Tag         |
| ----------- | ------- | ----------------- |
| TEST        | develop | test-<commit_sha> |
| PROD        | main    | prod-<commit_sha> |

---

# CI/CD Pipeline

1. Push to develop.
2. Run tests.
3. Build Docker images.
4. Push images to Docker Hub.
5. Update Kustomize image tags.
6. ArgoCD detects Git changes.
7. Automatic deployment to TEST.

Production deployment:

1. Merge develop into main.
2. Build production images.
3. Push prod tags.
4. Update production manifests.
5. ArgoCD deploys to PROD.

---

# Logging

Application logs are generated in JSON format.

Fluent Bit collects container logs and sends them to OpenSearch.

Logs can be searched using OpenSearch Dashboards.

Example flow:

```text
Application
     ↓
Container stdout
     ↓
Fluent Bit
     ↓
OpenSearch
     ↓
Dashboards
```

---

# GitOps

All Kubernetes manifests are stored in Git.

ArgoCD continuously synchronizes cluster state with repository state.

No manual kubectl apply operations are required.

---

# Infrastructure

Infrastructure is provisioned using Terraform.

Server configuration is managed using Ansible.

Public VM IP address is static.

---

# Features

* Separate TEST and PROD environments
* Automatic deployments
* Commit-based image tags
* Centralized logging
* GitOps delivery
* Infrastructure as Code
* Kubernetes workloads
* Kafka event processing
* OpenSearch observability

---

# Repository Structure

```text
apps/
ansible/
kustomize/
services/
terraform/
.github/
```

---

# Future Improvements

* Prometheus monitoring
* Grafana dashboards
* Helm charts
* Horizontal Pod Autoscaler
* Alertmanager integration
* Kubernetes autoscaling

---

# Author

Almaz Rakhmatullin

DevOps learning project and interview preparation platform.

```
```
