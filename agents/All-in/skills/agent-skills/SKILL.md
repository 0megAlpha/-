---
name: agent-skills
description: 技能與 references 分離；一包多 Agent；技能要有擁有者；from output to delivery。
version: "1.0.0"
owner: "Ai-agent-skill"
---
# 原則
- one pack many agents：同一技能包可掛到 Hermes / OpenCode / Kilo / Crush 等
- skills need ownership：每個技能都有維護者與版本號（frontmatter 標註）
- 共享 references 不隨單一技能帶入，統一放 ~/.agents/references/
- 流程配合團隊實況更新，以目前實際部署狀態為準（舊文件僅作歷史參考）
- from output to delivery：產出必須走到可交付（測試、文檔、部署、驗證）
