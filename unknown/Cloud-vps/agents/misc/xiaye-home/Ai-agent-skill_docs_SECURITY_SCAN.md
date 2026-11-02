# Security Scan Report

生成時間: 2026-08-13 05:13:12

## 1. gitleaks Git 歷史掃描（含過往 commit）
```
-- /root/Ai-Agent-Skill --
-- /root/ai-agent-workflows --
-- /root/ai-company --
-- /root/openhands --
```

## 2. 工作目錄明文密鑰掃描（只列路徑與規則，不顯示值）
```
/root/Ai-Agent-Skill/openhands-extensions/tests/test_live_integration_smoke.py:344:    bogus 
/root/Ai-Agent-Skill/openhands-extensions/tests/test_automation_setup.py: <REDACTED>notarealtokenvalue00"
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_slack_plugin_setup.py: <REDACTED>b-test-token", "xapp-test-token", "", "C01ABC2DE3F"],
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_slack_plugin_setup.py: <REDACTED>b-test-token", "xapp-test-token", "", ""],
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_platform_base.py: <REDACTED> OPENSSH PRIVATE KEY-----")
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_platform_base.py: <REDACTED> OPENSSH PRIVATE KEY-----")
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_config.py:997:                PlatformConfig(enabled
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_slack.py:107:    config 
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_slack_approval_buttons.py:52:    config 
/root/Ai-Agent-Skill/hermes-007/tests/gateway/test_slack_channel_session_scope.py:35:    config 
/root/Ai-Agent-Skill/hermes-007/tests/skills/test_openclaw_migration_hardening.py:58:    out 
/root/Ai-Agent-Skill/hermes-007/tests/skills/test_openclaw_migration_hardening.py:65:    out 
/root/Ai-Agent-Skill/hermes-007/tests/hermes_cli/test_whatsapp_cloud_setup.py:91:        ok, reason 
/root/Ai-Agent-Skill/hermes-007/tests/hermes_cli/test_web_server.py:177:        result 
/root/Ai-Agent-Skill/hermes-007/tests/hermes_cli/test_web_server.py:1753:            json
/root/Ai-Agent-Skill/hermes-007/tests/hermes_cli/test_copilot_auth.py:13:        valid, msg 
/root/Ai-Agent-Skill/hermes-007/tests/hermes_cli/test_set_config_value.py:275:        secret 
/root/Ai-Agent-Skill/hermes-007/tests/agent/test_bedrock_integration.py: <REDACTED>IOSFODNN7EXAMPLE")
/root/Ai-Agent-Skill/hermes-007/tests/agent/test_bedrock_integration.py: <REDACTED>IOSFODNN7EXAMPLE")
/root/Ai-Agent-Skill/hermes-007/tests/agent/test_bedrock_integration.py: <REDACTED>IOSFODNN7EXAMPLE")
```

## 3. 既有 .env 檔清單（存在性，不讀內容）


## 結論
- gitleaks git 歷史掃描：**無洩漏**（Ai-Agent-Skill / ai-agent-workflows / ai-company / openhands 全乾淨）
- 工作目錄掃描命中：全部為**測試檔的假 token 樣本**（bogus / notarealtokenvalue00 / xapp-test-token / 測試用假私鑰）
- **未發現真實密鑰洩漏**。既有 .env（/root/.env、ai-company/.env 等）存在但未在掃描範圍內被誤標
- 依最高級別指令：不推送到 GitHub、不做 sed 覆寫（避免破壞運行中設定）
