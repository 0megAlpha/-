from dataclasses import dataclass
@dataclass(frozen=True)
class PipelineAgent:
    id: str; name_zh: str; model: str; system_prompt: str; output_artifact: str
PIPELINE_AGENTS={}
def _r(i,n,m,p,o): PIPELINE_AGENTS[i]=PipelineAgent(i,n,m,p,o)
_r("ceo","01 CEO","claude-sonnet","你是策略決策核心。輸入使用者需求，輸出：目標與限制、優先序、分配給哪些下游Agent。","ceo_decision.md")
_r("product","02 Product","claude-sonnet","你是產品經理。輸入CEO決策，輸出PRD：需求分析、用戶故事、驗收標準。","PRD.md")
_r("architect","03 Architect","claude-sonnet","你是架構師。輸入PRD，輸出：系統架構、技術選型、模組劃分、API設計、資料庫設計。","architecture.md")
_r("research","04 Research","gpt-4o","你是技術調研員。輸入架構，輸出：可行性、第三方套件、風險評估、成本估算。","research.md")
_r("coder","05 Coder","qwen3-coder","你是全端工程師。輸入架構與調研，輸出完整可執行程式碼（前後端+資料庫+單元測試）。","source_code.md")
_r("reviewer","06 Reviewer","deepseek-r1","你是程式碼審查員。輸出審查報告，結尾標註 STATUS: PASS 或 STATUS: FAIL。","review_report.md")
_r("qa","07 QA","deepseek-r1","你是測試工程師。輸出測試報告，結尾標註 STATUS: PASS 或 STATUS: FAIL 並說明原因。","test_report.md")
_r("devops","08 DevOps","deepseek-r1","你是運維。輸出CI/CD、Dockerfile、docker-compose.yml、部署策略。","deploy_config.md")
_r("ops","09 Ops","deepseek-r1","你是運營監控員。輸出監控儀表板、告警規則、日誌分析策略。","monitoring_dashboard.md")
_r("release","10 Release","claude-sonnet","你是發布管理員。輸出版本紀錄、發布計畫、回滾準備。","release_notes.md")
_r("documentation","11 Documentation","gpt-4o","你是文件工程師。輸出用戶文檔、API文檔、操作手冊（繁體中文）。","user_guide.md")
assert len(PIPELINE_AGENTS)==11
