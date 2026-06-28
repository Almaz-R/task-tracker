# Task Tracker Architecture

This document describes the architecture of the Task Tracker DevOps sandbox project.

---

1. High-Level Architecture


User Browser
    |
    | HTTP
    v
Yandex Cloud VM Static Public IP
    |
    | NodePort 30088
    v
Ingress Nginx Controller
    |
    +-----------------------------+
    |                             |
    v                             v
/test/* namespace              /prod/* namespace
task-tracker-test              task-tracker-prod

The project has two isolated Kubernetes environments:

task-tracker-test
task-tracker-prod

Each environment contains its own application components:

frontend
backend
PostgreSQL
Kafka
consumer
monitoring/logging components

2. Application Architecture

Frontend
    |
    | HTTP request
    v
Backend API
    |
    +------------------------+
    |                        |
    v                        v
PostgreSQL              Kafka topic
tasks table             task-created
                             |
                             v
                        Kafka Consumer
Request Flow
User opens the frontend.
User creates a task.
Frontend sends an HTTP POST request to the backend.
Backend saves the task into PostgreSQL.
Backend publishes an event to Kafka.
Consumer reads the Kafka message.
Consumer processes the task event.
Logs are written to stdout.
Fluent Bit collects logs.
OpenSearch stores logs.
Logs are available in OpenSearch Dashboards.

3. GitOps Architecture

Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +-------------------------+
    |                         |
    v                         v
Docker Hub              Updated Kustomize manifests
    |                         |
    +-----------+-------------+
                |
                v
              ArgoCD
                |
                v
          Kubernetes Cluster

ArgoCD watches the Git repository and automatically applies the desired state to the Kubernetes cluster.

4. Environment Separation

Environment	Git Branch	Namespace	Image Tag
Test	develop	task-tracker-test	test-commit_sha
Prod	main	task-tracker-prod	prod-commit_sha
Test Flow
git push develop
    |
    v
GitHub Actions
    |
    v
Build images with test-commit_sha tag
    |
    v
Update test Kustomize overlays
    |
    v
ArgoCD deploys to task-tracker-test
Prod Flow
merge develop into main
    |
    v
GitHub Actions
    |
    v
Build images with prod-commit_sha tag
    |
    v
Update prod Kustomize overlays
    |
    v
ArgoCD deploys to task-tracker-prod

5. Kubernetes Components

Deployment

Deployment manages application pods.

Used for:

backend
frontend
consumer
PostgreSQL
Kafka
Grafana
OpenSearch Dashboards

Deployment controls:

desired number of replicas
container image
environment variables
pod template
rollout strategy
Service

Service provides a stable internal DNS name and virtual IP for pods.

Examples:

backend-service
postgres-service
kafka-service
frontend-service

Pods can be recreated and receive new IP addresses, but Service name remains stable.

Ingress

Ingress exposes internal services outside the cluster.

The project uses Nginx Ingress Controller with NodePort.

External access flow:

Browser
    |
    v
VM_PUBLIC_IP:30088
    |
    v
Ingress Nginx
    |
    v
Kubernetes Service
    |
    v
Pod
ConfigMap

ConfigMap stores non-sensitive configuration.

Used for:

Fluent Bit configuration
Grafana configuration
OpenSearch Dashboards configuration
Secret

Secret stores sensitive data.

Used for:

Grafana credentials
application credentials if required

6. Networking

External Traffic Flow
Internet
   |
   v
Yandex Cloud Static Public IP
   |
   v
NodePort 30088
   |
   v
Ingress Nginx Controller
   |
   v
Application Service
   |
   v
Application Pod
Internal DNS

Kubernetes provides internal DNS names.

Examples:

backend-service
postgres-service
kafka-service
opensearch-service

Backend connects to PostgreSQL using:

postgres-service:5432

Backend connects to Kafka using:

kafka-service:9092

Fluent Bit sends logs to OpenSearch using:

opensearch-service:9200

7. Observability Architecture

Application Pods
    |
    | stdout logs
    v
/var/log/containers/*.log
    |
    v
Fluent Bit DaemonSet
    |
    v
OpenSearch
    |
    v
OpenSearch Dashboards
Structured Logging

Backend and consumer write JSON logs.

Example task flow:

create_task_request_received
task_saved_to_db
task_sent_to_kafka
task_processing_started
task_processed_successfully

This allows tracing the full event lifecycle by searching task name in OpenSearch Dashboards.

8. Monitoring

Grafana is available in both environments.

Monitoring components collect Kubernetes metrics and application information.

Grafana dashboards can be used to observe:

running pods
pod restarts
CPU usage
memory usage
namespace-level workload state

9. Log Retention

OpenSearch logs are stored in daily indexes:

k8s-logs-YYYY.MM.DD

A Kubernetes CronJob deletes old log indexes after 7 days.

This prevents unlimited disk growth.

10. Infrastructure Layer

Terraform

Terraform manages Yandex Cloud infrastructure.

Used for:

VM creation
network configuration
remote state backend

Terraform keeps infrastructure state and allows repeatable provisioning.

Ansible

Ansible configures the VM after provisioning.

Used for:

installing packages
configuring firewall
checking services
preparing the server
11. Full Request Lifecycle:

1. User opens frontend
2. Frontend sends POST /tasks
3. Ingress routes request to backend-service
4. backend-service sends traffic to backend pod
5. Backend writes task to PostgreSQL
6. Backend publishes event to Kafka
7. Consumer receives Kafka message
8. Consumer processes task
9. Backend and consumer write JSON logs
10. Fluent Bit collects logs
11. OpenSearch stores logs
12. OpenSearch Dashboards displays logs


12. Why This Architecture Is Useful

This project demonstrates:

Infrastructure as Code
Configuration management
Kubernetes workloads
GitOps deployment
CI/CD automation
Environment separation
Centralized logging
Monitoring
Event-driven architecture
Basic production-like DevOps workflow

13. Technology Stack

- Yandex Cloud
- Terraform
- Ansible
- Docker
- Kubernetes
- ArgoCD
- GitHub Actions
- Kustomize
- FastAPI
- PostgreSQL
- Kafka
- OpenSearch
- Fluent Bit
- Grafana