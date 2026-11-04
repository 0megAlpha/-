# Hermes VPS toolchain inventory

Inventory of locally installed tool bundles. Executable payloads are intentionally not copied into Git when individual files exceed GitHub's 100 MiB file limit. Use the project installers/bootstrap scripts to fetch or rebuild them on the target VPS.

- agent-browser-0.26.0-linux-x64
- assets
- chromium-1208 — large payloads: chromium-1208/chrome-linux64/chrome (270 MB)
- computer_use
- cua-driver-0.21.0-linux-x64
- docker
- environments
- ffmpeg-9.0.1-linux-x64 — large payloads: ffmpeg-9.0.1-linux-x64/bin/ffmpeg (146 MB), ffmpeg-9.0.1-linux-x64/bin/ffplay (148 MB), ffmpeg-9.0.1-linux-x64/bin/ffprobe (146 MB)
- i18n
- metrics
- neutts_samples
- node-26.7.0-linux-x64 — large payloads: node-26.7.0-linux-x64/bin/node (148 MB)
- npm-12.0.2-linux-x64
- packages
- python-3.14.7+20260901-linux-x64 — large payloads: python-3.14.7+20260901-linux-x64/bin/python3.14 (116 MB), python-3.14.7+20260901-linux-x64/bin/python (116 MB), python-3.14.7+20260901-linux-x64/bin/python3 (116 MB), python-3.14.7+20260901-linux-x64/lib/libpython3.14.so.1.0 (248 MB), python-3.14.7+20260901-linux-x64/lib/libpython3.14.so (248 MB)
- ripgrep-15.2.0-linux-x64
- uv-0.12.3-linux-x64

Source and configuration subsets that are safe to move between hosts are preserved under portable-installs/tool-source/.
