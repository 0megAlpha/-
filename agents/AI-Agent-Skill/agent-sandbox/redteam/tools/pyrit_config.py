"""PyRIT 紅隊測試配置"""
class RedTeamTester:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = "deepseek-ai/deepseek-v4-flash-0731"
    def build_target(self):
        from pyrit.prompt_target import OpenAIChatTarget
        return OpenAIChatTarget(api_key=self.api_key, endpoint=self.base_url, model_name=self.model)
    def test_jailbreak(self, prompts: list) -> dict:
        from pyrit.orchestrator import PromptSendingOrchestrator
        orch = PromptSendingOrchestrator(prompt_target=self.build_target())
        results = orch.send_prompts(prompts)
        return {"total": len(prompts), "results": results}
