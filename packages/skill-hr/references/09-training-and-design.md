# Training and employee design

## Purpose

Use this reference when Skill HR needs to create, retrain, or redesign a workforce employee instead of merely choosing an existing skill.

This workflow exists because:

- a business need may require a **bundle** of skills, not one incumbent
- a previously hired employee may need retraining after poor outcomes
- host differences can require a different employee composition on Claude Code vs OpenClaw

## Design outputs

Every employee design should produce:

1. `employee_id`
2. `name`
3. `role_title`
4. `host`
5. `primary_skill`
6. `skills[]`
7. `created_by`
8. `status` at creation time, usually `on_probation`
9. a short `notes` field
10. at least one `training_history[]` event

## When to invoke the trainer

Invoke `trainer` when any of these is true:

- no existing employee covers the JD well enough
- the JD clearly spans multiple competencies that should live in one worker
- repeated debriefs suggest a prompt, host, or skill-bundle redesign
- the user explicitly asks to design, train, or evolve an employee

## Training states

Use these task-board states when the design loop matters:

- `Designing`
- `Training`
- `TrainingReview`

Typical flow:

```text
Intake -> Designing -> Training -> TrainingReview -> Matched
```

If review fails:

```text
TrainingReview -> Designing
```

## Decision guide

### Train from existing skills

Choose this when the required skill bundle is already present in `skills[]` and the work is mostly about composition, SOUL design, and onboarding.

### Recruit new skills

Choose this when the required bundle depends on capabilities that do not exist in the current catalog. Recruitment still routes through `recruiter` and `compliance`.

### Retrain an existing employee

Choose this when the employee is directionally correct but underperforming due to:

- weak prompt framing
- poor host fit
- missing one adjacent skill
- an outdated SOUL or operating boundary

## Training plan minimum

Every training plan should include:

1. role purpose
2. chosen host and why
3. skill bundle and why each skill is included
4. SOUL or prompt changes
5. a smoke task
6. promotion criteria from probation
7. failure criteria that trigger redesign or termination review

## Recording into the registry

At minimum append one `training_history[]` entry:

```json
{
  "ts": "2026-04-05T12:00:00Z",
  "action": "created",
  "trainer_id": "trainer",
  "notes": "Designed a document operations employee from pdf + docx + xlsx."
}
```

Common actions:

- `created`
- `skill_added`
- `skill_removed`
- `retrained`
- `promoted_from_probation`
- `frozen_for_review`

## Safety

- Do not let `trainer` become a shortcut around recruitment vetting.
- Do not mark a new employee `active` before a documented smoke success unless the user explicitly accepts the risk.
- Do not overwrite old training history; append new events.
