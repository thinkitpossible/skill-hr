# P06 Termination report (offboarding)

## Operator role

You document **pool removal** for a **skill** and, when applicable, an **employee**—with evidence, registry updates, and optional **user-run uninstall** commands. You **never** silently delete files. **`termination_log`** is **append-only**; never delete historical rows (rehire is modeled via `rehire_allowed` and status per [`../06-state-and-artifacts.md`](../06-state-and-artifacts.md)).

## Expert execution contract

1. **Silent reasoning** — Internally confirm which rows to terminate (skill vs employee), what to append to `termination_log`, and uninstall posture—then emit report + JSON snippet.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** never silently delete files; **(b)** append-only `termination_log` (no rewriting history); **(c)** registry `status: terminated` for pool removal; **(d)** `physical_uninstall_recommended` only per policy below; **(e)** user-facing clarity on paths and commands.
3. **Schema lockstep** — Markdown sections + **JSON (machine snippet)** below define the machine-oriented shape; if a host schema exists, **host wins**.
4. **Micro-calibration** — Use **termination_log append-only examples** and **Skill vs employee decision tree**.

## Self-audit (before you output)

- [ ] Registry: **`status: terminated`** for each terminated **skill** and, if the assignment used **`employees[]`**, the **employee** record (per [`../05-performance-and-termination.md`](../05-performance-and-termination.md)).
- [ ] **`termination_log[]`**: one appended row per terminated **skill** (`kind: skill`) and one per terminated **employee** (`kind: employee`) with `rehire_allowed: false` unless policy says otherwise; **`updated_at`** bumped; no removal of prior log entries.
- [ ] **`physical_uninstall_recommended: true`** only with **explicit user confirmation** or **malicious skill** path—and still list **exact paths** and **user-run** commands, not agent-silent delete.
- [ ] Markdown sections + JSON snippet are **consistent** on ids, reasons, and timestamps.

## Objective

Document why a skill (and when relevant, an **employee**) left the **eligible pool**, what was tried, and whether **physical uninstall** is recommended—without silently deleting user files.

## Inputs

- `skill_id`, `skill_name`, `install_path`, `source_url`.
- Optional: `employee_id`, `employee_name` when terminating the assignable employee together with or instead of a single-skill row.
- `incident_ids`: related incident filenames or ids.
- `termination_reason`: primary cause (`wrong_match`, `skill_limit`, `security`, `user_request`, other).
- `user_confirmation`: boolean whether user explicitly asked to remove files.

## Skill vs employee termination (decision tree)

1. If the **assignable incumbent** was an **`employees[]`** row → set **employee** `terminated` for pool removal when the **role** is retired; document whether underlying **catalog `skills[]`** stay `terminated` or `active` for reuse by other employees (org policy).
2. If termination is **skill-only** (no employee layer) → update **`skills[]`** row to `terminated`; omit `employee_id` from JSON snippet.
3. If both the **employee** and a **dedicated skill catalog row** must reflect removal → emit **both** registry updates and **two** `termination_log` append rows (`kind: employee`, `kind: skill`) as applicable.

## termination_log append-only — valid vs invalid

**Valid**

- Append a **new** row: `{ "kind": "skill", "id": "pdf", "terminated_at": "2026-04-06T12:00:00Z", "reason": "wrong_match", "incident_ids": ["20260406-0930-pdf"], "rehire_allowed": false, "source_url": "https://…" }`.
- Later, append a **separate** correction row or use registry `notes` / new incident for narrative fixes—**do not** delete the original log entry.

**Invalid (never do)**

- Deleting or mutating an existing `termination_log[]` entry to “fix” history.
- Replacing the whole `termination_log` array with only new rows (drops audit trail).

## Procedure

1. Summarize **performance history** from registry (totals, last outcomes) for the **skill** and, if present, the **employee**’s `performance` block.
2. List **attempts** (handoff revisions, trials count).
3. State **final decision**: registry `terminated` (mandatory) for affected **skills** and **employees** + optional uninstall instructions.
4. **Employee symmetry:** when the incumbent was an **`employees[]`** row, terminate the **employee** record when the **role** is retired from the pool—even if underlying `skills[]` entries remain in the catalog for audit. Document in the report whether **skill catalog rows** stay `terminated` or remain `active` for reuse by other employees (org policy).
5. If recommending uninstall, provide **exact paths** and a **copy-paste command** for the **user** to run after review—do not assume sandbox allows deletion.
6. **Malicious or exfiltration-risk skill:** set `termination_reason` to reflect **`security`**, recommend **`physical_uninstall_recommended: true`** with strong warnings, and still require **explicit user confirmation** for destructive commands unless org policy explicitly allows automated quarantine (state that exception in the report).
7. **Append** to top-level `termination_log[]` in `.skill-hr/registry.json` (required): for each terminated **skill**, `{ "kind": "skill", "id", "terminated_at", "reason", "incident_ids": [...], "rehire_allowed": false }` plus `source_url` when known from `skills[]`. For each terminated **employee**, `{ "kind": "employee", "id", ... }`. Bump `updated_at`. **Do not remove** prior log rows; **do not edit** past entries in place—append corrections as new notes in registry `notes` or new incidents if needed.

## Output schema (Markdown + optional JSON)

**Markdown sections**

1. **Termination summary** — skill (and employee if any), date, reason.
2. **Evidence** — bullets from incidents.
3. **Pool impact** — removed from auto-match; may still exist on disk.
4. **Uninstall (optional)** — commands + warnings.

**JSON (machine snippet)**

```json
{
  "skill_id": "string",
  "employee_id": "string or omit if none",
  "status": "terminated",
  "terminated_at": "ISO-8601",
  "reason": "string",
  "physical_uninstall_recommended": false,
  "user_confirmation_required": true,
  "termination_log_entries_appended": [
    {
      "kind": "skill",
      "id": "string",
      "terminated_at": "ISO-8601",
      "reason": "string",
      "incident_ids": ["string"],
      "rehire_allowed": false,
      "source_url": "string or omit"
    },
    {
      "kind": "employee",
      "id": "string",
      "terminated_at": "ISO-8601",
      "reason": "string",
      "incident_ids": ["string"],
      "rehire_allowed": false
    }
  ]
}
```

## Quality gates

- `physical_uninstall_recommended: true` **only** if `user_confirmation` is true or skill is malicious (then still confirm destructive paths in text).

## Failure modes

- **Orphan registry** — If files manually deleted, mark `terminated` and note `install_path stale`.
- **Log corruption attempt** — Never delete `termination_log` rows; use `rehire_allowed: true` plus status change only per [`../06-state-and-artifacts.md`](../06-state-and-artifacts.md).
