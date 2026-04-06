# Performance, probation, and termination

## KPIs (lightweight)

Tracked in `registry.json` per skill, and in v2 primarily per employee:

- `tasks_total` — completed assignments (success + fail + partial counted once each completion).
- `tasks_success` — P05 `outcome: success`.
- `tasks_fail` — P05 `outcome: fail` with `root_cause_class` in `skill_limit` or `wrong_match` (configurable).

When `employees[]` exists, treat employee-level performance as the assignment truth and skill-level counters as supporting telemetry.

**Partial** outcomes: increment `tasks_total`; do not increment `tasks_success` unless user accepts partial as success (document in incident).

## Delivery quality (P05)

`delivery_quality` is **not** a substitute for `outcome`; it describes how richly the incumbent met the bar when work was delivered.

- **`exceeds_bar`** — Strong signal for promoting `on_probation` → `active` when combined with `outcome: success` (org may still require a fixed number of successes).
- **`minimal_compliance`** on repeated debriefs — Prefer extra debrief detail, `retrain_prompt`, or `on_probation` tightening; do not treat as full performance credit for high-trust delegation.

## Probation rules

- New external hires default to `on_probation`.
- Promote to `active` after **1** documented success on a non-trivial criterion (or **2** if org is risk-averse—state in registry `notes`).
- If **two consecutive** failures with `wrong_match` or `skill_limit`, set `terminated` unless user overrides.

## Termination (pool removal)

**Always**:

1. Set `status: terminated` in registry for the skill and, when the assignment used `employees[]`, the employee record.
2. **Append** to `termination_log[]` in `.skill-hr/registry.json` (see `06-state-and-artifacts.md`): one entry per terminated skill (`kind: skill`) and one per terminated employee (`kind: employee`) with `rehire_allowed: false`, `terminated_at`, `reason`, and `incident_ids` when known. Optional `source_url` on skill rows for P04 dedupe.
3. Write P06 report and link incidents.
4. Exclude from P02 and P04 shortlists while `rehire_allowed` is false **or** status is `terminated`/`frozen` (see `prompts/P02-match-installed.md`, `04-market-recruitment.md`). To rehire: set `rehire_allowed: true` on the latest relevant log entry (or add a clarifying note), set `status` back to `active` or `on_probation`, and document rationale in `notes`.

**Physical uninstall** (optional):

- Only with **explicit user confirmation** and a path audit.
- Never delete skills outside the user's skills directories (e.g. system or shared plugins).

## Retrain vs terminate

- **`environment`** failures: prefer fix + retry; do not terminate the skill.
- **`user_spec`** failures: prefer clarification and P03 revision; do not terminate unless repeated scope mismatch after documented warnings.
- **`wrong_match`**: terminate quickly after `max_trials_per_task_per_skill` exhausted.

## Trial limits

`matching.max_trials_per_task_per_skill` (default **2**) counts P03 iterations for **same skill_id** on **same incident thread**. After exceeded → `escalate` or recruit replacement.

## Frozen state

Use `frozen` for:

- Pending security review
- License uncertainty
- User asked to pause a skill without deleting history

Frozen skills are skipped in P02 like terminated, but are visible for audit.
