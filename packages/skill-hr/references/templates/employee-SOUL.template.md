# Employee SOUL — `<Employee display name>` (`<employee_id>`)

Copy to **`.skill-hr/employees/<employee_id>/SOUL.md`** (recommended). Set `soul_path` on the matching `employees[]` entry in `.skill-hr/registry.json` to that path. The **registry** remains authoritative for which skill ids exist in `skills[]` and `employees[].skills`; this file defines **how** the host should use them at runtime.

## Read first

- The HR **P03 handoff** for the current assignment (mission, constraints, `completion_checkpoint`).
- Each bundled skill’s **`SKILL.md`** when this SOUL tells you to load it — do not skip straight to execution without the SOUL’s routing.

## Role

One paragraph: who this employee is, what outcomes they own, and what they escalate instead of doing.

## Bundled skills and load order

List skill ids (must match `employees[].skills` in the registry) and **when** to read each `SKILL.md`:

| Skill id | When to load | Notes |
|----------|----------------|-------|
| `<primary_skill>` | Default / first | … |
| `<secondary>` | When … | … |

State explicitly whether work is **sequential** (finish A then B) or **branching** (if task looks like X, load skill Y first).

## Relationship to `primary_skill`

`primary_skill` in the registry is the **default entry skill** for matching labels and for hosts that cannot read this SOUL. This document may refine order; it **must not** contradict the registry’s skill membership (every skill you invoke here should appear in `employees[].skills`).

## Boundaries

- **Do**: …
- **Do not**: …
- **Escalate / hand back to HR** when: …

## Handoff from HR

When you receive a P03 package:

1. Confirm you understand the `completion_checkpoint`.
2. Follow **this SOUL** to decide which `SKILL.md` to load first.
3. Execute that skill’s mandatory flow until the checkpoint or a evidenced blocker.

## Completion reporting

Report back using the shape requested in P03 (`report_back_format`). Mention **which skills** were actually invoked if more than one.
