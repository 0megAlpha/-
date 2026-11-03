- Current Branch: main
- Remote URL: https://github.com/xh09411-web/Ai-agent-skill.git
- Uncommitted Changes (Count): 1
- Untracked/Unsaved Assets:
  -  audit_report.md

## 3. Infrastructure & Container Inventory
- Total Containers: 18
- Active Ports Mapping:
- agent-plane-caddy: 
- coolify-db: 5432/tcp
- coolify-redis: 6379/tcp
- coolify-realtime: 0.0.0.0:6001-6002->6001-6002/tcp, [::]:6001-6002->6001-6002/tcp
- openhands-canvas-staging: 
- agent-plane-cadvisor-1: 8080/tcp
- agent-plane-grafana-1: 127.0.0.1:3010->3000/tcp
- agent-plane-uptime-kuma-1: 127.0.0.1:3001->3001/tcp
- agent-plane-loki-1: 127.0.0.1:3100->3100/tcp
- agent-plane-jaeger-1: 4317-4318/tcp, 9411/tcp, 14250/tcp, 14268/tcp, 127.0.0.1:16686->16686/tcp
- agent-plane-prometheus-1: 127.0.0.1:9090->9090/tcp
- agent-plane-otel-collector-1: 127.0.0.1:4317-4318->4317-4318/tcp, 127.0.0.1:8889->8889/tcp, 55679/tcp
- agent-plane-node_exporter-1: 127.0.0.1:9100->9100/tcp
- litellm-pg: 127.0.0.1:5432->5432/tcp
- sonarqube: 0.0.0.0:9000->9000/tcp, [::]:9000->9000/tcp
- neo4j: 0.0.0.0:7474->7474/tcp, [::]:7474->7474/tcp, 7473/tcp, 0.0.0.0:7687->7687/tcp, [::]:7687->7687/tcp
- n8n: 0.0.0.0:5678->5678/tcp, [::]:5678->5678/tcp
- open-webui: 
- Bind Mounts & Volumes Overview:
                  "Destination": "/app/backend/data",
                  "Destination": "/app/data",
                  "Destination": "/data",
                  "Destination": "/etc/caddy/Caddyfile",
                  "Destination": "/etc/loki/local-config.yaml",
                  "Destination": "/etc/otel-collector-config.yaml",
                  "Destination": "/etc/prometheus/prometheus.yml",
                  "Destination": "/home/node/.n8n",
                  "Destination": "/home/openhands/.openhands",
                  "Destination": "/logs",
                  "Destination": "/loki",
                  "Destination": "/projects",
                  "Destination": "/prometheus",
                  "Destination": "/rootfs",
                  "Destination": "/sys",
                  "Destination": "/tmp",
                  "Destination": "/var/lib/docker",
                  "Destination": "/var/lib/grafana",
                  "Destination": "/var/lib/postgresql/data",
                  "Destination": "/var/run",
                  "Destination": "/var/www/html/storage/app/ssh",
                  "Destination": "/www",
                  "Source": "/",
                  "Source": "/data/coolify/ssh",
                  "Source": "/opt/agent-plane/caddy/Caddyfile",
                  "Source": "/opt/agent-plane/loki/loki-config.yml",
                  "Source": "/opt/agent-plane/otel/otel-collector-config.yml",
                  "Source": "/opt/agent-plane/prometheus/prometheus.yml",
                  "Source": "/opt/agent-plane/www",
                  "Source": "/root/ai-company/open-webui",

## 4. Secret-Safe Scan (Filename Match Only)
- Suspected Sensitive Files found:
  - [CONFIDENTIAL] /opt/agent-plane/secrets.env
  - [CONFIDENTIAL] /root/.hermes/response_store.db
  - [CONFIDENTIAL] /root/.hermes/.env
  - [CONFIDENTIAL] /root/.hermes/auth.json
  - [CONFIDENTIAL] /root/.hermes/cron/executions.db
  - [CONFIDENTIAL] /root/.hermes/state.db
  - [CONFIDENTIAL] /root/.hermes/kanban.db

## 5. Log & Large Assets Summary
- deploy.out: 待補 (未找到)
=========================================
