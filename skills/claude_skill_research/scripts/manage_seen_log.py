#!/usr/bin/env python3
"""
manage_seen_log.py — Helper for claude_skill_research skill

Usage:
  python manage_seen_log.py init              # Initialize seen_log.json if missing
  python manage_seen_log.py list              # Print all seen URLs
  python manage_seen_log.py check <url>       # Check if a URL has been seen (exit 0=seen, 1=new)
  python manage_seen_log.py add <url> <title> <report_file>   # Add a URL to the seen log
  python manage_seen_log.py stats             # Show stats about the seen log
  python manage_seen_log.py pending           # List URLs marked as skipped (pending next run)
"""

import json
import sys
import os
from datetime import datetime

WORKSPACE = os.environ.get(
    "CLAUDE_WORKSPACE",
    "/sessions/tender-sweet-dijkstra/mnt/claude_cowork"
)
LOG_PATH = os.path.join(WORKSPACE, "skill_research", "seen_log.json")


def load_log():
    """Load or initialize the seen log."""
    if not os.path.exists(LOG_PATH):
        return {"last_run": None, "seen_urls": []}
    try:
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # Backup corrupted file
        bak = LOG_PATH + ".bak"
        if os.path.exists(LOG_PATH):
            os.rename(LOG_PATH, bak)
            print(f"[WARNING] seen_log.json was corrupted. Backed up to {bak}. Starting fresh.", file=sys.stderr)
        return {"last_run": None, "seen_urls": []}


def save_log(data):
    """Save the seen log to disk."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)


def cmd_init():
    if not os.path.exists(LOG_PATH):
        save_log({"last_run": None, "seen_urls": []})
        print(f"Initialized: {LOG_PATH}")
    else:
        print(f"Already exists: {LOG_PATH}")


def cmd_list():
    data = load_log()
    urls = data.get("seen_urls", [])
    if not urls:
        print("No URLs seen yet.")
        return
    for entry in urls:
        skipped = " [PENDING]" if entry.get("skipped") else ""
        print(f"  {entry['date_seen']}  {entry['url']}{skipped}")
    print(f"\nTotal: {len(urls)} URLs | Last run: {data.get('last_run', 'never')}")


def cmd_check(url):
    data = load_log()
    seen = {e["url"] for e in data.get("seen_urls", [])}
    if url in seen:
        print("SEEN")
        sys.exit(0)
    else:
        print("NEW")
        sys.exit(1)


def cmd_add(url, title, report_file, skipped=False):
    data = load_log()
    seen_urls = data.get("seen_urls", [])
    existing = {e["url"] for e in seen_urls}
    if url in existing:
        print(f"Already in log: {url}")
        return
    entry = {
        "url": url,
        "title": title,
        "date_seen": datetime.now().strftime("%Y-%m-%d"),
        "report_file": report_file,
    }
    if skipped:
        entry["skipped"] = True
    seen_urls.append(entry)
    data["seen_urls"] = seen_urls
    data["last_run"] = datetime.now().isoformat(timespec="seconds")
    save_log(data)
    print(f"Added: {url}")


def cmd_stats():
    data = load_log()
    urls = data.get("seen_urls", [])
    pending = [e for e in urls if e.get("skipped")]
    processed = [e for e in urls if not e.get("skipped")]
    print(f"Total seen:     {len(urls)}")
    print(f"  Processed:    {len(processed)}")
    print(f"  Pending:      {len(pending)}")
    print(f"Last run:       {data.get('last_run', 'never')}")


def cmd_pending():
    data = load_log()
    pending = [e for e in data.get("seen_urls", []) if e.get("skipped")]
    if not pending:
        print("No pending URLs.")
        return
    for entry in pending:
        print(f"  {entry['date_seen']}  {entry['url']}  ({entry.get('title', 'no title')})")
    print(f"\nTotal pending: {len(pending)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "list":
        cmd_list()
    elif cmd == "check":
        if len(sys.argv) < 3:
            print("Usage: manage_seen_log.py check <url>")
            sys.exit(2)
        cmd_check(sys.argv[2])
    elif cmd == "add":
        if len(sys.argv) < 5:
            print("Usage: manage_seen_log.py add <url> <title> <report_file>")
            sys.exit(2)
        cmd_add(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "pending":
        cmd_pending()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
