# opencode-data-agent

Standalone OpenCode data sub-agent plugin for Windows. 

## Commands
- `/data` (master hub)
- `/analyze`
- `/explore-data`
- `/write-query`
- `/create-viz`
- `/build-dashboard`
- `/validate`

## Skills
- `sql-queries`
- `data-exploration`
- `data-visualization`
- `statistical-analysis`
- `data-validation`
- `interactive-dashboard-builder`
- `data-context-extractor`

## Requirements

- **Node.js**: recommended 22+
- **npm**: recommended 10+
- **Runtime dependency**: `@opencode-ai/plugin` (installed automatically with package)

### Python (for visualization/dashboard commands)

- **Required for**: `/create-viz`, `/build-dashboard`
- **Version**: Python 3.10+
- **Install**: https://www.python.org/downloads/
- **Required libraries**: `pandas`, `matplotlib`, `seaborn`, `plotly`

If Python is unavailable, plugin falls back to instructions/code output.

## Installation (Windows)

```powershell
npm install -g opencode-data-agent
```

Add plugin to `%USERPROFILE%\.config\opencode\opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "opencode-data-agent"
  ]
}
```

Restart OpenCode and run `/data`.

## MCP behavior
- `/write-query` generates SQL code only.
- User runs SQL against their own database/warehouse environment.

## Runtime state
- `%USERPROFILE%\.local\share\opencode-data-agent\state.json`

## Development

```powershell
npm install
npm run build
npm run typecheck
```

## Credits & Attribution

This plugin is based on the Data plugin from Anthropic's
knowledge-work-plugins repository, licensed under Apache 2.0.

- **Original source:** https://github.com/anthropics/knowledge-work-plugins/tree/main/data
- **Architecture inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode)
- **License:** Apache 2.0 -- see LICENSE file for details

---

## ⚠️ Disclaimer

This plugin has been tested in a controlled environment with sample datasets.

Before using on full-scale or production data:

- Test with your own data in a safe/isolated environment first
- Evaluate the results carefully before relying on them
- Python-dependent commands (`/create-viz`, `/build-dashboard`) require `pandas`, `matplotlib`, `seaborn`, `plotly` installed
- SQL commands (`/write-query`) generate code only — always review before running against a real database

Found unexpected behavior or bugs? Please report your experience in the issue section.

Your feedback helps improve accuracy and future updates.
