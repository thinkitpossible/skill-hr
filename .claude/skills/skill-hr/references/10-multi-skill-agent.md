# Multi-skill employee model

## Why this exists

`skill-hr` originally tracked a **skill pool** only. That was enough for simple matching, but it does not model how a real employee can combine multiple skills, be trained over time, or move across hosts.

This reference adds a second layer:

- `skills[]` = the **shared catalog** of installable capabilities
- `employees[]` = the **assignable workforce** built from one or more skills

Use `employees[]` as the preferred assignment surface when it exists.

## Core concepts

### Skill catalog

A skill remains the smallest reusable capability unit. Keep provenance, install hints, and skill-level trust notes in `skills[]`.

Examples:

- `pdf`
- `docx`
- `security-auditor`
- `frontend-design`

### Employee

An employee is the runtime worker HR can actually assign. It may be:

- a migrated single-skill incumbent (`skills: ["pdf"]`)
- a trained multi-skill worker (`skills: ["pdf", "docx", "xlsx"]`)
- a cross-host worker registered on a specific runtime

Minimum employee shape:

```json
{
  "id": "document-ops-01",
  "name": "Document Operations Specialist",
  "status": "active",
  "skills": ["pdf", "docx", "xlsx"],
  "primary_skill": "pdf",
  "host": "claude-code",
  "created_by": "trained",
  "performance": {
    "tasks_total": 9,
    "tasks_success": 8,
    "tasks_fail": 1
  },
  "training_history": []
}
```

Optional: add **`soul_path`** (e.g. `.skill-hr/employees/document-ops-01/SOUL.md`) so hosts know where the employee’s orchestration brief lives. Template: [`references/templates/employee-SOUL.template.md`](templates/employee-SOUL.template.md).

Optional registry field **`task_archetype`** (string): one-line label for the **class of user tasks** this employee serves (keep aligned with `role_title` / `notes`). See `schemas/registry-v2.schema.json` and `references/06-state-and-artifacts.md`.

## Task-type specialization (task archetype)

Each `employees[]` row should be a **task-type specialist**: one **primary class of work** (the **task archetype**), not a grab bag of unrelated missions.

1. **Declare the archetype** — In prose (`notes`, `role_title`, optional `task_archetype`) and in the per-employee SOUL (**Task archetype** section in the template), state the **single main scenario** this employee is for. If the host must cover multiple unrelated scenarios, prefer **multiple employees** or **separate P01 `workstreams[]`**, each staffed to a specialist.
2. **Skill closure** — For that archetype, list every **must-have capability** (competencies, deliverable shapes, tooling). **Each** must map to a **real** `skills[].id` in `employees[].skills`. The bundle is the **closure** for the archetype: executing typical tasks in that class should not routinely force mid-task handoffs because a skill is missing.
3. **Anti-patterns** — Do not inflate `skills[]` unrelated to the archetype just to raise P02 scores. Do not omit a skill that is **routinely** needed for the archetype (that causes churn and re-recruitment). The employee SOUL should document **which skill covers which capability** (see template **技能闭包声明**).

**Trainer** and **employee-fabricator** (see `references/09-training-and-design.md`, `references/prompts/P07-design-agent.md`): when creating or extending an employee, produce a written **closure checklist** — task archetype → required capabilities → skill id per row — and ensure the draft `skills[]` and SOUL match it before handoff.

## Employee SOUL contract

The **employee SOUL** (`SOUL.md` at `soul_path`) is the runtime brief for **multi-skill composition**. The registry answers *what* skills belong to the employee; the SOUL answers *how* the incumbent should **load and apply** those `SKILL.md` files (order, branching, fallbacks).

### What the SOUL must contain

1. **Identity** — role, scope, tone consistent with HR’s `role_title` / `name`.
2. **Skill bundle alignment** — every skill the SOUL instructs the host to use must appear in `employees[].skills` (and exist in `skills[]`).
3. **Load order and rules** — when to read which `SKILL.md` first; sequential vs conditional paths; when to switch skills mid-task.
4. **`primary_skill` relationship** — `primary_skill` remains the default label for P02/P03 compatibility and for hosts that only load one skill; the SOUL may override sequencing but must not invent skills not in the registry bundle.
5. **Boundaries** — explicit do / do-not / escalate rules so multi-skill breadth does not become scope creep.

### When `soul_path` is missing (fallback)

If no `soul_path` is set, treat the employee as **single-primary-skill execution**: load the `primary_skill`’s `SKILL.md` only, same as a legacy one-skill incumbent. Secondary skills in `skills[]` are still true for matching and HR narrative but are not auto-invoked unless the host or user explicitly loads them.

### Delegation with SOUL

P03 must tell the incumbent to **read the employee SOUL first** (when present), then follow it to load the right domain `SKILL.md` files. The completion checkpoint may be defined in P03 or reinforced in the SOUL; if both exist, **P03 wins** for the current assignment unless the SOUL explicitly defers to the handoff.

## Workstreams vs one bundled employee

When P01 produces **`workstreams[]`**:

- **Multiple incumbents / handoffs** — Use separate streams when **separation of concerns** matters (e.g. compliance vs implementation), **different completion checkpoints**, or when parallelizing reduces calendar time without shared context. Prefer **one task-type employee per stream** (each with its own **skill closure** for that stream’s archetype) when streams correspond to different missions.
- **One employee + `soul_path`** — Prefer a **single** multi-skill employee when the same thread should **retain context** across skills, handoffs would lose state, or the “employee” is really **one** task archetype whose closure is exactly the bundled skills with a defined load order in SOUL.

If unsure, favor **streams** when failure modes are independent; favor **bundle + SOUL** when integration and narrative continuity dominate **and** the work still fits **one** task archetype.

## Matching rules

When `employees[]` exists:

1. Match the JD against the **employee skill bundle**, not only a single skill.
2. Give extra credit when one employee covers multiple must-have competencies without requiring handoffs.
3. Penalize bundles with large unused surface area only when that extra surface adds meaningful safety or scope risk.
4. Keep `primary_skill` as the short label for evidence and onboarding, but cite additional skills when they materially improve coverage.

When `employees[]` is absent:

1. Build synthetic employees from `skills[]`.
2. Set `created_by: migrated`.
3. Copy counters and notes from the source skill.

## Delegation rules

P03 handoffs should name:

- the selected employee id and display name
- the primary skill being leaned on
- any secondary skills expected to help
- the completion checkpoint

Do not expose internal scoring just because the employee uses multiple skills.

## Performance rules

- Employee performance lives in `employees[].performance`.
- Skill-level counters in `skills[]` may continue to exist for legacy tooling and audit views.
- When both are updated, treat employee counters as the **assignment truth** and skill counters as supporting telemetry.

## Training rules

Training changes should append to `training_history[]` with:

- timestamp
- action
- optional trainer id
- optional affected skill id
- notes

Common actions:

- `created`
- `migrated_from_skill`
- `skill_added`
- `skill_removed`
- `retrained`
- `promoted_from_probation`

## Host rules

- `host` is the runtime home for the employee: `claude-code`, `cursor`, `openclaw`, or `unknown`.
- One skill catalog entry may be referenced by multiple employees on different hosts.
- Host adapters should keep employee ids stable even if install paths differ.

## Anti-patterns

- **Employee equals folder name only**: a host folder may store skills, not the worker abstraction.
- **Duplicate employee records for every task**: reuse ids across assignments and track history instead.
- **Multi-skill by string stuffing**: do not pretend an employee is multi-skill unless each referenced skill is real and available in `skills[]`.
- **One employee, many unrelated archetypes**: do not use one SOUL or one registry row to cover unrelated task classes; split employees or use `workstreams[]`.
- **Incomplete closure**: do not assign an employee to an archetype when `skills[]` omits a routinely required capability for that archetype.
