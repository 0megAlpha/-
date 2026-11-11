from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from .graph import run_task


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Xiaye Agent OS planning/review loop")
    parser.add_argument("task", help="Natural-language engineering task")
    args = parser.parse_args()
    print(json.dumps(run_task(args.task), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
