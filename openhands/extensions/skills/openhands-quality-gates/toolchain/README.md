# OpenHands Runtime Quality Toolchain

Install this toolchain from the OpenHands Agent directory:

    OPENHANDS_TOOLS_DIR=/opt/agents/-/openhands/workspace/.openhands/tools ./install-tools.sh

When invoked inside the OpenHands runtime container, the default target is /opt/workspace_base/.openhands/tools.

Packages pinned in package.json:
- Playwright Test + Chromium
- Biome
- ESLint
- SonarScanner npm wrapper
- Semgrep in a dedicated Python virtual environment
- Trivy copied from the host when available

Set OPENHANDS_CANVAS_URL and OPENHANDS_UI_URL before running the sample tests. SonarScanner is installed but requires a SonarQube/SonarCloud server and a runtime-injected SONAR_TOKEN.

The runtime UID is not granted direct access to the host Docker socket. Use the OpenHands Docker runtime control plane for container lifecycle operations.
