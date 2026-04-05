#!/usr/bin/env python3
"""Validate .skill-hr/registry.json against the skill-hr schema (lightweight)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from registry_runtime import load_registry

REQUIRED_TOP = ("skill_hr_version", "updated_at", "skills", "matching")
REQUIRED_SKILL = ("id", "name", "status", "added_at", "tasks_total", "tasks_success", "tasks_fail")
REQUIRED_EMPLOYEE = (
    "id",
    "name",
    "status",
    "skills",
    "primary_skill",
    "host",
    "created_by",
    "added_at",
    "performance",
    "training_history",
)
ALLOWED_STATUS = frozenset({"active", "on_probation", "terminated", "frozen"})
ALLOWED_CC_SCOPE = frozenset({"user", "project", "nested", "plugin", "unknown"})
ALLOWED_CC_INVOKE = frozenset({"auto", "manual_only"})
REQUIRED_MATCHING = ("delegate_min_score", "confirm_band_min", "max_trials_per_task_per_skill")
ALLOWED_HOST = frozenset({"claude-code", "cursor", "openclaw", "unknown"})
ALLOWED_CREATED_BY = frozenset({"recruited", "trained", "migrated"})


def soul_path_warnings(data: Any, registry_path: Path) -> list[str]:
    """If registry lives at `<workspace>/.skill-hr/registry.json`, warn when soul_path files are missing.

    Non-fatal: CI or fresh checkouts may not have created employee SOUL files yet.
    """
    if registry_path.parent.name != ".skill-hr":
        return []
    workspace_root = registry_path.parent.parent
    employees = data.get("employees")
    if not isinstance(employees, list):
        return []
    out: list[str] = []
    for i, employee in enumerate(employees):
        if not isinstance(employee, dict):
            continue
        sp = employee.get("soul_path")
        if not isinstance(sp, str) or not sp.strip():
            continue
        rel = sp.strip().replace("\\", "/")
        # workspace-relative path as stored in registry
        candidate = (workspace_root / rel).resolve()
        if not candidate.is_file():
            eid = employee.get("id", f"[{i}]")
            out.append(
                f"WARN: employees[{i}] id={eid!r} soul_path {sp!r} not found at {candidate}"
            )
    return out


def err(msg: str) -> None:
    print(msg, file=sys.stderr)


def validate(data: Any, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{path}: root must be an object"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"{path}: missing top-level key '{key}'")

    if "matching" in data and isinstance(data["matching"], dict):
        m = data["matching"]
        for k in REQUIRED_MATCHING:
            if k not in m:
                errors.append(f"{path}.matching: missing '{k}'")
            elif not isinstance(m[k], int):
                errors.append(f"{path}.matching.{k}: must be integer")
        if "delegate_min_score" in m and "confirm_band_min" in m:
            if m["confirm_band_min"] > m["delegate_min_score"]:
                errors.append(
                    f"{path}.matching: confirm_band_min should be <= delegate_min_score"
                )
    elif "matching" in data:
        errors.append(f"{path}.matching: must be an object")

    skills = data.get("skills")
    if not isinstance(skills, list):
        errors.append(f"{path}: 'skills' must be an array")
        return errors

    seen: set[str] = set()
    skill_ids: set[str] = set()
    for i, s in enumerate(skills):
        p = f"{path}.skills[{i}]"
        if not isinstance(s, dict):
            errors.append(f"{p}: must be an object")
            continue
        for k in REQUIRED_SKILL:
            if k not in s:
                errors.append(f"{p}: missing '{k}'")
        sid = s.get("id")
        if isinstance(sid, str):
            if sid in seen:
                errors.append(f"{p}.id: duplicate id '{sid}'")
            seen.add(sid)
            skill_ids.add(sid)
        st = s.get("status")
        if st not in ALLOWED_STATUS:
            errors.append(f"{p}.status: must be one of {sorted(ALLOWED_STATUS)}")
        for cnt in ("tasks_total", "tasks_success", "tasks_fail"):
            if cnt in s and not isinstance(s[cnt], int):
                errors.append(f"{p}.{cnt}: must be integer")
            if cnt in s and isinstance(s[cnt], int) and s[cnt] < 0:
                errors.append(f"{p}.{cnt}: must be non-negative")
        if "cc_scope" in s:
            if not isinstance(s["cc_scope"], str):
                errors.append(f"{p}.cc_scope: must be string")
            elif s["cc_scope"] not in ALLOWED_CC_SCOPE:
                errors.append(
                    f"{p}.cc_scope: must be one of {sorted(ALLOWED_CC_SCOPE)}"
                )
        if "cc_invoke" in s:
            if not isinstance(s["cc_invoke"], str):
                errors.append(f"{p}.cc_invoke: must be string")
            elif s["cc_invoke"] not in ALLOWED_CC_INVOKE:
                errors.append(
                    f"{p}.cc_invoke: must be one of {sorted(ALLOWED_CC_INVOKE)}"
                )

    employees = data.get("employees")
    if employees is not None and not isinstance(employees, list):
        errors.append(f"{path}: 'employees' must be an array when present")
        return errors

    employee_ids: set[str] = set()
    for i, employee in enumerate(employees or []):
        p = f"{path}.employees[{i}]"
        if not isinstance(employee, dict):
            errors.append(f"{p}: must be an object")
            continue
        for key in REQUIRED_EMPLOYEE:
            if key not in employee:
                errors.append(f"{p}: missing '{key}'")
        employee_id = employee.get("id")
        if isinstance(employee_id, str):
            if employee_id in employee_ids:
                errors.append(f"{p}.id: duplicate id '{employee_id}'")
            employee_ids.add(employee_id)
        status = employee.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{p}.status: must be one of {sorted(ALLOWED_STATUS)}")
        host = employee.get("host")
        if host not in ALLOWED_HOST:
            errors.append(f"{p}.host: must be one of {sorted(ALLOWED_HOST)}")
        created_by = employee.get("created_by")
        if created_by not in ALLOWED_CREATED_BY:
            errors.append(f"{p}.created_by: must be one of {sorted(ALLOWED_CREATED_BY)}")
        employee_skills = employee.get("skills")
        if not isinstance(employee_skills, list) or not employee_skills:
            errors.append(f"{p}.skills: must be a non-empty array")
        else:
            for j, skill_id in enumerate(employee_skills):
                if not isinstance(skill_id, str):
                    errors.append(f"{p}.skills[{j}]: must be string")
                elif skill_id not in skill_ids:
                    errors.append(f"{p}.skills[{j}]: unknown skill id '{skill_id}'")
        primary_skill = employee.get("primary_skill")
        if not isinstance(primary_skill, str) or not primary_skill:
            errors.append(f"{p}.primary_skill: must be non-empty string")
        elif primary_skill not in skill_ids:
            errors.append(f"{p}.primary_skill: unknown skill id '{primary_skill}'")
        elif isinstance(employee_skills, list) and primary_skill not in employee_skills:
            errors.append(f"{p}.primary_skill: must appear in skills[]")
        performance = employee.get("performance")
        perf_path = f"{p}.performance"
        if not isinstance(performance, dict):
            errors.append(f"{perf_path}: must be an object")
        else:
            for cnt in ("tasks_total", "tasks_success", "tasks_fail"):
                if cnt not in performance:
                    errors.append(f"{perf_path}: missing '{cnt}'")
                elif not isinstance(performance[cnt], int):
                    errors.append(f"{perf_path}.{cnt}: must be integer")
                elif performance[cnt] < 0:
                    errors.append(f"{perf_path}.{cnt}: must be non-negative")
        training_history = employee.get("training_history")
        if not isinstance(training_history, list):
            errors.append(f"{p}.training_history: must be an array")
        else:
            for j, event in enumerate(training_history):
                event_path = f"{p}.training_history[{j}]"
                if not isinstance(event, dict):
                    errors.append(f"{event_path}: must be an object")
                    continue
                if "ts" not in event or not isinstance(event["ts"], str):
                    errors.append(f"{event_path}.ts: must be string")
                if "action" not in event or not isinstance(event["action"], str):
                    errors.append(f"{event_path}.action: must be string")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path(".skill-hr") / "registry.json",
        help="Path to registry.json (default: .skill-hr/registry.json)",
    )
    args = parser.parse_args()
    path: Path = args.registry
    if not path.is_file():
        err(f"File not found: {path}")
        return 2
    try:
        data = load_registry(path)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON: {e}")
        return 1
    errors = validate(data, str(path))
    if errors:
        for e in errors:
            err(e)
        return 1
    for w in soul_path_warnings(data, path):
        err(w)
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
