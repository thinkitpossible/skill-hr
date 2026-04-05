# P08 Training plan

## Objective

Turn an employee design into a concrete training or retraining plan that can be executed and audited.

## Inputs

- `employee_design`
- `jd`
- `registry`
- optional `incident_context`

## Procedure

1. Identify the exact skills, prompts, and host setup needed.
2. Define a smoke task that proves the employee can do meaningful work.
3. Set promotion criteria from `on_probation` to `active`.
4. Define what outcome triggers redesign, freeze, or termination review.
5. Add one or more `training_history[]` events that should be written after execution.

## Output schema

```json
{
  "employee_id": "string",
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
