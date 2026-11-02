# DSH (DeepSeek Harness) 資產整合清單

## 來源：VPS /root/.dsh
## 整合時間：2026-10-02T10:18:34+08:00

## 結構說明
- `config/`     → cordis yml 主配置、prompt-inject 規則
- `profiles/`   → acp / default / web 三個 profile 定義（不含 node_modules）
- `plugins/`    → 已安裝的插件源碼（不含 node_modules，需重跑 pnpm install）
- `skills/`     → 技能包（pentester 等）
- `manifests/`  → 插件版本清單

## 還原步驟（新 VPS）
1. git clone 此倉庫
2. cp -a dsh/config/* ~/.dsh/
3. cp -a dsh/profiles/* ~/.dsh/profiles/
4. cp -a dsh/plugins/* ~/.dsh/plugins/
5. cp -a dsh/skills/* ~/.dsh/dsh-pentester/skills/  (對應位置)
6. 各 profile 目錄下執行 pnpm install
7. systemctl restart dsh-web.service
