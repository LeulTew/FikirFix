import os
import json
from datetime import datetime, timezone


LOG_DIR = os.path.expanduser("~/.fikirfix/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "tool_calls.log")


def log_tool_call(tool_name: str, args: dict, result: object):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tool": tool_name,
        "args": args,
        "result_repr": str(result)[:4000],
    }
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # Do not crash the agent for logging failures
        pass
