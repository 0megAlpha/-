"""
ScraperAgent — 網頁抓取與解析 Agent。

安全：僅抓取 SEARCH_API_URL 回傳或白名單（ALLOWED_SCRAPE_DOMAINS）內的網址；
不抓取內部服務位址；不輸出 cookies / headers。
"""
import os
import json
import re
from html.parser import HTMLParser
from typing import Any, Dict, List
from urllib.parse import urlparse

from agents.base_agent import BaseAgent


class _TextExtractor(HTMLParser):
    """純 stdlib 的 HTML 文字抽取。"""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: List[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def text(self, max_chars: int = 8000) -> str:
        return " ".join(self._chunks)[:max_chars]


class ScraperAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("scraper", **kwargs)
        allowed = os.getenv("ALLOWED_SCRAPE_DOMAINS", "example.com")
        self.allowed_domains = {d.strip().lower() for d in allowed.split(",") if d.strip()}

    def _allowed(self, url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        if host in ("localhost", "127.0.0.1", "0.0.0.0"):
            return False  # 絕不抓取內部服務
        return any(host == d or host.endswith("." + d) for d in self.allowed_domains)

    def _fetch_text(self, url: str) -> str:
        if self.mock:
            self.log.info("[mock] 抓取略過: %s", url)
            return f"<html><body><p>mock content for {url}</p></body></html>"
        import requests
        resp = requests.get(url, timeout=30, headers={"User-Agent": "agent-system/1.0"})
        resp.raise_for_status()
        return resp.text

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        urls: list = input_data.get("urls") or []
        raw_text: str = input_data.get("raw", "") or ""
        # 支援從 research result 的字串自動提取 URL
        if not urls and raw_text:
            urls = re.findall(r"https?://[^\s\"']+", raw_text)
        texts: list = []
        for url in urls[:5]:
            if not self._allowed(url):
                self.log.warning("跳過非白名單網址: %s", url)
                continue
            try:
                html = self._fetch_text(url)
                parser = _TextExtractor()
                parser.feed(html)
                texts.append({"url": url, "text": parser.text()})
            except Exception as exc:  # noqa: BLE001
                self.log.warning("抓取失敗 %s: %s", url, self.redact(str(exc)))
        return {"result": json.dumps(texts, ensure_ascii=False), "data": texts}
