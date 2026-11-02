#!/usr/bin/env python3
"""
把 fleet/agents.json 展開成 fleet/<name>/config.json（每崗位一個檔）。
並把驗證結果（which 找得到 / 端點可達）寫回 config.json。

為什麼要展開？
  · 單一檔在 git diff 時難讀、難單獨交接給某一崗位
  · 各 Agent 的設定可以被單獨 sync 到 ~/.config/<agent>/ 而不互相干擾

用法：
    python3 deploy/gen_fleet.py            # 產生/更新 config.json（不探測）
    python3 deploy/gen_fleet.py --probe    # 同上 + 真實探測 binary/endpoint
    python3 deploy/gen_fleet.py --sync     # 同步到 ~/.config/<agent>/
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "fleet", "agents.json")
OUT = os.path.join(ROOT, "fleet")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def which(binary: str):
    p = shutil.which(binary)
    if p:
        return p
    for d in (os.path.expanduser("~/.local/bin"), os.path.expanduser("~/go/bin"),
              "/usr/local/bin", "/usr/bin", os.path.expanduser("~/.npm-global/bin"),
              os.path.expanduser("~/.bun/bin")):
        cand = os.path.join(d, binary)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    return None


def probe_endpoint(url, timeout=2.0):
    if not url:
        return None
    for suffix in ("/health", "/"):
        try:
            with urllib.request.urlopen(url.rstrip("/") + suffix, timeout=timeout) as r:
                return {"ok": True, "code": r.status}
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return {"ok": True, "code": e.code}
        except Exception as e:
            last = str(e)
    return {"ok": False, "error": locals().get("last", "unreachable")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true", help="真實探測 binary/endpoint")
    ap.add_argument("--sync", action="store_true", help="同步到 ~/.config/<agent>/")
    args = ap.parse_args()

    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    agents = data.get("agents", [])
    print(f"📂 來源：{SRC}（{len(agents)} 個崗位）")

    written = 0
    for a in agents:
        cfg = dict(a)
        cfg["_generated_at"] = now()

        if args.probe:
            bp = which(cfg.get("binary", "")) or which(cfg.get("name", ""))
            cfg["binary_path"] = bp
            cfg["installed"] = bool(bp)
            cfg["endpoint_probe"] = probe_endpoint(cfg.get("endpoint"))
            if bp:
                try:
                    out = subprocess.run([bp, "--version"], capture_output=True,
                                         text=True, timeout=8)
                    cfg["version"] = (out.stdout or out.stderr).strip()[:120] or None
                except Exception:
                    cfg["version"] = None
            print(f"  {'✅' if bp else '❌'} {cfg['name']:<18} "
                  f"{(bp or 'not-found')}"
                  f"{'  endpoint=' + str(cfg['endpoint_probe']) if cfg.get('endpoint') else ''}")

        d = os.path.join(OUT, cfg["name"])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "config.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        written += 1

        if args.sync:
            target = os.path.expanduser(f"~/.config/{cfg['name']}")
            os.makedirs(target, exist_ok=True)
            with open(os.path.join(target, "ai-company.json"), "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 展開 {written} 個 config.json → {OUT}/<name>/config.json")
    if args.sync:
        print("✅ 已同步到 ~/.config/<name>/ai-company.json")
    if not args.probe:
        print("ℹ️  加 --probe 可填入真實 binary_path / installed / endpoint_probe")


if __name__ == "__main__":
    main()