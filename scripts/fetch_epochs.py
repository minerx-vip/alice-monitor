#!/usr/bin/env python3
"""Fetch Alice Protocol epoch data and merge into data/epochs.json.

Run by GitHub Actions on a cron schedule. Stdlib only.
"""

import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

API_LIMIT = 50
API_URL = f"https://aliceprotocol.org/api/indexer/epochs?limit={API_LIMIT}"
# Retention: keep up to last N epochs in the committed JSON. 200 ≈ ~7d at
# ~50min/epoch. Trim so the repo doesn't grow unbounded.
RETAIN_EPOCHS = 200

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "epochs.json"


def fetch() -> list[dict]:
    req = Request(API_URL, headers={"User-Agent": "AliceMonitorPublic/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def load_existing() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text()).get("epochs", [])
    except Exception:
        return []


def merge(cached: list[dict], fresh: list[dict]) -> list[dict]:
    by_id = {}
    for ep in cached:
        by_id[int(ep.get("epoch", 0))] = ep
    for ep in fresh:
        by_id[int(ep.get("epoch", 0))] = ep
    ordered = sorted(by_id.values(), key=lambda e: int(e.get("epoch", 0)), reverse=True)
    return ordered[:RETAIN_EPOCHS]


def main() -> int:
    try:
        fresh = fetch()
    except Exception as e:
        print(f"[fetch] API error: {e}", file=sys.stderr)
        return 1
    cached = load_existing()
    merged = merge(cached, fresh)
    payload = {"updated": int(time.time()), "epochs": merged}
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"[fetch] ok · {len(fresh)} fresh · {len(merged)} retained")
    return 0


if __name__ == "__main__":
    sys.exit(main())
