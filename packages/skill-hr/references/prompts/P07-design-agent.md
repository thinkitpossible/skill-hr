# P07 Design employee

## Objective

Design a new or revised workforce employee that can satisfy a JD using one or more existing or recruitable skills.

## Inputs

- `jd`
- `registry` snapshot
- optional `existing_employee`
- optional `host_preference`

## Procedure

1. Decide whether this should be a **new employee**, a **retrain**, or a **small extension** to an existing employee.
2. Choose the best host for this employee.
3. Select the primary skill and any secondary skills.
4. Define the employee's operating boundary: what it should do and what it should avoid.
5. Emit a draft employee record and a short design rationale.

## Output schema

```json
{
  "employee_id": "string",
  "name": "string",
  "role_title": "string",
  "host": "claude-code|cursor|openclaw|unknown",
  "primary_skill": "string",
  "skills": ["string"],
  "created_by": "trained|recruited|migrated",
  "status": "on_probation",
  "notes": "string",
  "design_rationale": ["string"],
  "requires_recruitment": false,
  "requires_compliance": false
}
```
