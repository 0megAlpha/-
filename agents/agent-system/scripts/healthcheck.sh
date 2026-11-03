#!/usr/bin/env bash
# 健康檢查（只檢查本機 localhost，不輸出任何真實位址）
echo "== LiteLLM 閘道 =="
curl -s -o /dev/null -w "  localhost:4000 -> %{http_code}\n" --max-time 5 http://localhost:4000/ || echo "  4000 無回應"
echo "== Agent 模組 import 測試 =="
cd "$(dirname "$0")/.."
python3 -c "
import sys; sys.path.insert(0, '.')
from agents.researcher import ResearcherAgent
from agents.scraper import ScraperAgent
from agents.processor import ProcessorAgent
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.verifier import VerifierAgent
from agents.memory import MemoryAgent
from agents.notifier import NotifierAgent
print('  8 個 Agent 全部 import OK')
"
