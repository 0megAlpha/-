# Open WebUI 還原指南
- VPS 上 /root/open-webui 是資料目錄（webui.db / uploads / vector_db，890M）— 不進 git
- 容器：open-webui-secure（docker），服務於 Tailscale 100.126.48.60:8081
- 完整備份：見 LARGE_FILES.md 的 openwebui tar.gz
- 還原：解壓資料目錄 → docker run 同參數掛載
