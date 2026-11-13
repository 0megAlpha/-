---
name: openhands-quality-gates
description: Run persistent Playwright browser tests, Biome, ESLint, SonarScanner, Semgrep, Trivy and Docker-backed validation from the OpenHands runtime.
---

# OpenHands Quality Gates

The persistent toolchain is installed in the OpenHands Docker runtime at `/opt/workspace_base/.openhands/tools`. The host source is `/opt/agents/-/openhands/workspace/.openhands/tools`. Do not install duplicate global copies.

## Playwright browser testing

Set:
```sh
export HOME=/opt/workspace_base/.openhands/tools/home
export PLAYWRIGHT_BROWSERS_PATH=/opt/workspace_base/.openhands/tools/ms-playwright
export NPM_CONFIG_CACHE=/opt/workspace_base/.openhands/tools/.npm-cache
cd /opt/workspace_base/.openhands/tools
```

Run `node_modules/.bin/playwright test --config playwright.config.mjs`. Tests and screenshots/traces belong under the project workspace; do not store credentials in test fixtures. Use the existing `tests/openhands-health.spec.mjs` as the minimal example. The current health smoke suite checks Canvas on host bridge port 8000 and the OpenHands UI on 13000.

## Static analysis and formatting

- Biome: `node_modules/.bin/biome check <paths>`
- ESLint: `node_modules/.bin/eslint <paths>`
- SonarScanner: `node_modules/.bin/sonar-scanner-npm`; requires a configured `SONAR_HOST_URL`, project key and runtime-injected `SONAR_TOKEN`. Do not report a Sonar server analysis until the server and token exist.

## Security scanning

- Semgrep: `HOME=/opt/workspace_base/.openhands/tools/home XDG_CACHE_HOME=/opt/workspace_base/.openhands/tools/.cache SEMGREP_USER_LOG_FILE=/opt/workspace_base/.openhands/tools/.semgrep/semgrep.log /opt/workspace_base/.openhands/tools/semgrep-venv/bin/semgrep scan --config p/python --metrics=off <paths>`.
- Trivy: `/opt/workspace_base/.openhands/tools/bin/trivy fs --scanners vuln,secret,misconfig <path>`. Review and redact findings before publishing.
- Docker runtime: OpenHands itself provisions and controls the isolated Docker runtime. The unprivileged runtime UID cannot access the host Docker socket directly; do not add it to the docker group or bypass that boundary. Use the OpenHands runtime controls for container lifecycle and keep shell-side checks inside the assigned sandbox.

## Completion criteria

A quality gate is complete only when the exact command, exit code, scanned paths, tool version and findings summary are recorded. A tool being installed is not the same as a successful scan. Sonar is marked CLI-ready/server-pending until a SonarQube/SonarCloud endpoint and token are configured.
