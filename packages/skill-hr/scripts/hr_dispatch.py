#!/usr/bin/env python3
"""HR task board: state machine + audit log for multi-agent skill-hr workflows.

Stores data under workspace `.skill-hr/hr_tasks.json`. Use this CLI instead of
hand-editing the file (see agents/GLOBAL.md).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TASKS_FILE = "hr_tasks.json"
DEFAULT_STATE = "Intake"

# Valid task states (see references/06-state-and-artifacts.md)
STATES = frozenset(
    {
        "Intake",
        "JDReady",
        "Matching",
        "Matched",
        "Recruiting",
        "Vetting",
        "Delegated",
        "InProgress",
        "Debrief",
        "Closed",
        "Probation",
        "Terminated",
        "Escalation",
    }
)

# Directed edges: from_state -> allowed to_states
_VALID_TRANSITIONS: dict[str, frozenset[str]] = {
    "Intake": frozenset({"JDReady", "Escalation"}),
    "JDReady": frozenset({"Matching", "Escalation"}),
    "Matching": frozenset({"Matched", "Recruiting", "Escalation"}),
    "Recruiting": frozenset({"Vetting", "Escalation"}),
    "Vetting": frozenset({"Matched", "Recruiting", "Escalation"}),
    "Matched": frozenset({"Delegated", "Escalation"}),
    "Delegated": frozenset({"InProgress", "Escalation"}),
    "InProgress": frozenset({"Debrief", "Escalation"}),
    "Debrief": frozenset({"Closed", "Probation", "Escalation"}),
    "Probation": frozenset({"Terminated", "Debrief", "Matching", "Escalation"}),
    "Escalation": frozenset({"Closed", "Recruiting", "Matching"}),
    "Closed": frozenset(),
    "Terminated": frozenset(),
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_workspace_root(start: Path | None = None, *, ensure: bool = False) -> Path:
    """Walk upward from start (or cwd) for a directory containing `.skill-hr`.

    If ``ensure`` is True and no `.skill-hr` exists, create ``./.skill-hr`` under cwd.
    """
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / ".skill-hr").is_dir():
            return p
    if ensure:
        d = cur / ".skill-hr"
        d.mkdir(parents=True, exist_ok=True)
        return cur
    raise FileNotFoundError(
        "Could not find `.skill-hr/` in cwd or parents. "
        "Create `.skill-hr/` at the workspace root or run from that repo."
    )


def tasks_path(root: Path) -> Path:
    return root / ".skill-hr" / TASKS_FILE


def load_doc(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "skill_hr_tasks_version": "1.0.0",
            "updated_at": _utc_now_iso(),
            "tasks": [],
        }
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    if "tasks" not in data or not isinstance(data["tasks"], list):
        data["tasks"] = []
    return data


def save_doc(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _utc_now_iso()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_task(tasks: list[dict[str, Any]], task_id: str) -> dict[str, Any]:
    for t in tasks:
        if t.get("id") == task_id:
            return t
    raise KeyError(f"Unknown task id: {task_id}")


def ensure_task_shape(t: dict[str, Any]) -> None:
    t.setdefault("flow_log", [])
    t.setdefault("progress_log", [])
    if not isinstance(t["flow_log"], list):
        t["flow_log"] = []
    if not isinstance(t["progress_log"], list):
        t["progress_log"] = []


def cmd_create(args: argparse.Namespace) -> int:
    root = find_workspace_root(ensure=True)
    path = tasks_path(root)
    doc = load_doc(path)
    tasks: list[dict[str, Any]] = doc["tasks"]
    tid = args.id
    if any(t.get("id") == tid for t in tasks):
        print(f"Error: task id already exists: {tid}", file=sys.stderr)
        return 1
    state = args.state or DEFAULT_STATE
    if state not in STATES:
        print(f"Error: invalid state: {state}", file=sys.stderr)
        return 1
    now = _utc_now_iso()
    task = {
        "id": tid,
        "title": args.title,
        "state": state,
        "created_at": now,
        "updated_at": now,
        "current_agent": "hr-director",
        "flow_log": [],
        "progress_log": [],
    }
    tasks.append(task)
    save_doc(path, doc)
    print(f"Created {tid} state={state} at {path}")
    return 0


def cmd_state(args: argparse.Namespace) -> int:
    root = find_workspace_root()
    path = tasks_path(root)
    doc = load_doc(path)
    tasks = doc["tasks"]
    try:
        t = get_task(tasks, args.id)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1
    ensure_task_shape(t)
    new_state = args.new_state
    if new_state not in STATES:
        print(f"Error: invalid state: {new_state}", file=sys.stderr)
        return 1
    old = t.get("state", DEFAULT_STATE)
    allowed = _VALID_TRANSITIONS.get(old, frozenset())
    if new_state not in allowed and old != new_state:
        print(
            f"Error: illegal transition {old!r} -> {new_state!r}. "
            f"Allowed: {sorted(allowed)}",
            file=sys.stderr,
        )
        return 1
    t["state"] = new_state
    t["updated_at"] = _utc_now_iso()
    if args.note:
        t.setdefault("state_notes", []).append(
            {"ts": _utc_now_iso(), "state": new_state, "note": args.note}
        )
    save_doc(path, doc)
    print(f"{args.id}: {old} -> {new_state}")
    return 0


def cmd_flow(args: argparse.Namespace) -> int:
    root = find_workspace_root()
    path = tasks_path(root)
    doc = load_doc(path)
    try:
        t = get_task(doc["tasks"], args.id)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1
    ensure_task_shape(t)
    entry = {
        "ts": _utc_now_iso(),
        "from_agent": args.from_agent,
        "to_agent": args.to_agent,
        "remark": args.remark,
    }
    t["flow_log"].append(entry)
    t["updated_at"] = _utc_now_iso()
    t["current_agent"] = args.to_agent
    save_doc(path, doc)
    print(f"{args.id}: flow {args.from_agent} -> {args.to_agent}")
    return 0


def cmd_progress(args: argparse.Namespace) -> int:
    root = find_workspace_root()
    path = tasks_path(root)
    doc = load_doc(path)
    try:
        t = get_task(doc["tasks"], args.id)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1
    ensure_task_shape(t)
    entry = {
        "ts": _utc_now_iso(),
        "current_work": args.current,
        "plan": args.plan,
    }
    t["progress_log"].append(entry)
    t["updated_at"] = _utc_now_iso()
    save_doc(path, doc)
    print(f"{args.id}: progress logged")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = find_workspace_root()
    path = tasks_path(root)
    doc = load_doc(path)
    try:
        t = get_task(doc["tasks"], args.id)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1
    print(json.dumps(t, indent=2, ensure_ascii=False))
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    root = find_workspace_root()
    path = tasks_path(root)
    doc = load_doc(path)
    for t in doc["tasks"]:
        print(f"{t.get('id')}\t{t.get('state')}\t{t.get('title', '')[:60]}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Skill HR task dispatch / state machine")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="Create a new HR task")
    p_create.add_argument("id", help="Task id e.g. HR-20260405-001")
    p_create.add_argument("title", help="Short title")
    p_create.add_argument(
        "state",
        nargs="?",
        default=DEFAULT_STATE,
        help=f"Initial state (default {DEFAULT_STATE})",
    )
    p_create.set_defaults(func=cmd_create)

    p_state = sub.add_parser("state", help="Transition task state")
    p_state.add_argument("id")
    p_state.add_argument("new_state")
    p_state.add_argument("note", nargs="?", default="", help="Optional note for audit")
    p_state.set_defaults(func=cmd_state)

    p_flow = sub.add_parser("flow", help="Append handoff between agents")
    p_flow.add_argument("id")
    p_flow.add_argument("from_agent")
    p_flow.add_argument("to_agent")
    p_flow.add_argument("remark")
    p_flow.set_defaults(func=cmd_flow)

    p_prog = sub.add_parser("progress", help="Append progress snapshot")
    p_prog.add_argument("id")
    p_prog.add_argument("current")
    p_prog.add_argument("plan")
    p_prog.set_defaults(func=cmd_progress)

    p_show = sub.add_parser("show", help="Print task JSON")
    p_show.add_argument("id")
    p_show.set_defaults(func=cmd_show)

    p_list = sub.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=cmd_list)

    args = p.parse_args()
    try:
        return int(args.func(args))
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2
    except (ValueError, KeyError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
