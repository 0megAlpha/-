# 20260924 修復記錄（本次崩溃元凶：dsh-purge autoUpdateOnStart）
問題：dsh-purge 插件預設 autoUpdateOnStart=true，每次服務啟動都跑插件自動更新(pnpm)。
     pnpm-lock.yaml 仍鎖定 0.1.6-alpha 污染核心套件 → 蓋掉 dsh-settings 相容層(shim)
     → 5 個 import 錯誤 → 崩潰 → systemd 重啟 → 又觸發更新 → 無限循環(累積 2956 次重啟)。
修復：
  1. cordis.patch.yml 增加 `- id: dsh-purge / config: autoUpdateOnStart: false`（見本目錄）
  2. 隔離 82 個污染核心套件 → /root/.dsh/quarantine-cores-20260924-051256/
     （fallback /root/.dsh/profiles/node_modules 接手，統一解析到 CLI 0.1.5-rc.2）
  3. 還原 dsh-settings 相容層 shim（本備份 shim/ 目錄，pnpm install 會蓋掉它，被蓋就照此還原）
  4. /var/log/dsh-web.log 改 600 權限並清空（舊日誌含歷史 token）
警告：
  - 不要在此 profile 裸跑 pnpm install（鎖檔仍記錄 alpha 版）
  - 裝插件一律用 dsh plugin --profile web add <pkg>
  - shim 被覆蓋時：cp -r <本備份>/shim/dsh-settings /root/.dsh/profiles/web/node_modules/@deepseek-ai/
