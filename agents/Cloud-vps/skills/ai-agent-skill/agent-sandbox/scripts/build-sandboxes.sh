#!/bin/bash
set -uo pipefail
LOG=/tmp/build-sandboxes.log
: > "$LOG"
mkdir -p /opt/openhands-sandbox/{workspace,logs,cache} /opt/dsh-sandbox/{workspace,logs,cache} /opt/opencode-sandbox/{workspace,logs,cache} /opt/hermes-sandbox/{workspace,logs,cache}
cat > /opt/openhands-sandbox/Dockerfile << 'DF_OH'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs npm git curl wget jq tree build-essential python3-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests httpx beautifulsoup4 pandas numpy scipy pytest unittest-xml-reporting black ruff mypy playwright && playwright install --with-deps chromium 2>/dev/null || true
RUN npm install -g typescript ts-node eslint prettier jest mocha 2>/dev/null || true
WORKDIR /workspace
VOLUME /workspace
CMD ["/bin/bash"]
DF_OH
cat > /opt/dsh-sandbox/Dockerfile << 'DF_DSH'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs npm git curl wget jq build-essential python3-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests httpx pytest black ruff mypy 2>/dev/null || true
WORKDIR /workspace
VOLUME /workspace
CMD ["/bin/bash"]
DF_DSH
cat > /opt/opencode-sandbox/Dockerfile << 'DF_OC'
FROM node:20-slim
RUN apt-get update && apt-get install -y git curl wget jq build-essential python3 && rm -rf /var/lib/apt/lists/*
RUN npm install -g typescript ts-node eslint prettier jest mocha 2>/dev/null || true
WORKDIR /workspace
VOLUME /workspace
CMD ["/bin/bash"]
DF_OC
cat > /opt/hermes-sandbox/Dockerfile << 'DF_HM'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git curl wget jq build-essential python3-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests httpx pytest black ruff 2>/dev/null || true
WORKDIR /workspace
VOLUME /workspace
CMD ["/bin/bash"]
DF_HM
for n in openhands dsh opencode hermes; do
  docker build -t ${n}-sandbox:latest /opt/${n}-sandbox/ >> "$LOG" 2>&1 || {
    echo "${n} build failed, fallback base image" >> "$LOG"
    case $n in opencode) docker pull node:20-slim >> "$LOG" 2>&1 && docker tag node:20-slim ${n}-sandbox:latest ;; *) docker pull python:3.11-slim >> "$LOG" 2>&1 && docker tag python:3.11-slim ${n}-sandbox:latest ;; esac
  }
  echo "${n}-sandbox: $(docker image inspect ${n}-sandbox:latest >/dev/null 2>&1 && echo OK || echo FAIL)" >> "$LOG"
done
touch /tmp/sandboxes.done
