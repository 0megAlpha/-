# Portable Hermes installed-workspace snapshot

This directory preserves the VPS-installed Hermes workspace source as a pullable snapshot. It excludes live credentials, runtime state, logs, caches, Python bytecode, virtual environments, and compiled system binaries.

## Restore

1. Use a Python version compatible with this Hermes revision and install required OS tools from the project documentation.
2. Create an isolated environment with python3 -m venv .venv.
3. Activate it and run python -m pip install --upgrade pip.
4. Install the workspace using its declared packaging metadata with python -m pip install -e . when supported; otherwise follow the workspace README.
5. Copy config.yaml.example or config.json.example to the expected runtime config location and supply credentials through environment variables or a secret manager. Do not commit live credential files.

The original source repository and installer scripts remain the source of truth for toolchain downloads. Very large bundled executables are not committed because GitHub rejects individual files over 100 MiB; see TOOLCHAIN-MANIFEST.md.


## Additional installed generation

The directory portable-installs/76f6e7e5145b5f39/workspace-generation-473bc8385ab240e980a77e50f2b958f1/workspace preserves a second, materially different installed-workspace generation. Both snapshots are retained for comparison and recovery; neither contains live credentials or runtime state.


Portable source and metadata subsets from installed tools are preserved under portable-installs/tool-source/; compiled runtimes and large binaries are documented in portable-installs/TOOLCHAIN-MANIFEST.md.
