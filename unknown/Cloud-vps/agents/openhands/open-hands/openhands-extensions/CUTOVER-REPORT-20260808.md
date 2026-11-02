# Agent Canvas Production Cutover Report — 2026-08-08

## 1. Pre-Cutover State (recorded)

### Old Production Nginx Config (backup: /root/ai-company/staging-openhands/eni-gateway.bak-20260808-230639)
- :3000 -> http://127.0.0.1:3001 (old production OpenHands app, internal port 3001)
- :8080 -> http://127.0.0.1:8081 (OpenWebUI)
- Both blocks: Basic Auth via /etc/nginx/.eni-htpasswd (user: eni)

### Old Production Container
- name: openhands-app-   image: openhands:latest (sha256:1ef3ed2335c1)
- status BEFORE cutover: running (exited during cutover window, ExitCode 137)
- network: host | command: uvicorn openhands.server.listen:app --host 127.0.0.1 --port 3001
- LLM_MODEL=openai/glm-5.2 | LLM_BASE_URL=http://localhost:4000/v1 (LiteLLM gateway)
- restart policy: no (will NOT auto-restart; safe to keep stopped)
- source repo: /root/openhands @ my-custom branch commit 3dceff0181566d025291fd62de6223a4e8c29254

## 2. Staging Verification (before cutover)
- container: openhands-canvas-staging (openhands-canvas:staging, sha256:e62ce177c727)
- /health 200 | /ready 200 | /server_info 200 (agent server v1.40.1, build_git_sha c1877b44)
- REAL LLM TASK: conversation 81904da2-37f0-429f-b482-8f8a6b6c6b09 -> finished, agent_final_response = "LLM-TASK-OK"
  (model openai/glm-5.2 via LiteLLM :4000 -> NVIDIA, 7696 prompt / 19 completion tokens)

## 3. Cutover Actions
1. nginx config /etc/nginx/sites-available/eni-gateway updated: :3000 -> http://127.0.0.1:8000 (Agent Canvas staging)
2. nginx -t: PASSED ("configuration file test is successful")
3. systemctl reload nginx: OK
4. Basic Auth verified: :3000 no-auth -> 401; with eni creds -> 308 -> /canvas/ (HTTP 200)
5. Old production container openhands-app- STOPPED (exited 137), NOT deleted (rollback kept)
6. Double-execution check: only openhands-canvas-staging running; old prod not listening (:3001 free); no stray tmux pools

## 4. Post-Cutover Production Verification (all via :3000)
| Check | Result |
|---|---|
| Web UI | HTTP 308 -> /canvas/ -> 200 (OpenHands title) |
| API | /server_info 200, /api/conversations POST 201 |
| LLM task | conversation 8df75a36-64e7-4f0b-93ae-4d7acf8445d5 -> finished, response "PROD-CUTOVER-OK" |
| logs | nginx access.log shows eni-authed proxied requests; container logs show full run |
| External access | http://x.x.x.x:3000/ -> 401 (no auth), 308->/canvas (auth) |
| UFW | 3000/tcp ALLOW, 3001/tcp DENY, 8081/tcp DENY |

## 5. Versions / Commit Record
- New production entry: http://IP:3000 (Basic Auth: eni / see /root/ai-company/open-webui/.gateway-password)
- Agent Canvas image: openhands-canvas:staging, revision label e37d9561f858c26620427d172c3c77083fdd95f9
  (source /root/open-hands main branch, HEAD matches: e37d9561)
- Agent server: v1.40.1, build_git_sha c1877b44129696cb99535c0e074d22a324cc7312
- LLM gateway: LiteLLM :4000 (systemd litellm.service) -> NVIDIA glm-5.2
- Old production kept: openhands-app- (exited), image openhands:latest (1ef3ed2335c1)
- nginx upstream: :3000 -> http://127.0.0.1:8000

## 6. Rollback Method (if health check fails)
1. Restore old nginx config:
   cp /root/ai-company/staging-openhands/eni-gateway.bak-20260808-230639 /etc/nginx/sites-available/eni-gateway
   nginx -t && systemctl reload nginx
2. Restart old production container (from /root/openhands):
   docker compose up -d --no-recreate   (or: docker start openhands-app-)
3. Verify: curl http://127.0.0.1:3001/ (old app) and http://127.0.0.1:3000/ with auth
4. Optionally stop staging: docker compose -f /root/ai-company/staging-openhands/docker-compose.staging.yml stop

## 7. NOT deleted (kept for rollback)
- old container: openhands-app-
- old image: openhands:latest (1ef3ed2335c1)
- old nginx config backup: eni-gateway.bak-20260808-230639
