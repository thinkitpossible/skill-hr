# OpenClaw: skill-hr Dashboard — copy-paste workflow snippets

Use this file when you want **one place** to copy rules or tool text into OpenClaw (workspace rules, `AGENTS.md`, or a custom tool description). Upstream OpenClaw config shapes change; align field names with [Skills config](https://docs.openclaw.ai/tools/skills-config) and your gateway version.

## Suggested user phrases (routes to `skill-hr`)

These align with the `SKILL.md` description so the skill is likely to load:

- English: “Start the skill-hr Dashboard”, “Open the HR board UI for skill-hr”.
- 中文：「启动 skill-hr 看板」「打开人事看板 / Dashboard」。

## Block for workspace rules or `AGENTS.md`

Paste and adjust paths if your OpenClaw workspace root differs from the skill-hr git checkout:

```markdown
When the user asks to start or open the **skill-hr local Dashboard** (Web UI over `.skill-hr/`):

1. `cd` to the **repository root** that contains both `dashboard/` and `packages/skill-hr/`.
2. Run: `python packages/skill-hr/scripts/launch_dashboard.py --workspace-root . --port 8787`
3. For OpenClaw (agent must return while the server keeps running), add **`--background`** and tell the user to open `http://127.0.0.1:8787` (or the chosen host/port).
4. If Node/npm or bind fails, report the error; do not invent paths.

If only the `skill-hr/` skill folder is installed without the monorepo `dashboard/` tree, a full checkout or manual `server.py --static-dir <path-to-built-dist>` is required—see `references/hosts/openclaw.md`.
```

## Template: custom tool / plugin description (natural language)

Copy into whatever field your setup uses for “what this tool does” (adapt to JSON5 / YAML as needed):

```text
Purpose: Build and serve the skill-hr Dashboard (static UI + local API) for the current workspace.

When to use: User wants to open/start the skill-hr Dashboard, HR board UI, or 人事看板.

Steps:
- Working directory: root of the skill-hr git repository (must contain `dashboard/` and `packages/skill-hr/scripts/`).
- Command: python packages/skill-hr/scripts/launch_dashboard.py --workspace-root . --port 8787 --background
- Success: Process stays running; user opens http://127.0.0.1:8787
- Prerequisites: Node.js + npm on PATH; Python can import packages under packages/skill-hr/scripts (same as README).
- Failure: Missing dashboard/ (standalone skill copy only) → instruct full clone or run server.py with --static-dir to a prebuilt dist; port in use → try another --port.
```

## Canonical command reference

| Flag | Meaning |
|------|---------|
| `--workspace-root .` | Repo root with `.skill-hr/` |
| `--port 8787` | Listen port (default 8787) |
| `--background` | Detach server so the agent session can continue |
| `--skip-build` | Skip npm when `dashboard/dist` is already built |

Full host semantics: [openclaw.md](openclaw.md) (Dashboard bridge section).
