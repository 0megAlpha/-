# Agent Orchestrator Skill

## 用途
管理多個 AI agents（Freebuff, OpenHands, Hermes）並行執行

## 支持 Agent 清單
- Freebuff（快速原型）
- OpenHands（深度開發）
- Hermes SWE-agent（生產部署）
- Kilo Code（架構設計）
- CrewAI（協調層）

## 工作流
```yaml
workflow: "feature-complete"
agents:
  - name: freebuff-spec
    task: "產出完整規格"
    model: claude-opus-4.7
    timeout: 5min

  - name: openhands-dev
    depends_on: freebuff-spec
    task: "完整開發 + 測試"
    timeout: 30min

  - name: hermes-deploy
    depends_on: openhands-dev
    task: "生產部署 + 監控"
    timeout: 10min

checkpoints:
  - after: freebuff-spec
    wait_for: manual_approval
  - after: openhands-dev
    wait_for: ci_pass
```

## 觸發
`freebuff orchestrate <repo> feature-complete`
