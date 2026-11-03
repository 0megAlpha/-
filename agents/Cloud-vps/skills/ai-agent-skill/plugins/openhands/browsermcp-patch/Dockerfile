FROM ghcr.io/openhands/agent-canvas:1.27.1
USER root
RUN apt-get update && apt-get install -y --no-install-recommends lsof \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/browsermcp && npm install --prefix /opt/browsermcp --no-audit --no-fund @browsermcp/mcp@0.1.3
COPY patch-browsermcp.py /tmp/patch-browsermcp.py
RUN python3 /tmp/patch-browsermcp.py \
    && rm -f /tmp/patch-browsermcp.py \
    && node --check /opt/browsermcp/node_modules/@browsermcp/mcp/dist/index.js \
    && chown -R 10001:10001 /opt/browsermcp
USER openhands
