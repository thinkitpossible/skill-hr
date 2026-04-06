# Matching rubric (installed pool)

## Scoring dimensions (0–100 total)

When `registry.json` contains `employees[]`, score the **employee bundle** first and use `primary_skill` as the short label for the P02 record. Keep `skill_id` for compatibility, but the actual routing target may be a multi-skill employee.

Allocate points and **document sub-scores** on every P02b row (`subscores` in JSON). Sub-scores **must sum** to total `score`.

| Dimension | Max points | JSON key | Guidance |
|-----------|------------|----------|----------|
| Outcome fit | 40 | `outcome_fit` | Employee or skill text covers the **same deliverables** as the JD, not just shared keywords |
| Competency coverage | 30 | `competency_coverage` | Each `must_have` mapped in coverage matrix; multi-skill coverage is allowed when one employee owns the bundle |
| Tool / stack fit | 15 | `tool_stack_fit` | Languages, CLIs, MCP, browsers align with `tools_and_access` and, when present, **`jd.capability_slots[]`** **`integration_surface`** + **`must_satisfy`** per slot (see [`prompts/P02-match-installed.md`](prompts/P02-match-installed.md) §Capability slots) |
| Quality / safety posture | 10 | `quality_safety` | Validation, scope discipline, safe patterns in skill text |
| Freshness / trust | 5 | `freshness_trust` | Maintainer signal, narrow scope, no red flags |

## Default thresholds

Stored in `registry.json` → `matching`:

- **`delegate_min_score`**: 75 — route with P03 and continue execution to a completion checkpoint.
- **`confirm_band_min`**: 60 — reserve for true user gates such as destructive actions, unclear ownership, or required approval.
- Below **60** — recruit (P04).

Override per org: lower delegate only if incidents show low false positives.

## Decision semantics

- **`delegate`** means the framework owns dispatch: prepare P03, invoke the incumbent when the host allows it, wait for a completion checkpoint, then continue into P05 before the main reply.
- **`confirm`** is not the default "recommendation" band. Use it only when the flow truly needs user input to continue: destructive or costly actions, ambiguous ownership, unclear JD, missing access, or host-specific manual-only invocation.
- **`recruit`** means proceed to P04 and keep executing the recruitment flow until a real approval gate or blocker is reached.
- **OpenClaw:** prefer `delegate` or `recruit` over `confirm` whenever the next documented step is agent-executable.
- **Claude Code:** manual-first rules in `hosts/claude-code.md` still apply when a skill cannot be safely auto-invoked.

## Hard negatives and near-neighbor disambiguation

When two+ skills share vocabulary or stack, **do not** split the tie on keyword count alone.

1. **Outcome vs tooling** — Penalize if the skill optimizes for the **wrong primary artifact** (e.g. longform SEO article skill for an **audit** JD).
2. **Review vs implement** — Security **review** skills lose to implementation skills if the JD demands shipping code; the converse if the JD asks for findings only.
3. **Meta vs domain** — `skill-hr` must not win business JDs; domain skills must not win **skill workforce** JDs (see [`matching-lexicon.md`](matching-lexicon.md)).
4. **Candidate-side vs hiring-manager** — Resume **writing** ≠ interview **design** from a resume.
5. **Record `hard_negative_explanations`** in P02 output for runner-ups: one line **why** the higher-scoring neighbor is rejected (scope, missing MCP, wrong vendor API, etc.).
6. **Employee vs loose handoff chain** — Prefer one employee that credibly covers the JD with a coherent skill bundle over a brittle sequence of unrelated single-skill hops, unless the bundle adds clear safety risk.

## Registry `notes` and empirical stats

- Read **`skills[].notes`** in `registry.json` when present: treat as HR annotations (e.g. “strong for forms, weak for OCR”)—adjust `competency_coverage` or `outcome_fit` and cite in evidence.
- **Tie-breakers** (in order): higher `tasks_success / max(tasks_total, 1)`; more recent `last_used_at`; higher raw `score`; alphabetic `skill_id`.
- When breaking a tie, add one sentence to **`decision_rationale`** or per-candidate evidence stating **which tie-break step** decided (for auditability).

## Probation adjustments

- If candidate `status: on_probation`, require **+5 score margin** over second place to auto-delegate; else `confirm`.

## Exclusions

- `terminated`, `frozen`: score = N/A, omit from ranking.
- `skill-hr`: exclude from business JD matching (meta-tasks only).

## Example evidence line

> "Description states 'comprehensive PDF manipulation' and lists form filling; JD requires PDF form extraction—strong outcome fit (+36/40)."
