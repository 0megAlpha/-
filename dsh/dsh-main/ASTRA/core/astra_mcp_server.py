#!/usr/bin/env python3
"""
ASTRA MCP Server — 零第三方依赖，纯 stdlib。
Protocol: JSON-RPC 2.0 over stdio, newline-delimited (MCP 2024-11-05)
"""
import sys, os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for p in (_ROOT, _HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

# --- 导入 core，路径两种都兜底 ---
try:
    from core import AstraCore
    from core.outbound_cloaker import OutboundCloaker
except ImportError:
    from astra_core import AstraCore
    from outbound_cloaker import OutboundCloaker

_core = AstraCore()

TOOLS = [
    {
        "name": "astra_pipeline",
        "description": "跑一次 ASTRA 全栈 pipeline：任务切分 + 关键词编织 + 编码 + debug 包装。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "原始任务字符串"},
                "keywords": {"type": "array", "items": {"type": "string"},
                             "description": "可选注入关键词"},
            },
            "required": ["task"],
        },
    },
    {
        "name": "astra_health",
        "description": "回传 ASTRA 版本与已载入模块清单。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "astra_encode",
        "description": "单次 base64 / hex 编码。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payload": {"type": "string"},
                "mode": {"type": "string", "enum": ["base64", "hex"]},
            },
            "required": ["payload"],
        },
    },
]


def _call_tool(name, args):
    if name == "astra_pipeline":
        return json.dumps(_core.pipeline(args.get("task", ""),
                                         args.get("keywords") or []),
                          ensure_ascii=False)
    if name == "astra_health":
        return json.dumps(_core.health(), ensure_ascii=False)
    if name == "astra_encode":
        return OutboundCloaker(mode=args.get("mode", "base64")).encode(
            args.get("payload", ""))
    raise ValueError(f"unknown tool: {name}")


def _send(msg):
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _handle(req):
    method = req.get("method")
    rid = req.get("id")
    params = req.get("params") or {}

    # 通知（无 id）不回
    if rid is None and method and method.startswith("notifications/"):
        return None

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "astra", "version": "5.2.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            text = _call_tool(name, args)
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": text}]}}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": f"ERROR: {e}"}],
                "isError": True}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}

    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": f"method not found: {method}"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            _send({"jsonrpc": "2.0", "id": None,
                   "error": {"code": -32700, "message": str(e)}})
            continue
        resp = _handle(req)
        if resp is not None:
            _send(resp)


if __name__ == "__main__":
    main()
