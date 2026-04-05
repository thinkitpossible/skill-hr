# Host adapter: OpenClaw

**HR deployment note:** On OpenClaw, treat **`skill-hr` as the dedicated HR function** for your skill workforce—the same JD → match → recruit → handoff → performance / termination loop as in `SKILL.md`, with `.skill-hr/` registry and incidents as the **HR record** for assignments (host-agnostic paths; see `references/06-state-and-artifacts.md`). In v2, route normal work through `employees[]` and use `skills[]` as the underlying capability catalog. For employees with **`soul_path`**, use **`SOUL.md` as the orchestration layer** over multiple `SKILL.md` files; plugins and OpenClaw tools follow the skill that is actually loaded for each phase.

## Execution contract

On OpenClaw, this host adapter is not just a human runbook. It is the execution contract for which steps the agent should keep running before replying:

- **Default posture:** if the next step is documented, vetted, and non-destructive, execute it and continue the flow.
- **Stop only for real gates:** explicit approval requirements, secrets, destructive changes, missing permissions, or a proven blocker.
- **Report after action:** prefer "installed, verified, delegated" or "blocked because X" over "here is the sequence I would follow."

## Source of truth (keep current with upstream)

Authoritative behavior and schema change with OpenClaw releases. Prefer these pages when anything below drifts:

- [Skills (loading, precedence, format, security)](https://docs.openclaw.ai/tools/skills)
- [Skills config (`openclaw.json`)](https://docs.openclaw.ai/tools/skills-config)
- [Creating skills](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub (install / browse)](https://docs.openclaw.ai/tools/clawhub) — registry: [clawhub.ai](https://clawhub.ai/)

## Main config file

Skill loader and install settings live under **`skills`** in:

`~/.openclaw/openclaw.json`

Agent-level **visibility** (allowlists) lives under **`agents.defaults.skills`** and **`agents.list[].skills`** (separate from *where* files sit on disk).

## Where skills load from (precedence)

When the **same skill name** exists in more than one place, **higher row wins** (workspace / agent paths beat shared and bundled copies):

| Precedence (high → low) | Typical meaning |
|-------------------------|-----------------|
| `<workspace>/skills/` | Per-agent workspace skills; `openclaw skills install` targets the active workspace `skills/` tree |
| `<workspace>/.agents/skills/` | Project-scoped agent skills for that workspace |
| `~/.agents/skills/` | Shared across workspaces for the user profile |
| `~/.openclaw/skills/` | Managed / local overrides visible to agents on this machine |
| Bundled skills | Shipped with the OpenClaw install |
| `skills.load.extraDirs` | Extra directories to scan (**lowest** precedence); each entry should be a folder whose **child directories** are individual skills (each child contains `SKILL.md`) |

Exact path spelling follows your OS and OpenClaw workspace layout; resolve real paths on the machine and record them in the incident the first time you recruit on that host.

Useful **`skills.load`** knobs (defaults may change—see [Skills config](https://docs.openclaw.ai/tools/skills-config)):

- `extraDirs` — additional skill roots
- `watch` / `watchDebounceMs` — refresh when `SKILL.md` changes (often picked up on the next agent turn)

## Installing `skill-hr`

1. Copy this repository folder **`packages/skill-hr/`** into a **skill root** as a directory named **`skill-hr`**, so `SKILL.md` resolves as **`skill-hr/SKILL.md`**, preserving **`references/`** and **`scripts/`**.

   **Common choices:**

   - **All agents on this machine:** `~/.openclaw/skills/skill-hr/`
   - **Current OpenClaw workspace only:** `<active-workspace>/skills/skill-hr/` (matches “workspace wins” precedence)
   - **Shared pack via config:** parent directory listed in `skills.load.extraDirs`, with `skill-hr` as a subfolder under that parent

2. If you use **agent skill allowlists**, add the skill key OpenClaw uses for this package. Default config keys match the skill **`name`** in frontmatter (`skill-hr`). Hyphenated names are supported; in JSON5 you can quote the key under `skills.entries` if needed.

3. **Reload:** start a **new** session (e.g. `/new` in chat) or **`openclaw gateway restart`** so the loader picks up the skill. Verify with:

   ```bash
   openclaw skills list
   ```

## Discovering the installed pool (P02)

- Prefer **`openclaw skills list`** for the effective snapshot on that session.
- For bench analysis, you may still enumerate skill directories under the roots above and read each **`SKILL.md`** frontmatter (`name`, `description`).
- Merge with **project** `.skill-hr/registry.json` when the workspace uses HR state in-repo. If `employees[]` exists, prefer ranking employee bundles after the raw skill discovery step. After delegation, if the chosen employee has **`soul_path`**, read that file from the workspace before chaining domain `SKILL.md` loads per `references/10-multi-skill-agent.md`.

## Safe agent actions vs user-gated actions

**Normally agent-executable after the candidate itself is approved:**

- `openclaw skills list`
- `openclaw skills install ...` against a vetted marketplace or source
- Copying a vetted local skill folder into a documented OpenClaw skill root
- Starting a new session or running `openclaw gateway restart` when reload is required
- Writing `.skill-hr/registry.json` and incident artifacts
- Running a smoke delegation after install

**Still user-gated:**

- Unvetted shell from the network
- Destructive filesystem cleanup or uninstall
- Auth or payment steps requiring the user
- Any action that violates the current sandbox / permissions posture

Approval should be collected at the **candidate / risk** level when possible, not repeated for every safe substep in the same install-and-verify path.

## Format notes (OpenClaw ↔ this bundle)

OpenClaw documents **[AgentSkills](https://agentskills.io/)**-compatible folders with **`SKILL.md`** + YAML frontmatter. The embedded parser expects **single-line frontmatter keys**; keep `description` on **one line** (quoted if it contains `:`). If you add **`metadata.openclaw`**, upstream expects it as a **single-line JSON object** in frontmatter—see [Skills](https://docs.openclaw.ai/tools/skills).

Optional: use **`{baseDir}`** in instructions to mean the skill folder path (OpenClaw replaces it when building prompts).

## Recruitment and marketplace flows

- **From ClawHub / CLI:** prefer documented commands such as **`openclaw skills install …`** and **`openclaw skills update --all`** per [ClawHub](https://docs.openclaw.ai/tools/clawhub); installs into the **active workspace** `skills/` tree unless your setup differs.
- **From git:** cloning or copying into one of the skill roots above is fine; log **`source_url`** in `.skill-hr/registry.json`.
- **Safety:** treat third-party skills as untrusted; avoid silent **`curl | sh`**. Gateway-backed installs may run a **dangerous-code scanner**—still apply **`references/01-competency-model.md`** vetoes and user confirmation before risky steps.

## OpenClaw happy path

When recruitment is needed and the candidate passes vetting:

1. Present the top candidate and the approval-gated risks once.
2. After approval, run the documented install path.
3. Verify visibility with `openclaw skills list` and reload if needed.
4. Register the skill as `on_probation`. If the skill belongs to a designed employee, append it to that employee's record and add a `training_history[]` event.
5. Continue into delegation or smoke-task execution before replying.

Do not stop after step 1 if steps 2–5 are still safe and documented.

## Sandbox and env

If the agent runs in a **sandbox**, host `process.env` may not apply to skill child processes. Per OpenClaw docs, use **`agents.defaults.sandbox.docker.env`** (or per-agent equivalents) or a custom image when a recruited skill needs env vars or binaries inside the container.

## Incident and registry paths

Use **workspace root** paths from **`references/06-state-and-artifacts.md`** so HR state can live in the repo (`.skill-hr/registry.json`, `.skill-hr/incidents/`) regardless of OpenClaw skill install location.

## Dashboard bridge

The local dashboard can run beside OpenClaw as a read/write bridge over the same workspace state. Keep the dashboard pointed at the repo root so it reflects:

- OpenClaw-hosted employees and their host-specific skill bundles
- task-board progress in `.skill-hr/hr_tasks.json`
- incident trails written during recruitment, delegation, and debrief

### Having the OpenClaw agent start the Dashboard

OpenClaw does **not** auto-start the dashboard when a skill loads. Treat “run the dashboard” like any other **documented, user-approved** host action: if the user asks and the agent has a safe shell / process tool, **execute** the steps below from the machine that should serve the UI (usually the same host as the OpenClaw workspace), then report the URL.

**Suggested user phrases (skill routing):** e.g. “Start the skill-hr Dashboard”, “Open the HR board UI”; 中文如「启动 skill-hr 看板」「打开人事看板」—aligned with `SKILL.md` `description` so `skill-hr` loads.

**Prerequisites on that host:** `node` + `npm` (for build) and `python3` with the skill’s `scripts/` dependencies importable (run scripts with imports resolvable from `packages/skill-hr/scripts`—same as README).

**Paths (important):** The launcher discovers a repo root that contains **`dashboard/package.json`**. If you only copied **`skill-hr/`** into `~/.openclaw/skills/` without the monorepo’s `dashboard/` tree, `launch_dashboard.py` will exit with an error—use a **full git checkout**, or run `server.py` manually with **`--static-dir`** to a built `dashboard/dist`.

**Preferred one-shot (workspace = repo root with `dashboard/` and `.skill-hr/`):**

```bash
python packages/skill-hr/scripts/launch_dashboard.py --workspace-root . --port 8787
```

- **OpenClaw / agent should return while the server keeps running:** add **`--background`**, then tell the user to open `http://127.0.0.1:8787` (or the chosen `--host` / `--port`).
- **Faster repeat runs** when `dashboard/dist` is already fresh: **`--skip-build`** (skips `npm ci` / `npm install` and `npm run build`).

**Manual / troubleshooting flow** (equivalent to what the launcher does by default):

1. `cd dashboard && npm install && npm run build` (or `npm ci` when `package-lock.json` exists)
2. From repo root: `python packages/skill-hr/scripts/server.py --port 8787 --workspace-root .`
   - If static files are elsewhere: add `--static-dir /path/to/dashboard/dist`

**Long-running process:** In the foreground the server blocks; prefer **`launch_dashboard.py --background`** (or your tool’s detached job) so the agent can still reply. If the sandbox has no Node or Python, or binds are forbidden, report that blocker instead of guessing.

**Completion-first:** when the user asks to “open” or “start” the dashboard, prefer running the command above (after any needed approval) over returning only prose instructions.

**Copy-paste rules / tool text:** [openclaw-dashboard-workflow.md](openclaw-dashboard-workflow.md).

## Maintenance

When OpenClaw changes default paths or config keys, update this file in **one focused edit** and align any examples in **`references/prompts/P04-market-search-brief.md`** outputs for `host: openclaw`.
