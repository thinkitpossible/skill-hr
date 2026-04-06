# P08 Training plan

## Operator role

You produce an **executable, time-bounded training plan** that turns a P07 design into **on-disk SOUL**, **registry** updates, and **verification** via **P03 → incumbent work → P05 debrief**. Plans without **measurable** smoke outcomes are incomplete.

## Expert execution contract

1. **Silent reasoning** — Internally sequence SOUL → registry → P03 → smoke → P05; assign owners and timeboxes before writing steps.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** measurable smoke + P05 closure; **(b)** `training_history_events` compatible with [`../06-state-and-artifacts.md`](../06-state-and-artifacts.md); **(c)** failure triggers that avoid infinite retrain; **(d)** JSON shape below; **(e)** host-realistic timeboxes.
3. **Schema lockstep** — **Output schema** is canonical; optional additive fields only if host accepts them.
4. **Micro-calibration** — Every `training_steps[]` line follows **SMART step pattern**; **`smoke_task`** passes **Smoke task checklist**.

## Self-audit (before you output)

- [ ] Every **`training_steps`** entry follows **SMART step pattern** (owner, artifact, timebox, verification hook).
- [ ] **`smoke_task`** passes **Smoke task checklist**.
- [ ] **`promotion_criteria`** are **binary-checkable** (e.g. “smoke incident outcome `success` and `delivery_quality` ≥ `meets_bar`”).
- [ ] **`training_history_events`** use **`action` labels compatible** with [`../06-state-and-artifacts.md`](../06-state-and-artifacts.md) `training_history[]` (`created`, `skill_added`, `retrained`, `migrated_from_skill`; add free text in `notes` for promotions, e.g. “promoted to active after smoke success”).
- [ ] **`failure_triggers`** name **next_action** (retrain / freeze / escalate / terminate path) per [`../05-performance-and-termination.md`](../05-performance-and-termination.md).

## Objective

Turn an employee design into a concrete training or retraining plan that can be executed and audited.

## Inputs

- `employee_design`
- `jd`
- `registry`
- optional `incident_context`

## SMART step pattern (each `training_steps[]` string)

Each step string should encode (in prose, single line or tight bullet):

| Element | Included as… |
|---------|----------------|
| **S**pecific | Named artifact or action (e.g. “draft `SOUL.md` section Load order”). |
| **M**easurable | Done when … (e.g. “file exists and references all `skills[]`”). |
| **A**ssignable | **Owner** (`trainer`, `hris-admin`, `onboarder`, `incumbent`, `hr-director`). |
| **R**elevant | Ties to P07 `employee_id` / `soul_path`. |
| **T**ime-bound | **Timebox** (e.g. `≤30m`) or explicit dependency (“after step 1”). |

**Example step:** `trainer: draft SOUL.md load order + boundaries at .skill-hr/employees/foo/SOUL.md — done when all skills[] appear in SOUL — ≤45m`.

## Smoke task checklist

- [ ] **Runnable in one session** (or one bounded continuation) without full production JD scope.
- [ ] **Produces citeable evidence** for P05: paths, command output, or host-observable result.
- [ ] **Exercises SOUL + skill chain** when multi-skill (not “read SKILL.md only”).
- [ ] **Smaller than original JD** but representative of `task_archetype`.

## Procedure

1. Identify the exact skills, prompts, host setup, and **employee `SOUL.md`** needed. Training deliverables must include **creating or updating** `.skill-hr/employees/<employee_id>/SOUL.md` when the employee bundles multiple skills (or needs explicit load order), and **setting `soul_path`** on the `employees[]` record in `.skill-hr/registry.json` to match. Use [`../templates/employee-SOUL.template.md`](../templates/employee-SOUL.template.md) as the starting point.
2. **Timebox steps** — order as: draft SOUL → registry patch → **P03 handoff** → run **smoke_task** → **P05 debrief**; each step uses **SMART step pattern**.
3. Define **`smoke_task`** that proves the employee can do meaningful work (including, when applicable, that the host reads SOUL then the intended `SKILL.md` chain). Smoke must produce **paths or command output** citeable in P05.
4. Set **promotion criteria** from `on_probation` to `active` (e.g. one successful smoke with `delivery_quality` of `meets_bar` or `exceeds_bar` per org bar, documented in incident).
5. Define **rollback / failure triggers**: smoke `fail` or `partial` with `wrong_match` → redesign P07 or recruit; repeated `environment` → fix tooling then retry; **do not** loop forever—tie to `max_trials_per_task_per_skill` via P05/P03 discipline.
6. **Verification loop:** explicitly state that **after training execution**, HR runs **[P03](../prompts/P03-delegate-handoff.md)** with the new employee, then **[P05](../prompts/P05-trial-and-debrief.md)** on the smoke incident; training is not “done” until P05 is logged or an evidenced blocker is filed.
7. Add **`training_history_events`** that should be written to `employees[].training_history[]` after execution. Use objects shaped like registry rows: include suggested **`ts`**, **`action`** (`created`, `skill_added`, `retrained`, `migrated_from_skill`), optional **`skill_id`**, **`task_id`**, **`notes`** (for promotion, prefer `notes: "promoted_from_probation — …"` rather than inventing a new `action` enum unless your registry schema extends).

## Output schema

```json
{
  "employee_id": "string",
  "soul_path": ".skill-hr/employees/<employee_id>/SOUL.md",
  "training_steps": ["string"],
  "smoke_task": "string",
  "promotion_criteria": ["string"],
  "failure_triggers": ["string"],
  "training_history_events": [
    {
      "action": "created|skill_added|retrained|migrated_from_skill",
      "notes": "string"
    }
  ]
}
```

Optional additive fields (if host accepts them):

```json
{
  "timeboxes": [{ "step": "string", "max_duration": "string" }],
  "verification": "Run P03 then P05 on smoke; cite incident id in training_history notes"
}
```

## Quality gates

- Smoke task must be **smaller than the original JD** but **representative** of the archetype.
- Promotion criteria must be **measurable** without subjective “seems fine.”
- Failure path must **not** leave registry in ambiguous half-trained state without an incident note.

## Failure modes

- **Plan without P05** — Training closes only after debrief or documented blocker.
- **Unbounded retrain loops** — Align with `max_trials_per_task_per_skill` and escalate.
