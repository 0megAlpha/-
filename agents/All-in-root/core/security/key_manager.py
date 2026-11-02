#!/usr/bin/env python3
"""憑證管理 + 去敏 + 推送前密鑰掃描（gitleaks 缺席時的陽春替代品）。

用法：
  python3 core/security/key_manager.py scan .   # 掃描整個 repo（只印檔案:行號:類型，永不印出密鑰本體）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{16,}", "OpenAI 風格 Key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub PAT"),
    (r"gh[oaur]_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "私鑰區塊"),
    (r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{20,}", "疑似憑證賦值"),
]
SKIP_DIRS = {".git", "node_modules", "venv", "__pycache__", ".hermes"}


def redact(text: str) -> str:
    """日誌輸出去敏：把疑似密鑰換成 [REDACTED]。"""
    out = text
    for pat, _ in SECRET_PATTERNS:
        out = re.sub(pat, "[REDACTED]", out)
    return out


def scan(root: Path):
    hits = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(p in SKIP_DIRS for p in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat, kind in SECRET_PATTERNS:
                if re.search(pat, line):
                    hits.append((str(path), lineno, kind))
    return hits


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        print("用法: key_manager.py scan <path>")
        return 2
    hits = scan(Path(sys.argv[2]))
    for f, line, kind in hits:
        print(f"❌ {f}:{line} → {kind}")
    if hits:
        print(f"共 {len(hits)} 處疑似密鑰：請改用環境變數注入，嚴禁推送。")
        return 1
    print("✅ 未發現疑似密鑰。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
