# Existing-stack repair overlay

This deployment helper repairs two existing integration faults without adding listeners or publishing new ports.

## Prerequisites

- Docker Compose v2+.
- Existing OpenHands deployment at /opt/agents/-/openhands.
- Existing Dify deployment at /opt/dify/docker.
- Existing environment files remain local and are never copied into this repository.

## Dify runtime token

Create a local-only token file. Do not commit it:

~~~bash
install -d -m 700 "$HOME/.config/xiaye-agent-os"
umask 077
printf 'DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN=%s\n' "$(openssl rand -hex 32)" > "$HOME/.config/xiaye-agent-os/dify-runtime.env"
chmod 600 "$HOME/.config/xiaye-agent-os/dify-runtime.env"
~~~

## Apply

~~~bash
./deploy/apply-existing-stack.sh
~~~

The script recreates only the existing LiteLLM, Dify agent_backend and Dify local_sandbox services. It does not recreate databases, Redis, OpenHands, Dify API/web, or any other service. It does not change firewall rules, NAT, published ports or reverse proxies.

The LiteLLM overlay mounts the existing regular file ./litellm/config.yaml to /app/config.yaml; the original compose file mistakenly mounted a directory at that path.

## Verify

~~~bash
curl -fsS http://127.0.0.1:14000/health/liveliness
curl -fsS http://127.0.0.1:14000/health/readiness
docker inspect docker-local_sandbox-1 --format '{{.State.Health.Status}}'
docker logs --tail 40 docker-agent_backend-1
~~~
