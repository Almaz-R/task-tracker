# Подготовка к собеседованию по проекту Task Tracker

---

# 1. Расскажите о своем проекте

Я разработал собственный DevOps-проект Task Tracker.

Это микросервисное приложение, развернутое в Kubernetes с использованием GitOps-подхода.

Проект состоит из:

* Frontend
* Backend (FastAPI)
* PostgreSQL
* Kafka
* Kafka Consumer
* OpenSearch
* Fluent Bit
* ArgoCD
* GitHub Actions

Есть два независимых окружения:

* TEST
* PROD

Деплой полностью автоматизирован.

---

# 2. Какая архитектура проекта?

Пользователь обращается к frontend через Ingress.

Frontend вызывает backend.

Backend:

* сохраняет данные в PostgreSQL;
* отправляет событие в Kafka.

Consumer получает сообщение и обрабатывает его.

Все сервисы пишут JSON-логи.

Fluent Bit собирает логи и отправляет их в OpenSearch.

Логи доступны через OpenSearch Dashboards.

---

# 3. Как работает CI/CD?

TEST:

* push в develop;
* GitHub Actions собирает образы;
* публикует их в Docker Hub;
* обновляет Kustomize;
* ArgoCD автоматически деплоит TEST.

PROD:

* merge develop → main;
* сборка prod-образов;
* обновление манифестов;
* ArgoCD деплоит PROD.

---

# 4. Что такое GitOps?

Git является источником истины.

Изменения в кластер напрямую не применяются.

ArgoCD постоянно сравнивает:

* состояние Git;
* состояние Kubernetes.

Если есть различия — кластер синхронизируется автоматически.

---

# 5. Зачем Kafka?

Kafka используется для асинхронной обработки.

Backend не выполняет всю работу сам.

Он отправляет событие:

task-created

Consumer получает сообщение и обрабатывает его отдельно.

Это уменьшает связанность сервисов.

---

# 6. Как работает логирование?

Приложения пишут JSON-логи.

Fluent Bit собирает контейнерные логи.

OpenSearch хранит логи.

Можно найти всю цепочку обработки задачи:

* create_task_request_received
* task_saved_to_db
* task_sent_to_kafka
* task_processing_started
* task_processed_successfully

---

# 7. Как вы ищете проблемы?

Мой алгоритм:

1. kubectl get pods
2. kubectl describe pod
3. kubectl logs
4. kubectl exec
5. проверка Service
6. проверка Ingress
7. проверка зависимостей
8. проверка ArgoCD

---

# 8. Что было самым сложным?

* Ingress и пути.
* OpenSearch Dashboards.
* Fluent Bit.
* Разделение TEST и PROD.
* Автоматическое обновление тегов.
* Настройка GitOps.

---

# 9. Что бы вы улучшили?

* Prometheus.
* Полноценные Grafana Dashboard.
* HPA.
* Alertmanager.
* Helm Charts.
* Несколько Kubernetes-нод.
* Terraform remote state.

---

# 10. Почему вы сделали этот проект?

Чтобы:

* изучить DevOps-практики;
* понять Kubernetes;
* изучить GitOps;
* научиться траблшутингу;
* получить реальный проект для собеседований.

---

# 11. Что вы изучили?

* Docker
* Kubernetes
* Kustomize
* ArgoCD
* GitHub Actions
* Kafka
* PostgreSQL
* OpenSearch
* Fluent Bit
* Terraform
* Ansible
* GitOps
* CI/CD

---

# 12. Итог

Этот проект используется мной как:

* портфолио;
* учебный стенд;
* среда для траблшутинга;
* подготовка к собеседованиям.
