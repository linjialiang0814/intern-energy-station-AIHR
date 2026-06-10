"""Initialize SQLite database from CSV seed data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.data_service import clear_data_cache
from services.storage_service import DB_PATH, init_database


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize SQLite database from CSV data.")
    parser.add_argument("--force", action="store_true", help="Recreate database even if it already exists.")
    args = parser.parse_args()

    path = init_database(DB_PATH, force=args.force)
    clear_data_cache()
    print(f"SQLite database ready: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
