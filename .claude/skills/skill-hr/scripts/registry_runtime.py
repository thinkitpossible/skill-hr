#!/usr/bin/env python3
"""Helpers for loading a backward-compatible skill-hr registry."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ALLOWED_STATUS = frozenset({"active", "on_probation", "terminated", "frozen"})
ALLOWED_HOSTS = frozenset({"claude-code", "cursor", "openclaw", "unknown"})


def _default_matching() -> dict[str, int]:
    return {
        "delegate_min_score": 75,
        "confirm_band_min": 60,
        "max_trials_per_task_per_skill": 2,
    }


def default_registry() -> dict[str, Any]:
    return {
        "skill_hr_version": "2.0.0",
        "updated_at": "",
        "hosts": [],
        "matching": _default_matching(),
        "skills": [],
        "employees": [],
    }


def _skill_performance(skill: dict[str, Any]) -> dict[str, int]:
    return {
        "tasks_total": int(skill.get("tasks_total", 0) or 0),
        "tasks_success": int(skill.get("tasks_success", 0) or 0),
        "tasks_fail": int(skill.get("tasks_fail", 0) or 0),
    }


def derive_employee_from_skill(skill: dict[str, Any]) -> dict[str, Any]:
    skill_id = str(skill.get("id") or "").strip()
    skill_name = str(skill.get("name") or skill_id or "unknown").strip()
    host = "claude-code" if skill.get("cc_scope") else "unknown"
    if host not in ALLOWED_HOSTS:
        host = "unknown"
    return {
        "id": skill_id,
        "name": skill_name,
        "status": skill.get("status", "active"),
        "skills": [skill_id] if skill_id else [],
        "primary_skill": skill_id,
        "host": host,
        "created_by": "migrated",
        "added_at": skill.get("added_at", ""),
        "last_used_at": skill.get("last_used_at"),
        "source_skill_id": skill_id,
        "notes": skill.get("notes", ""),
        "performance": _skill_performance(skill),
        "training_history": [],
    }


def normalize_registry(data: dict[str, Any]) -> dict[str, Any]:
    doc = default_registry()
    doc.update(deepcopy(data))
    doc["matching"] = {**_default_matching(), **deepcopy(data.get("matching", {}))}
    skills = deepcopy(data.get("skills", []))
    doc["skills"] = skills if isinstance(skills, list) else []

    employees = deepcopy(data.get("employees", []))
    if isinstance(employees, list) and employees:
        doc["employees"] = employees
    else:
        doc["employees"] = [
            derive_employee_from_skill(skill)
            for skill in doc["skills"]
            if isinstance(skill, dict)
        ]

    version = str(doc.get("skill_hr_version") or "").strip() or "2.0.0"
    doc["skill_hr_version"] = version
    return doc


def load_registry(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return default_registry()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return normalize_registry(data)


def save_registry(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
