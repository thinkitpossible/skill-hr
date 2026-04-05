#!/usr/bin/env python3
"""Build the skill-hr dashboard (npm) and start scripts/server.py for the local UI + API."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _find_repo_root_with_dashboard(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        dash = parent / "dashboard"
        if dash.is_dir() and (dash / "package.json").is_file():
            return parent
    return None


def _run_npm_build(dashboard_dir: Path) -> int:
    lock = dashboard_dir / "package-lock.json"
    cmd = ["npm", "ci"] if lock.is_file() else ["npm", "install"]
    r = subprocess.run(cmd, cwd=dashboard_dir, check=False)
    if r.returncode != 0:
        return r.returncode
    r = subprocess.run(["npm", "run", "build"], cwd=dashboard_dir, check=False)
    return r.returncode


def _server_cmd(
    server_py: Path,
    host: str,
    port: int,
    workspace_root: Path,
    static_dir: Path | None,
) -> list[str]:
    cmd = [
        sys.executable,
        str(server_py),
        "--host",
        host,
        "--port",
        str(port),
        "--workspace-root",
        str(workspace_root.resolve()),
    ]
    if static_dir is not None:
        cmd.extend(["--static-dir", str(static_dir.resolve())])
    return cmd


def _popen_server_background(cmd: list[str]) -> subprocess.Popen:
    kwargs: dict = {}
    if sys.platform == "win32":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        det = getattr(subprocess, "DETACHED_PROCESS", 0)
        if det:
            creationflags |= det
        kwargs["creationflags"] = creationflags
    else:
        kwargs["start_new_session"] = True

    return subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=sys.platform != "win32",
        **kwargs,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=None,
        help="Workspace root containing .skill-hr/ (default: current working directory)",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip npm install/build (use existing dashboard/dist)",
    )
    parser.add_argument(
        "--background",
        action="store_true",
        help="Start server detached so the shell returns immediately",
    )
    parser.add_argument(
        "--static-dir",
        type=Path,
        default=None,
        help="Override static files directory (default: <repo>/dashboard/dist when present)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    server_py = script_dir / "server.py"
    if not server_py.is_file():
        print("launch_dashboard: server.py not found next to this script.", file=sys.stderr)
        return 1

    repo_root = _find_repo_root_with_dashboard(script_dir)
    if repo_root is None:
        print(
            "launch_dashboard: no sibling dashboard/ with package.json found above this script.\n"
            "Use a full git checkout of skill-hr that includes the dashboard/ tree, or run server.py "
            "manually with --static-dir pointing at a built dashboard/dist.",
            file=sys.stderr,
        )
        return 1

    dashboard_dir = repo_root / "dashboard"
    dist_dir = args.static_dir or (dashboard_dir / "dist")

    if not args.skip_build:
        print(f"launch_dashboard: building dashboard in {dashboard_dir}")
        rc = _run_npm_build(dashboard_dir)
        if rc != 0:
            print("launch_dashboard: npm build failed.", file=sys.stderr)
            return rc
    elif not dist_dir.is_dir() or not (dist_dir / "index.html").is_file():
        print(
            f"launch_dashboard: --skip-build but {dist_dir} is missing or has no index.html.",
            file=sys.stderr,
        )
        return 1

    workspace_root = (args.workspace_root or Path.cwd()).resolve()

    cmd = _server_cmd(server_py, args.host, args.port, workspace_root, args.static_dir)
    url = f"http://{args.host}:{args.port}"

    if args.background:
        _popen_server_background(cmd)
        print(f"launch_dashboard: server started in background; open {url}")
        return 0

    print(f"launch_dashboard: starting server; open {url}")
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
