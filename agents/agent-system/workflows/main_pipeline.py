"""
main_pipeline — Agent 工作流主控調度器。

功能：
- 讀取 config/settings.json 的 pipelines 定義
- 依序執行 stages，支援資料鏈接（上一階段輸出 → 下一階段輸入）
- 支援平行階段（parallel: [stage_ids]）
- 執行結果寫入 workflows/data/（gitignore 排除）
- --mock 讓整個流程在無真實金鑰下可驗證

用法：
  python3 workflows/main_pipeline.py --pipeline default --query "範例任務"
  python3 workflows/main_pipeline.py --pipeline default --mock --dry-run
"""
import os
import sys
import json
import argparse
import importlib
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

# 讓 agents/ 可被 import（從 repo 根目錄執行）
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agents.base_agent import BaseAgent  # noqa: E402


def load_config() -> Dict[str, Any]:
    cfg_path = os.path.join(ROOT, "config", "settings.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def instantiate_agent(cfg: Dict[str, Any], agent_id: str) -> BaseAgent:
    module_name, class_name = cfg["agents"][agent_id]["class"].split(".")
    module = importlib.import_module(f"agents.{module_name}")
    cls = getattr(module, class_name)
    return cls()


def resolve_input(value: Any, results: Dict[str, Dict[str, Any]], initial: Dict[str, Any]) -> Any:
    """把 'stage.key' 形式引用解析為前一階段輸出的欄位。"""
    if isinstance(value, str) and value.startswith("pipeline."):
        return initial.get(value.split(".", 1)[1])
    if isinstance(value, str) and "." in value and not value.startswith(("http", "/")):
        stage_id, _, key = value.partition(".")
        if stage_id in results and key in results[stage_id]:
            return results[stage_id][key]
    return value


def run_stage(cfg: Dict[str, Any], stage: Dict[str, Any],
              results: Dict[str, Dict[str, Any]], initial: Dict[str, Any]) -> Dict[str, Any]:
    agent = instantiate_agent(cfg, stage["agent"])
    inputs = {k: resolve_input(v, results, initial) for k, v in stage.get("inputs", {}).items()}
    # 任務包裝：task_xxx 函式
    task_name = stage.get("task")
    if task_name:
        task_mod = importlib.import_module(f"workflows.tasks.{task_name}")
        return task_mod.run(agent, inputs)
    return agent.run(inputs)


def run_pipeline(pipeline_name: str, initial: Dict[str, Any], mock: bool = False,
                 dry_run: bool = False) -> Dict[str, Any]:
    if mock:
        os.environ["MOCK_LLM"] = "1"
    cfg = load_config()
    pipeline = cfg["pipelines"][pipeline_name]
    stages: List[Dict[str, Any]] = pipeline["stages"]
    results: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []
    print(f"== 管線: {pipeline_name} — {pipeline.get('description','')}")
    print(f"== mock={mock} dry_run={dry_run}")

    def _exec_stage(stage: Dict[str, Any]) -> None:
        print(f"  ▶ stage [{stage['id']}] agent={stage['agent']}")
        if dry_run:
            results[stage["id"]] = {"_dry_run": True}
            order.append(stage["id"])
            return
        results[stage["id"]] = run_stage(cfg, stage, results, initial)
        order.append(stage["id"])

    for stage in stages:
        if "parallel" in stage:
            ids = stage["parallel"]
            with ThreadPoolExecutor(max_workers=len(ids)) as pool:
                futures = {pool.submit(_exec_stage, s): s for s in stages if s["id"] in ids}
                for fut in as_completed(futures):
                    fut.result()
        else:
            _exec_stage(stage)

    # 存檔（gitignore 排除）
    os.makedirs(os.path.join(ROOT, "workflows", "data"), exist_ok=True)
    ts = os.environ.get("RUN_TIMESTAMP", "")
    if not ts:
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    artifact = os.path.join(ROOT, "workflows", "data", f"run-{pipeline_name}-{ts}.json")
    with open(artifact, "w", encoding="utf-8") as f:
        json.dump({"pipeline": pipeline_name, "order": order, "results": results},
                  f, ensure_ascii=False, indent=2)
    print(f"== 完成, 執行順序: {' -> '.join(order)}")
    print(f"== 產物: {artifact}")
    return {"order": order, "results": results, "artifact": artifact}


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent 工作流主控調度器")
    parser.add_argument("--pipeline", default="default", help="settings.json 中的管線名稱")
    parser.add_argument("--query", default="範例任務", help="初始輸入 query")
    parser.add_argument("--mock", action="store_true", help="mock 模式（不需真實金鑰）")
    parser.add_argument("--dry-run", action="store_true", help="只印 stage 不執行")
    args = parser.parse_args()
    try:
        run_pipeline(args.pipeline, {"query": args.query, "objective": args.query},
                     mock=args.mock, dry_run=args.dry_run)
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
