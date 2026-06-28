# Troubleshooting Guide

Практический конспект по диагностике проблем в проекте Task Tracker.

## Быстрая диагностика

```bash
kubectl get pods -A
kubectl get applications -n argocd
kubectl get ingress -A
kubectl get svc -A

Основной порядок проверки:
Проверить ArgoCD application.
Проверить pod status.
Посмотреть events через describe.
Посмотреть logs.
Проверить service.
Проверить ingress.
Проверить внутренний DNS.
Проверить зависимости: PostgreSQL, Kafka, OpenSearch.


Потом:

```bash
git add docs/troubleshooting.md
git commit -m "Add troubleshooting guide"
git push origin main

# 1. Pod не запускается

Симптомы:

- CrashLoopBackOff
- Error
- ImagePullBackOff
- Pending

Проверка:

```bash
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

Примеры:

```bash
kubectl logs backend-deployment-xxxx -n task-tracker-test
kubectl describe pod kafka-consumer-xxxx -n task-tracker-prod
```

---

# 2. Приложение недоступно из браузера

Проверить:

```bash
kubectl get ingress -A
kubectl get svc -A
kubectl get endpoints -A
```

Проверить сам ingress:

```bash
kubectl describe ingress frontend-ingress -n task-tracker-test
```

Проверить сервис:

```bash
kubectl get svc -n task-tracker-test
```

Проверить внутри кластера:

```bash
curl http://frontend-service
curl http://backend-service:8000/health
```

---

# 3. Backend не видит PostgreSQL

Симптомы:

- connection refused
- timeout
- database does not exist

Проверка:

```bash
kubectl logs deploy/backend-deployment -n task-tracker-test

kubectl exec -it deploy/backend-deployment \
-n task-tracker-test -- sh
```

Проверить соединение:

```bash
nc -zv postgres-service 5432
```

---

# 4. Kafka не работает

Проверить:

```bash
kubectl logs deploy/kafka-consumer -n task-tracker-test

kubectl get pods | grep kafka
```

Типичные ошибки:

- GroupCoordinatorNotAvailable
- Topic not available
- Connection refused

Проверить топики:

```bash
kubectl exec -it kafka-0 -n task-tracker-test -- sh
```

---

# 5. ArgoCD показывает OutOfSync

Проверить:

```bash
kubectl get applications -n argocd
```

Обновить:

- Refresh
- Sync

Проверить:

```bash
kubectl describe application test-backend -n argocd
```

---

# 6. Логи не появляются в OpenSearch

Проверить:

```bash
kubectl get pods -A | grep fluent

kubectl logs daemonset/fluent-bit \
-n task-tracker-test
```

Проверить индексы:

```bash
kubectl exec opensearch-0 \
-n task-tracker-test -- \
curl -k -u admin:admin \
https://localhost:9200/_cat/indices?v
```

---

# 7. Нет новых образов

Проверить:

```bash
kubectl get deploy \
-n task-tracker-test \
backend-deployment \
-o jsonpath='{.spec.template.spec.containers[0].image}'
```

Проверить Git:

```bash
git log --oneline
```

Проверить GitHub Actions.

Проверить ArgoCD.

---

# 8. Как я ищу проблему

1. kubectl get
2. kubectl describe
3. kubectl logs
4. kubectl exec
5. проверка сервисов
6. проверка ingress
7. проверка зависимостей
8. проверка ArgoCD
9. проверка CI/CD

