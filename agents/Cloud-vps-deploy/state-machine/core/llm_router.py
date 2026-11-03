"""
Multi-Provider LLM Router - 支持所有 Agent 自由选择 API 后端
"""
 
import os
from typing import Optional, Dict, Any
from anthropic import Anthropic as AnthropicClient
import requests
import json
 
class LLMRouter:
    """Router for multiple LLM providers"""
 
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
 
        self.anthropic_client = None
        if self.anthropic_key:
            self.anthropic_client = AnthropicClient(api_key=self.anthropic_key)
 
    def call_llm(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        messages: list = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Call LLM with specified provider"""
 
        # Use defaults if not specified
        provider = provider or os.getenv("DEFAULT_MODEL_PROVIDER", "anthropic")
        model = model or os.getenv("DEFAULT_MODEL", "claude-opus-4-1-20250805")
 
        print(f"🔄 LLM Call: provider={provider}, model={model}")
 
        if provider == "anthropic":
            return self._call_anthropic(model, messages, temperature, max_tokens)
        elif provider == "openai":
            return self._call_openai(model, messages, temperature, max_tokens)
        elif provider == "openrouter":
            return self._call_openrouter(model, messages, temperature, max_tokens)
        else:
            # Fallback to Anthropic
            return self._call_anthropic(model, messages, temperature, max_tokens)
 
    def _call_anthropic(self, model, messages, temperature, max_tokens) -> str:
        """Call Anthropic API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
 
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return response.content[0].text
 
    def _call_openai(self, model, messages, temperature, max_tokens) -> str:
        """Call OpenAI API"""
        if not self.openai_key:
            raise ValueError("OpenAI API key not configured")
 
        import openai
        client = openai.OpenAI(api_key=self.openai_key)
 
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
 
    def _call_openrouter(self, model, messages, temperature, max_tokens) -> str:
        """Call OpenRouter API"""
        if not self.openrouter_key:
            raise ValueError("OpenRouter API key not configured")
 
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
 
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
 
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        return data["choices"][0]["message"]["content"]
 
# Global router instance
_router = None
 
def get_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
 
def call_llm(provider=None, model=None, messages=None, temperature=0.7, max_tokens=2000):
    """Convenience function"""
    return get_router().call_llm(provider, model, messages, temperature, max_tokens)
