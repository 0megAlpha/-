# DSH 還原指南（新 VPS）
1. 安裝：npm i -g @deepseek-ai/dsh ；systemd unit 見 recovery/dsh-web.service
2. 插件清單：plugin-inventory.txt；一律用 `dsh plugin --profile web add <套件>` 安裝
3. ⚠️ 永遠不要在 profile 內裸跑 `pnpm install`（鎖檔 alpha 污染會回來）
4. ⚠️ dsh-purge 的 autoUpdateOnStart 必須保持 false（每次啟動自動 pnpm = 崩潰循環元凶）
5. dsh-settings 相容 shim 在 recovery/（settingsNamespace 舊 API）；被 pnpm 蓋掉就還原
6. 敏感檔（.env、.credentials.yaml、storages、sessions）不在此 repo — 從 VPS 備份手動還原
