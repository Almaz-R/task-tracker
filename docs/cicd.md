# CI/CD and GitOps Pipeline

This document describes the delivery pipeline of the Task Tracker project.

---

# 1. Branch Strategy

The project uses two Git branches.

| Branch | Environment |
|--------|-------------|
| develop | TEST |
| main | PROD |

---

2. Deployment Flow

TEST

Developer
    |
git push develop
    |
    v
GitHub Actions
    |
    v
Build Docker images
    |
    v
Push images to Docker Hub
    |
    v
Update Kustomize manifests
    |
    v
Commit image tags
    |
    v
ArgoCD detects changes
    |
    v
Deploy to task-tracker-test

PROD
Developer
    |
merge develop -> main
    |
    v
GitHub Actions
    |
    v
Build production images
    |
    v
Push images to Docker Hub
    |
    v
Update production manifests
    |
    v
ArgoCD sync
    |
    v
Deploy to task-tracker-prod

3. Image Tags

The project uses commit-based image tags.

Examples:

test-7ebfebb
prod-9b45e1e

This provides:

reproducible deployments
rollback capability
image history
deployment traceability

4. Docker Images

Backend:

almaz8412/task-tracker

Consumer:

almaz8412/consumer

Frontend:

almaz8412/task-tracker-frontend

5. GitHub Actions Pipeline

Pipeline stages:

Checkout repository.
Install dependencies.
Run backend tests.
Build Docker images.
Push images to Docker Hub.
Run vulnerability scan.
Update Kustomize image tags.
Commit updated manifests.
Push changes back to Git.

6. Automated Tests

Backend tests are executed before image build.

Pipeline fails if tests fail.

This prevents broken code from reaching the cluster.

7. Vulnerability Scanning

Trivy scans container images.

The pipeline fails for:

CRITICAL vulnerabilities
HIGH vulnerabilities

This improves container security.

8. GitOps

The cluster is not modified manually.

The source of truth is Git.

ArgoCD continuously compares:

Desired state:
Git repository

Actual state:
Kubernetes cluster

If differences appear, ArgoCD synchronizes the cluster.

9. ArgoCD Applications

Applications:

test-backend
test-consumer
test-frontend
test-kafka
test-database
test-monitoring
prod-backend
prod-consumer
prod-frontend
prod-kafka
prod-database
prod-monitoring

10. Rollback

Rollback is performed by:

Reverting Git commit.
Pushing changes.
ArgoCD synchronization.

No manual kubectl apply commands are required.

11. Benefits
Full automation
Environment separation
Git history
Safe deployments
Easy rollback
GitOps approach
Production-like workflow