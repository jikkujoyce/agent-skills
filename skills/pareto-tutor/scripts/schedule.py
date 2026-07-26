#!/usr/bin/env python3
"""schedule.py -- tiny SM-2-lite spaced-repetition scheduler over progress.json.

Standard library only; works on Python 3.8+. Used by the pareto-tutor skill to
track which concepts a learner should review and when.

Commands:
  init  --topic "Python" [--file progress.json]
  add   <concept_id> "<display name>" [--file ...]
  due   [--file ...] [--all]
  grade <concept_id> <0-5> [--file ...]
  stats [--file ...]

progress.json schema:
{
  "topic": "Python",
  "created": "2026-07-11",
  "concepts": {
    "dicts": {
      "name": "Dicts and iteration idioms",
      "added": "2026-07-11",
      "ef": 2.5,            # ease factor (SM-2), min 1.3
      "interval": 0,        # days until next review
      "reps": 0,            # consecutive successful reviews
      "due": "2026-07-11",  # next review date (ISO)
      "history": [ {"date": "...", "grade": 4}, ... ]
    }
  }
}
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DEFAULT_FILE = "progress.json"
MIN_EF = 1.3


# ---------- persistence ----------

def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"error: {path} not found. Run `init` first (or check --file).")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"error: {path} is not valid JSON ({e}). Fix or restore it before continuing.")


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def today():
    return date.today()


def iso(d):
    return d.isoformat()


# ---------- commands ----------

def cmd_init(args):
    p = Path(args.file)
    if p.exists() and not args.force:
        sys.exit(f"error: {args.file} already exists (use --force to overwrite).")
    save(args.file, {"topic": args.topic, "created": iso(today()), "concepts": {}})
    print(f"initialized {args.file} for topic: {args.topic}")


def cmd_add(args):
    data = load(args.file)
    cid = args.concept_id
    if cid in data["concepts"] and not args.force:
        sys.exit(f"error: concept '{cid}' already exists (use --force to reset it).")
    data["concepts"][cid] = {
        "name": args.name,
        "added": iso(today()),
        "ef": 2.5,
        "interval": 0,
        "reps": 0,
        "due": iso(today()),  # new concepts are due immediately
        "history": [],
    }
    save(args.file, data)
    print(f"added '{cid}' ({args.name}) -- due today")


def cmd_due(args):
    data = load(args.file)
    t = today()
    rows = []
    for cid, c in data["concepts"].items():
        d = date.fromisoformat(c["due"])
        overdue = (t - d).days
        if args.all or overdue >= 0:
            rows.append((overdue, cid, c))
    if not rows:
        print("nothing due -- schedule is clear. Continue with lesson/project.")
        return
    rows.sort(key=lambda r: (-r[0], r[1]))  # most overdue first
    label = "ALL CONCEPTS" if args.all else f"DUE FOR REVIEW ({len(rows)})"
    print(f"{label} -- {data['topic']}, {iso(t)}")
    for overdue, cid, c in rows:
        status = "new" if not c["history"] else (
            "due today" if overdue == 0 else
            (f"{overdue}d overdue" if overdue > 0 else f"in {-overdue}d")
        )
        print(f"  [{status:>11}] {cid:<24} {c['name']}  (reps={c['reps']}, ivl={c['interval']}d)")
    if not args.all:
        print("\nquiz each with active recall, then: schedule.py grade <concept_id> <0-5>")


def cmd_grade(args):
    if not 0 <= args.grade <= 5:
        sys.exit("error: grade must be an integer 0-5.")
    data = load(args.file)
    c = data["concepts"].get(args.concept_id)
    if c is None:
        known = ", ".join(sorted(data["concepts"])) or "(none)"
        sys.exit(f"error: unknown concept '{args.concept_id}'. Known: {known}")

    q = args.grade
    # SM-2: ease factor adjusts on every review; floor at 1.3.
    c["ef"] = max(MIN_EF, c["ef"] + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    if q >= 3:
        c["reps"] += 1
        if c["reps"] == 1:
            c["interval"] = 1
        elif c["reps"] == 2:
            c["interval"] = 4
        else:
            c["interval"] = max(1, round(c["interval"] * c["ef"]))
    else:
        c["reps"] = 0
        c["interval"] = 1  # lapse: re-climb from the bottom

    c["due"] = iso(today() + timedelta(days=c["interval"]))
    c["history"].append({"date": iso(today()), "grade": q})
    save(args.file, data)
    verdict = "success" if q >= 3 else "lapse -- interval reset"
    print(f"'{args.concept_id}' graded {q} ({verdict}); next review {c['due']} "
          f"(interval {c['interval']}d, ef {c['ef']:.2f})")


def cmd_stats(args):
    data = load(args.file)
    cs = data["concepts"]
    if not cs:
        print(f"{data['topic']}: no concepts tracked yet.")
        return
    t = today()
    due_now = sum(1 for c in cs.values() if date.fromisoformat(c["due"]) <= t)
    mature = sum(1 for c in cs.values() if c["interval"] >= 21)
    reviews = sum(len(c["history"]) for c in cs.values())
    lapses = sum(1 for c in cs.values() for h in c["history"] if h["grade"] < 3)
    grades = [h["grade"] for c in cs.values() for h in c["history"]]
    avg = sum(grades) / len(grades) if grades else 0.0
    print(f"topic: {data['topic']}  (since {data['created']})")
    print(f"  concepts tracked : {len(cs)}")
    print(f"  due now          : {due_now}")
    print(f"  mature (>=21d)   : {mature}")
    print(f"  total reviews    : {reviews}  (lapses: {lapses}, avg grade: {avg:.1f})")
    hard = sorted(cs.items(), key=lambda kv: kv[1]["ef"])[:3]
    if reviews:
        print("  hardest concepts :", ", ".join(f"{k} (ef {v['ef']:.2f})" for k, v in hard))


def main():
    ap = argparse.ArgumentParser(description="SM-2-lite spaced-repetition scheduler")
    ap.add_argument("--file", default=DEFAULT_FILE, help="path to progress.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create a new progress file")
    p.add_argument("--topic", required=True)
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("add", help="track a new concept (due immediately)")
    p.add_argument("concept_id")
    p.add_argument("name")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("due", help="list concepts due for review")
    p.add_argument("--all", action="store_true", help="show every concept, not just due ones")
    p.set_defaults(fn=cmd_due)

    p = sub.add_parser("grade", help="record a review grade (0-5) and reschedule")
    p.add_argument("concept_id")
    p.add_argument("grade", type=int)
    p.set_defaults(fn=cmd_grade)

    p = sub.add_parser("stats", help="progress overview")
    p.set_defaults(fn=cmd_stats)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
