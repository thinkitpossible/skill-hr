#!/usr/bin/env python3
"""Local API bridge for the skill-hr dashboard."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from hr_dispatch import (
    append_task_progress,
    create_task,
    find_workspace_root,
    get_task_data,
    list_tasks_data,
    transition_task_state,
)
from registry_runtime import load_registry, save_registry


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return text or "task"


def _make_task_id() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("HR-%Y%m%d-%H%M%S")


def _parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    parts = markdown.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, markdown
    raw_frontmatter = parts[0].splitlines()[1:]
    body = parts[1]
    meta: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw_frontmatter:
        if line.startswith("  - ") and current_key:
            meta.setdefault(current_key, []).append(line[4:].strip())
            continue
        if line.startswith("- ") and current_key:
            meta.setdefault(current_key, []).append(line[2:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if value == "":
            meta[key] = []
            current_key = key
        else:
            meta[key] = value
            current_key = None
    return meta, body


class SkillHrStore:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.package_root = Path(__file__).resolve().parents[1]
        self.incidents_dir = workspace_root / ".skill-hr" / "incidents"
        self.registry_path = workspace_root / ".skill-hr" / "registry.json"
        self.templates_path = self.package_root / "templates" / "templates.json"
        self.agents_dir = self.package_root / "agents"

    def load_tasks(self) -> list[dict[str, Any]]:
        tasks = list_tasks_data(self.workspace_root)
        return sorted(tasks, key=lambda item: item.get("updated_at", ""), reverse=True)

    def get_task(self, task_id: str) -> dict[str, Any]:
        task = get_task_data(task_id, self.workspace_root)
        task["related_incidents"] = self.find_incidents_for_task(task_id)
        return task

    def load_registry(self) -> dict[str, Any]:
        return load_registry(self.registry_path)

    def save_registry(self, registry: dict[str, Any]) -> None:
        registry["updated_at"] = _utc_now_iso()
        save_registry(self.registry_path, registry)

    def load_templates(self) -> list[dict[str, Any]]:
        if not self.templates_path.is_file():
            return []
        data = json.loads(self.templates_path.read_text(encoding="utf-8"))
        templates = data.get("templates", [])
        return templates if isinstance(templates, list) else []

    def load_incidents(self) -> list[dict[str, Any]]:
        if not self.incidents_dir.is_dir():
            return []
        incidents: list[dict[str, Any]] = []
        for path in sorted(self.incidents_dir.glob("*.md"), reverse=True):
            markdown = path.read_text(encoding="utf-8")
            frontmatter, body = _parse_frontmatter(markdown)
            incidents.append(
                {
                    "filename": path.name,
                    "path": str(path.relative_to(self.workspace_root)),
                    "frontmatter": frontmatter,
                    "body": body,
                    "markdown": markdown,
                }
            )
        return incidents

    def find_incidents_for_task(self, task_id: str) -> list[dict[str, Any]]:
        return [
            {
                "filename": incident["filename"],
                "frontmatter": incident["frontmatter"],
            }
            for incident in self.load_incidents()
            if incident["frontmatter"].get("hr_task_id") == task_id
        ]

    def load_hr_agents(self) -> list[dict[str, Any]]:
        tasks = self.load_tasks()
        current_by_agent: dict[str, list[dict[str, Any]]] = {}
        for task in tasks:
            agent_id = task.get("current_agent")
            if isinstance(agent_id, str) and agent_id:
                current_by_agent.setdefault(agent_id, []).append(task)

        agents: list[dict[str, Any]] = []
        for path in sorted(self.agents_dir.glob("*/SOUL.md")):
            agent_id = path.parent.name
            heading = path.read_text(encoding="utf-8").splitlines()[0].strip("# ").strip()
            active_tasks = current_by_agent.get(agent_id, [])
            agents.append(
                {
                    "id": agent_id,
                    "name": heading.split("`")[0].strip() or agent_id,
                    "role": heading,
                    "active_task_count": len(active_tasks),
                    "current_tasks": [
                        {
                            "id": task.get("id"),
                            "title": task.get("title"),
                            "state": task.get("state"),
                        }
                        for task in active_tasks[:5]
                    ],
                    "health": "busy" if active_tasks else "idle",
                }
            )
        return agents

    def load_employees(self) -> list[dict[str, Any]]:
        registry = self.load_registry()
        skills_by_id = {
            skill["id"]: skill for skill in registry.get("skills", []) if isinstance(skill, dict) and "id" in skill
        }
        incidents = self.load_incidents()
        employees: list[dict[str, Any]] = []
        for employee in registry.get("employees", []):
            if not isinstance(employee, dict):
                continue
            perf = employee.get("performance", {})
            tasks_total = int(perf.get("tasks_total", 0) or 0)
            tasks_success = int(perf.get("tasks_success", 0) or 0)
            employee_incidents = [
                {
                    "filename": incident["filename"],
                    "frontmatter": incident["frontmatter"],
                }
                for incident in incidents
                if incident["frontmatter"].get("selected_employee_id") == employee.get("id")
                or incident["frontmatter"].get("selected_skill_id") in employee.get("skills", [])
            ]
            employees.append(
                {
                    **employee,
                    "skill_details": [
                        skills_by_id[skill_id]
                        for skill_id in employee.get("skills", [])
                        if skill_id in skills_by_id
                    ],
                    "success_rate": round((tasks_success / tasks_total) * 100, 1) if tasks_total else 0.0,
                    "related_incidents": employee_incidents,
                }
            )
        return employees

    def create_task_from_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        title = str(payload.get("title") or "").strip()
        if not title:
            raise ValueError("title is required")
        task_id = str(payload.get("id") or _make_task_id())
        state = str(payload.get("state") or "Intake")
        create_task(task_id, title, state)
        summary = str(payload.get("summary") or "").strip()
        if summary:
            append_task_progress(task_id, summary, "Created from dashboard request")
        return self.get_task(task_id)

    def create_task_from_template(self, template_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        templates = {template["id"]: template for template in self.load_templates() if isinstance(template, dict)}
        if template_id not in templates:
            raise KeyError(template_id)
        template = templates[template_id]
        defaults = template.get("defaults", {})
        title = str(payload.get("title") or defaults.get("title") or template["name"]).strip()
        summary = str(payload.get("summary") or defaults.get("summary") or template["description"]).strip()
        task = self.create_task_from_payload({"title": title, "summary": summary})
        append_task_progress(
            task["id"],
            f"Seeded from template {template['name']}",
            ", ".join(template.get("keywords", [])),
        )
        return self.get_task(task["id"])

    def update_task_state(self, task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        new_state = str(payload.get("new_state") or "").strip()
        if not new_state:
            raise ValueError("new_state is required")
        note = str(payload.get("note") or "").strip()
        transition_task_state(task_id, new_state, note)
        return self.get_task(task_id)

    def update_employee_status(self, employee_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        new_status = str(payload.get("status") or "").strip()
        if not new_status:
            raise ValueError("status is required")
        registry = self.load_registry()
        employees = registry.get("employees", [])
        for employee in employees:
            if isinstance(employee, dict) and employee.get("id") == employee_id:
                employee["status"] = new_status
                employee.setdefault("training_history", []).append(
                    {
                        "ts": _utc_now_iso(),
                        "action": "status_updated",
                        "notes": str(payload.get("note") or "").strip(),
                    }
                )
                self.save_registry(registry)
                return next(item for item in self.load_employees() if item["id"] == employee_id)
        raise KeyError(employee_id)

    def build_stats(self) -> dict[str, Any]:
        tasks = self.load_tasks()
        employees = self.load_employees()
        agents = self.load_hr_agents()
        incidents = self.load_incidents()
        task_counts: dict[str, int] = {}
        for task in tasks:
            state = str(task.get("state") or "unknown")
            task_counts[state] = task_counts.get(state, 0) + 1
        return {
            "task_counts": task_counts,
            "task_total": len(tasks),
            "employee_total": len(employees),
            "hr_agent_total": len(agents),
            "incident_total": len(incidents),
        }


class SkillHrHandler(BaseHTTPRequestHandler):
    store: SkillHrStore
    static_dir: Path | None = None

    def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,OPTIONS")
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, payload: str, content_type: str = "text/plain; charset=utf-8") -> None:
        data = payload.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, path: Path) -> None:
        data = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def _error(self, status: int, message: str) -> None:
        self._send_json({"error": message}, status)

    def _resolve_static_path(self, path: str) -> Path | None:
        if not self.static_dir:
            return None
        requested = (self.static_dir / path.lstrip("/")).resolve()
        static_root = self.static_dir.resolve()
        if static_root not in requested.parents and requested != static_root:
            return None
        if requested.is_file():
            return requested
        index_file = static_root / "index.html"
        if index_file.is_file():
            return index_file
        return None

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/health":
                self._send_json({"ok": True, "ts": _utc_now_iso()})
                return
            if path == "/api/tasks":
                tasks = self.store.load_tasks()
                state = query.get("state", [None])[0]
                if state:
                    tasks = [task for task in tasks if task.get("state") == state]
                self._send_json({"tasks": tasks})
                return
            if path.startswith("/api/tasks/"):
                task_id = path.split("/", 3)[3]
                self._send_json(self.store.get_task(task_id))
                return
            if path == "/api/archives":
                archives = [
                    task for task in self.store.load_tasks() if task.get("state") in {"Closed", "Terminated"}
                ]
                archive_ids = {task["id"] for task in archives if "id" in task}
                incidents = [
                    incident
                    for incident in self.store.load_incidents()
                    if incident["frontmatter"].get("hr_task_id") in archive_ids
                ]
                self._send_json({"tasks": archives, "incidents": incidents})
                return
            if path == "/api/agents":
                self._send_json({"agents": self.store.load_hr_agents()})
                return
            if path == "/api/employees":
                self._send_json({"employees": self.store.load_employees()})
                return
            if path.startswith("/api/employees/"):
                employee_id = path.split("/", 3)[3]
                employee = next(
                    (item for item in self.store.load_employees() if item.get("id") == employee_id),
                    None,
                )
                if not employee:
                    self._error(HTTPStatus.NOT_FOUND, f"Unknown employee id: {employee_id}")
                    return
                self._send_json(employee)
                return
            if path == "/api/templates":
                self._send_json({"templates": self.store.load_templates()})
                return
            if path == "/api/incidents":
                incidents = [
                    {"filename": incident["filename"], "frontmatter": incident["frontmatter"]}
                    for incident in self.store.load_incidents()
                ]
                self._send_json({"incidents": incidents})
                return
            if path.startswith("/api/incidents/"):
                filename = path.split("/", 3)[3]
                incident = next(
                    (item for item in self.store.load_incidents() if item.get("filename") == filename),
                    None,
                )
                if not incident:
                    self._error(HTTPStatus.NOT_FOUND, f"Unknown incident: {filename}")
                    return
                self._send_json(incident)
                return
            if path == "/api/stats":
                self._send_json(self.store.build_stats())
                return
            static_file = self._resolve_static_path(path)
            if static_file and not path.startswith("/api/"):
                self._send_file(static_file)
                return
            self._error(HTTPStatus.NOT_FOUND, f"Unknown endpoint: {path}")
        except FileNotFoundError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except ValueError as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:  # pragma: no cover - defensive server path
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._read_json()
            if path == "/api/tasks":
                self._send_json(self.store.create_task_from_payload(payload), HTTPStatus.CREATED)
                return
            if path.startswith("/api/templates/") and path.endswith("/execute"):
                template_id = path.split("/", 3)[3].rsplit("/", 1)[0]
                self._send_json(self.store.create_task_from_template(template_id, payload), HTTPStatus.CREATED)
                return
            self._error(HTTPStatus.NOT_FOUND, f"Unknown endpoint: {path}")
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except ValueError as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:  # pragma: no cover - defensive server path
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_PATCH(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._read_json()
            if path.startswith("/api/tasks/") and path.endswith("/state"):
                task_id = path.split("/", 3)[3].rsplit("/", 1)[0]
                self._send_json(self.store.update_task_state(task_id, payload))
                return
            if path.startswith("/api/employees/") and path.endswith("/status"):
                employee_id = path.split("/", 3)[3].rsplit("/", 1)[0]
                self._send_json(self.store.update_employee_status(employee_id, payload))
                return
            self._error(HTTPStatus.NOT_FOUND, f"Unknown endpoint: {path}")
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except ValueError as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:  # pragma: no cover - defensive server path
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=None,
        help="Workspace root containing .skill-hr/ (default: auto-discover from cwd)",
    )
    parser.add_argument(
        "--static-dir",
        type=Path,
        default=None,
        help="Optional static dashboard build directory",
    )
    args = parser.parse_args()

    workspace_root = find_workspace_root(args.workspace_root, ensure=True)
    store = SkillHrStore(workspace_root)
    handler = SkillHrHandler
    handler.store = store
    default_static_dir = Path(__file__).resolve().parents[3] / "dashboard" / "dist"
    handler.static_dir = args.static_dir or (default_static_dir if default_static_dir.is_dir() else None)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"skill-hr API listening on http://{args.host}:{args.port}")
    print(f"workspace_root={workspace_root}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
