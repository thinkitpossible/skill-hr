# P05 Trial and debrief (post-task)

## Objective

Classify **outcome**, attribute **root cause**, decide **next_action** for the skill, and write the incident record + registry deltas. A procedure description without execution evidence is not a success.

## Inputs

- `jd`: P01 JSON.
- `handoff`: P03 output summary.
- `incumbent_report`: structured or free-form result from the skill run.
- `registry_entry`: prior stats for the skill, if any.
- `max_trials_per_task_per_skill`: from registry matching config.

## Procedure

1. Verify the incumbent reached a **completion checkpoint** or produced a proven blocker with evidence.
2. Map deliverables to **success_criteria**; label `outcome`: `success` \| `partial` \| `fail`.
3. Choose **root_cause_class**:
   - `skill_limit` — skill scope insufficient or wrong workflow.
   - `user_spec` — unclear/moving requirements.
   - `environment` — tooling, auth, network, permissions.
   - `wrong_match` — HR mis-assigned; different competency needed.
   - `n/a` — only if `success`.
4. Choose **next_action**:
   - `retain` — update counters; keep `active`.
   - `retrain_prompt` — same skill, revised handoff (count trial; stop at max).
   - `terminate` — set registry `terminated`; remove from pool; **no filesystem delete** without user OK.
   - `escalate` — human decision or different domain; see `references/07-escalation.md`.
5. If the incumbent only explained steps, classify as `partial` or `fail` unless a policy gate prevented execution and the blocker is evidenced.
6. If `partial`, prefer `retrain_prompt` once; then `escalate` or `terminate` per user preference.
7. Emit **incident** body + YAML frontmatter per `references/06-state-and-artifacts.md`.
8. Update **registry** counters: `tasks_total++`, `tasks_success` or `tasks_fail` per rules in `references/05-performance-and-termination.md`.

## Output schema (JSON)

```json
{
  "outcome": "success|partial|fail",
  "root_cause_class": "skill_limit|user_spec|environment|wrong_match|n/a",
  "next_action": "retain|retrain_prompt|terminate|escalate",
  "completion_evidence": ["string"],
  "incident_markdown": "string",
  "registry_patch": {
    "skill_id": "string",
    "status": "active|on_probation|terminated|frozen",
    "tasks_total_delta": 1,
    "tasks_success_delta": 0,
    "tasks_fail_delta": 0,
    "last_used_at": "ISO-8601"
  },
  "user_message": "string"
}
```

## Quality gates

- Do not `terminate` on a single `environment` failure unless user directs or skill is clearly malicious/low-value.
- **Trials**: increment a task-local counter; if &gt; `max_trials_per_task_per_skill`, switch to `escalate`.
- A completion claim must cite concrete evidence: artifacts, commands, tests, or observed host state.

## Failure modes

- **False success** — If criteria unmet but report claims done, set `partial` or `fail` and document gaps.
- **Double counting** — Ensure registry deltas applied once per completed assignment.
- **Procedure-only report** — "Here is how I would do it" is not success evidence; route to `retrain_prompt` or `escalate`.
