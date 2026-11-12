from __future__ import annotations

import argparse
import json
import os

from dotenv import load_dotenv

from .graph import run_task
from .openhands_client import OpenHandsClient


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Xiaye Agent OS planning/review loop")
    parser.add_argument("task", help="Natural-language engineering task")
    parser.add_argument("--send-to-openhands", action="store_true", help="Create and start an OpenHands conversation after planning/review")
    parser.add_argument("--repository", help="Optional Git repository URL for OpenHands")
    parser.add_argument("--branch", help="Optional repository branch for OpenHands")
    args = parser.parse_args()
    result = run_task(args.task)
    if args.send_to_openhands:
        client = OpenHandsClient(os.getenv("OPENHANDS_BASE_URL", "http://127.0.0.1:13000"))
        try:
            created = client.create_conversation(result["implementation_brief"], repository=args.repository, selected_branch=args.branch)
            started = client.start_conversation(created["conversation_id"])
            result["openhands"] = {"created": created, "started": started}
        finally:
            client.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
