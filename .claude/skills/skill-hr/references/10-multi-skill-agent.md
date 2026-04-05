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
