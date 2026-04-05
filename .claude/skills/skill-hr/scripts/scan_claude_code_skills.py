#!/usr/bin/env python3
"""Scan on-disk Claude Code-style skill trees and print JSON for P02 / audits.

Discovers directories ``.../.claude/skills/<name>/SKILL.md`` under a workspace
(and optionally ``~/.claude/skills``). Parses a minimal subset of YAML frontmatter
(single-line keys; multiline values may be truncated).

**Limitation:** Skills that exist only inside Claude Code **plugins** are not
reliably visible on disk as normal folders. Merge this output with plugin /
slash-menu listings per ``references/hosts/claude-code.md``.

Example::

    python packages/skill-hr/scripts/scan_claude_code_skills.py . --include-user
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterator

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        "target",
        ".tox",
    }
)


def parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    if not raw.startswith("---"):
        return {}
    rest = raw[3:]
    end = rest.find("\n---")
    if end == -1:
        return {}
    block = rest[:end]
    data: dict[str, Any] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        if key == "name":
            data["name"] = val
        elif key == "description":
            data["description"] = val
        elif key == "disable-model-invocation":
            data["disable_model_invocation"] = val.lower() == "true"
        elif key == "user-invocable":
            data["user_invocable"] = val.lower() != "false"
        elif key == "paths":
            data["paths"] = val
        elif key == "context":
            data["context"] = val
    if "user_invocable" not in data:
        data["user_invocable"] = True
    if "disable_model_invocation" not in data:
        data["disable_model_invocation"] = False
    return data


def iter_skill_dirs_under_skills_root(skills_root: Path) -> Iterator[Path]:
    if not skills_root.is_dir():
        return
    for child in sorted(skills_root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            yield child


def walk_claude_skill_dirs(workspace: Path, max_depth: int) -> Iterator[Path]:
    workspace = workspace.resolve()
    for root, dirnames, _files in os.walk(workspace, topdown=True):
        root_path = Path(root)
        try:
            rel = root_path.relative_to(workspace)
        except ValueError:
            continue
        depth = len(rel.parts)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        if depth >= max_depth:
            dirnames[:] = []
            continue
        if root_path.name == "skills" and root_path.parent.name == ".claude":
            yield from iter_skill_dirs_under_skills_root(root_path)


def classify_source(skill_dir: Path, workspace: Path, user_skills_root: Path) -> str:
    ws = workspace.resolve()
    ud = user_skills_root.resolve()
    try:
        rel = skill_dir.resolve().relative_to(ws)
    except ValueError:
        if skill_dir.resolve().parent == ud:
            return "user"
        return "unknown"
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == ".claude" and parts[1] == "skills":
        if len(parts) == 3:
            return "project"
        return "nested"
    return "nested"


def scan_skill_dir(skill_dir: Path, workspace: Path, user_skills_root: Path) -> dict[str, Any]:
    fm = parse_frontmatter(skill_dir / "SKILL.md")
    name = fm.get("name") or skill_dir.name
    return {
        "skill_id": str(name),
        "skill_dir": str(skill_dir.resolve()),
        "source_guess": classify_source(skill_dir, workspace, user_skills_root),
        "description": fm.get("description", ""),
        "disable_model_invocation": fm.get("disable_model_invocation", False),
        "user_invocable": fm.get("user_invocable", True),
        "paths": fm.get("paths"),
        "context": fm.get("context"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        type=Path,
        help="Workspace root to scan for **/.claude/skills/",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=14,
        metavar="N",
        help="Max directory depth from workspace for os.walk (default: 14)",
    )
    parser.add_argument(
        "--include-user",
        action="store_true",
        help="Also scan user-level skills (~/.claude/skills; %USERPROFILE%\\.claude\\skills on Windows)",
    )
    parser.add_argument(
        "--additional-dir",
        action="append",
        type=Path,
        default=[],
        metavar="DIR",
        help="Extra directory (simulates --add-dir); scans DIR/.claude/skills and nested trees",
    )
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"Not a directory: {workspace}", file=sys.stderr)
        return 2

    user_skills = Path.home() / ".claude" / "skills"

    seen: set[Path] = set()
    records: list[dict[str, Any]] = []

    def add_from_tree(root: Path, max_depth: int) -> None:
        for skill_dir in walk_claude_skill_dirs(root, max_depth):
            resolved = skill_dir.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            records.append(scan_skill_dir(skill_dir, workspace, user_skills))

    add_from_tree(workspace, args.max_depth)
    for extra in args.additional_dir:
        if extra.is_dir():
            add_from_tree(extra.resolve(), args.max_depth)

    if args.include_user:
        for skill_dir in iter_skill_dirs_under_skills_root(user_skills):
            resolved = skill_dir.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            records.append(scan_skill_dir(skill_dir, workspace, user_skills))

    json.dump(records, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
