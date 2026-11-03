# Security Audit Skill

## 用途
自動掃描代碼 + 依賴 + 部署配置的安全漏洞

## 檢查項目
1. 硬編碼密鑰（gitleaks）
2. SQL injection 風險
3. OWASP Top 10
4. 依賴已知 CVE
5. 容器鏡像掃描（Trivy）
6. IAM 權限過寬
7. 日誌洩露敏感信息

## 觸發
- 手動：`freebuff audit <repo>`
- CI：每次 push 前跑 `pre-push` hook
