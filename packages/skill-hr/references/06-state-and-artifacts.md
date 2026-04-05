# State and artifacts

## Locations (project-local)

All paths are relative to the **workspace root** (the repository or folder the user is working in).

| Artifact | Path | Purpose |
|----------|------|---------|
| Registry | `.skill-hr/registry.json` | Skill pool under HR management: status, stats, install hints |
| HR task board | `.skill-hr/hr_tasks.json` | Multi-agent **assignment** state: Kanban-style task id, `state`, `flow_log`, `progress_log` (maintain via `scripts/hr_dispatch.py`) |
| Incidents dir | `.skill-hr/incidents/` | Per-assignment audit trail |
| Incident file | `.skill-hr/incidents/YYYYMMDD-HHmm-<slug>.md` | Human-readable record (preferred default) |
| JSONL stream | `.skill-hr/incidents/stream.jsonl` | Optional machine append-only log |

Create `.skill-hr/` on first use. Do not commit secrets into incidents.

## `hr_tasks.json` (multi-agent)

Used when the **Skill HR department** tracks an end-to-end assignment with `scripts/hr_dispatch.py`. Do not hand-edit unless repairing a failed tool call; the script enforces **legal state transitions**.

Top-level object:

```json
{
  "skill_hr_tasks_version": "1.0.0",
  "updated_at": "2026-04-05T12:00:00Z",
  "tasks": []
}
```

### `tasks[]` item

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable id, e.g. `HR-20260405-001` |
| `title` | string | Short human title |
| `state` | string | One of the **HR task states** below |
| `created_at` | string (ISO-8601) | Creation time |
| `updated_at` | string | Last update |
| `current_agent` | string | Last agent id from `flow` (e.g. `talent-assessor`) |
| `flow_log` | array | `{ts, from_agent, to_agent, remark}` handoffs |
| `progress_log` | array | `{ts, current_work, plan}` snapshots |
| `state_notes` | array | Optional `{ts, state, note}` from `hr_dispatch.py state` |

### HR task states (directed workflow)

| State | Meaning |
|-------|---------|
| `Intake` | User request received; JD not finalized |
| `JDReady` | P01 complete; ready for P02 |
| `Matching` | P02 in progress |
| `Matched` | Candidate skill selected (installed or approved) |
| `Recruiting` | P04 market search / install path |
| `Vetting` | Compliance review of candidate |
| `Delegated` | P03 handoff package issued |
| `InProgress` | Domain skill executing |
| `Debrief` | P05 review |
| `Probation` | Underperformance path |
| `Escalation` | No fit / blocker per `07-escalation.md` |
| `Closed` | Terminal — completed or deferred with record |
| `Terminated` | Terminal — skill/task offboarded per policy |

**CLI:** `python3 scripts/hr_dispatch.py create|state|flow|progress|show|list` (from the skill package path, or `skill-hr/scripts/...` when installed). See `agents/GLOBAL.md`.

## `registry.json` schema

Top-level object:

```json
{
  "skill_hr_version": "1.0.0",
  "updated_at": "2026-04-04T12:00:00Z",
  "hosts": ["claude-code", "cursor", "openclaw"],
  "matching": {
    "delegate_min_score": 75,
    "confirm_band_min": 60,
    "max_trials_per_task_per_skill": 2
  },
  "skills": []
}
```

### `skills[]` item

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable id, e.g. `pdf` or `my-org-deploy` |
| `name` | string | yes | Matches skill `name` in SKILL.md frontmatter when known |
| `install_path` | string | no | Filesystem path to skill directory, if local |
| `source_url` | string | no | Provenance (repo, marketplace URL) |
| `status` | string | yes | `active` \| `on_probation` \| `terminated` \| `frozen` |
| `added_at` | string (ISO-8601) | yes | When registered |
| `last_used_at` | string | no | Last delegation |
| `tasks_total` | integer | yes | Monotonic counter |
| `tasks_success` | integer | yes | Subset of completed successes |
| `tasks_fail` | integer | yes | Failures attributed to wrong skill / skill limit |
| `notes` | string | no | HR notes (e.g. "good for forms, not OCR") |
| `cc_scope` | string | no | Claude Code only: where the skill lives on disk — `user` \| `project` \| `nested` \| `plugin` \| `unknown` (from `hosts/claude-code.md` / `scan_claude_code_skills.py`) |
| `cc_invoke` | string | no | Claude Code only: `auto` (model may auto-load) \| `manual_only` (`disable-model-invocation` or equivalent; prefer user `/skill`) |

**Status semantics**

- `active`: eligible for automatic delegation when score ≥ threshold.
- `on_probation`: eligible but prefer confirmation for scores &lt; 85; mandatory debrief.
- `terminated`: **not** eligible; excluded from P02 pool. Physical uninstall is separate and user-gated.
- `frozen`: temporarily excluded (user or policy); not terminated.

## Incident markdown format

Filename: `20260404-1430-analyze-resume.md` (UTC or local—pick one per project and stay consistent).

Frontmatter (YAML):

```yaml
---
incident_id: 20260404-1430-analyze-resume
hr_task_id: HR-20260404-1430-analyze-resume
hr_task_state: Debrief
task_summary: "User wants resume parsing to structured JSON"
jd_role_title: "Resume ingestion analyst"
selected_skill_id: interview-designer
selected_skill_name: interview-designer
match_score: 78
phase: debrief
references_used:
  - references/prompts/P03-delegate-handoff.md
  - references/prompts/P05-trial-and-debrief.md
host_actions_taken:
  - delegated incumbent
  - verified output artifact
approval_gates_hit: []
outcome: success
root_cause_class: n/a
registry_updated: true
---
```

Body sections (headings):

1. **User request** — verbatim or faithful paraphrase.
2. **JD excerpt** — bullet summary from P01.
3. **Match rationale** — scores, alternatives considered.
4. **Handoff** — what was sent to the incumbent (P03 summary).
5. **Execution trace** — phases reached, host actions taken, approvals consumed, checkpoints attempted.
6. **Result** — deliverables, errors, partial work, and completion evidence.
7. **Next actions** — retain / probation / terminate / escalate.

## Optional incident fields

Use these when you need to explain why the framework stopped or continued:

- `hr_task_id` — links to `.skill-hr/hr_tasks.json` when using multi-agent mode
- `hr_task_state` — snapshot of board state when the incident was written
- `phase` — current or terminal phase, e.g. `matching`, `recruitment`, `delegation`, `debrief`, `escalation`
- `references_used` — list of prompt or reference files consulted during the run
- `host_actions_taken` — concrete host actions already executed
- `approval_gates_hit` — approvals requested or blocking gates encountered
- `completion_checkpoint` — the checkpoint the incumbent was expected to reach
- `completion_evidence` — artifact paths, commands, tests, or observed host state showing execution happened

These fields are optional and additive; they exist so the trace can live in incidents instead of chat.

## JSONL incident line (optional)

Each line is a JSON object:

```json
{"ts":"2026-04-04T14:30:00Z","incident_id":"...","skill_id":"...","outcome":"fail","root_cause_class":"wrong_match"}
```

## Example registry

See [examples/registry.example.json](../examples/registry.example.json).

## Migration

Bump `skill_hr_version` when breaking schema changes; keep a one-line note in `notes` on the registry or in repo CHANGELOG (human-facing).
