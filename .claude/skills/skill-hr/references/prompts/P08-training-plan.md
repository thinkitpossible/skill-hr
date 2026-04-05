# P08 Training plan

## Objective

Turn an employee design into a concrete training or retraining plan that can be executed and audited.

## Inputs

- `employee_design`
- `jd`
- `registry`
- optional `incident_context`

## Procedure

1. Identify the exact skills, prompts, host setup, and **employee `SOUL.md`** needed. Training deliverables must include **creating or updating** `.skill-hr/employees/<employee_id>/SOUL.md` when the employee bundles multiple skills (or needs explicit load order), and **setting `soul_path`** on the `employees[]` record in `.skill-hr/registry.json` to match. Use `references/templates/employee-SOUL.template.md` as the starting point.
2. Define a smoke task that proves the employee can do meaningful work (including, when applicable, that the host reads SOUL then the intended `SKILL.md` chain).
3. Set promotion criteria from `on_probation` to `active`.
4. Define what outcome triggers redesign, freeze, or termination review.
5. Add one or more `training_history[]` events that should be written after execution.

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
      "action": "created|skill_added|retrained|promoted_from_probation",
      "notes": "string"
    }
  ]
}
```
