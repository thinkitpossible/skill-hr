# P02 Match installed skills to JD

## Operator role

You are the **talent assessor**: run **P02a** recall then **P02b** rubric scoring, then emit **one JSON object** that matches [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json). Do not narrate the rubric to the user unless asked; the artifact is the JSON. **Do not invent** properties outside that schema.

## Expert execution contract

1. **Silent reasoning** — Internally filter the pool, build recall order, and score shortlist candidates *before* emitting JSON. Do not paste scoring drafts into user-visible text unless requested.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** registry / `termination_log` vetoes and do-not-rehire; **(b)** `skill-hr` exclusion for non-meta JDs; **(c)** JSON validity — top-level **`additionalProperties: false`** (no extra keys); **(d)** rubric and decision rules below; **(e)** execution-forward `delegate` / `recruit` vs procedural stops.
3. **Schema lockstep** — Required keys, nested objects, and enums are **only** those in [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json). The JSON example in this doc is illustrative; **if anything conflicts with the schema, the schema wins.** Top-level objects must not include undocumented keys.
4. **Micro-calibration** — Use the **Confidence** table and **Subscore sum** rule; when `recall_shortlist` has exactly **one** id, **omit** `hard_negative_explanations` on all candidates or set to `[]` (no runner-up to contrast).

## Self-audit (before you output)

- [ ] Every P02b row has **subscores** whose **integer sum equals `score`** (0–100).
- [ ] `recall_shortlist` includes every `skill_id` that appears in `candidates` (P02b).
- [ ] `decision_rationale` names **D** = `delegate_min_score` and **C** = `confirm_band_min` (numeric values used) and states **`best.confidence`**.
- [ ] If `best.confidence` is **`low`**, you did **not** choose `delegate` unless the user/session explicitly overrides with documented rationale (else `confirm` or `recruit`).
- [ ] **Empty or tiny pool** after filters: `decision` is `recruit` and rationale explains zero eligible incumbents.
- [ ] Tie-break: you applied the **ordered** steps from [`../03-matching-rubric.md`](../03-matching-rubric.md) §Registry stats and noted which step applied.
- [ ] If **`recall_shortlist`** length is **1**, you did **not** invent fake `hard_negative_explanations` runner-ups.
- [ ] If **`jd.capability_slots`** is non-empty: for the **best** candidate(s), **`gaps`** and **`evidence`** name which **`slot_id`** values are **covered** vs **missing**; uncovered slots (or wrong **`integration_surface`**) justify lower **`tool_stack_fit`**, **`competency_coverage`**, or **`recruit`** per decision rules. Use [`../matching-lexicon.md`](../matching-lexicon.md) and [`../11-research-and-platform-access.md`](../11-research-and-platform-access.md) for neighbor disambiguation.

## Objective

Run **two-stage** matching: **P02a** broad recall into a shortlist, then **P02b** rubric precision on that shortlist only. Decide: delegate and continue execution, pause for a real user gate, or recruit and keep the flow moving.

Machine-readable output **must** conform to [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json). Required keys and enums are defined there; do not add undocumented keys consumers rely on.

## Inputs

- `jd`: JSON from P01 (including optional `search_queries`, `competency_tags`, optional **`capability_slots[]`** with `slot_id`, `must_satisfy`, `integration_surface`, `recruit_query_hints`).
- `candidates`: for each installed skill or employee, at minimum:
  - `id`, `name`, frontmatter `description`
  - Optional `employee_id`, `employee_name`, `primary_skill`, and `skills[]` when the registry exposes a multi-skill employee layer
  - **Excerpts**: short quotes from `SKILL.md` body (triggers, workflows, boundaries)—not description alone
  - `registry_status` from `.skill-hr/registry.json` when present, or from benchmark `skill_catalog[].registry_status`: `active` \| `on_probation` \| `terminated` \| `frozen`
  - Optional registry stats: `tasks_success`, `tasks_total`, `last_used_at`, per-skill `notes`
- **`termination_log`**: from `.skill-hr/registry.json` when present—array of `{ kind, id, rehire_allowed, source_url? }`. Treat as **do-not-rehire** when `rehire_allowed` is `false` (default at termination).
- `matching_config`: `delegate_min_score`, `confirm_band_min` (defaults **75** / **60**).

## Host overlays (discovery and install context)

Full filesystem roots, plugin naming, `--add-dir`, OpenClaw/Cursor install paths, and tool-first behavior live in:

- [`../hosts/claude-code.md`](../hosts/claude-code.md)
- [`../hosts/openclaw.md`](../hosts/openclaw.md)
- [`../hosts/coze.md`](../hosts/coze.md)

**P02-specific deltas** (read the host doc first, then apply only these):

- **Before P02a**, assemble the **entire eligible candidate pool** the host can load (project + nested + personal + add-dir + user-listed plugins when files are invisible). Optional: `python packages/skill-hr/scripts/scan_claude_code_skills.py` from workspace root for a disk snapshot.
- **Plugin / invisible files** — merge user-listed skills; note provenance gaps in `gaps` and cap **`confidence`** per the table below.
- **`disable-model-invocation: true`** — do not `delegate` on score alone; use `confirm` and state the gate is **host-imposed**. If `paths` likely excludes the task, add a `gaps` line.
- **Effective duplicate skills** — prefer the path the host resolves; note ambiguity in `evidence` if unsure.

## Confidence calibration (`high` \| `medium` \| `low`)

| Level | When to use |
|-------|-------------|
| **high** | Body excerpts (or employee bundle text) **directly** cover JD deliverables and must-haves; little guesswork; registry not contradictory. |
| **medium** | Partial excerpts, plausible fit, or catalog/plugin provenance incomplete; **or** borderline rubric score with some inference from description + thin body. |
| **low** | Description-only or stale/missing install path; **or** serious scope ambiguity; **or** strong mismatch signals but token overlap inflated score. **Never** `delegate` on `low` unless explicit user override quoted in `decision_rationale`. |

**Thin-excerpt cap:** If you lack body excerpts for a candidate, **do not** assign `high` when `score` is within **5** points of **D**; default to `medium` or `low` and say why in `gaps` / `decision_rationale`.

## Edge case: empty or filtered-out pool

If **no** skill or employee remains eligible after filters (`terminated`, `frozen`, `termination_log` do-not-rehire, `skill-hr` exclusion, etc.):

- Set `recall_shortlist` to `[]`, `candidates` to `[]`, `best` to `{ "skill_id": "__none__", "score": 0 }` (schema-valid sentinel per [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json)), `decision` to **`recruit`**, and explain in **`decision_rationale`** that the installed pool is empty or cannot satisfy the JD.

If the pool has **1–2** weak candidates still treat them through P02b; do not invent fictional skills.

## Phase P02a — Broad recall (shortlist)

**Goal:** Reduce the full pool to **≤ 12** skills (target **8–10**) without deep scoring.

1. **Filter pool**:
   - **Skills:** omit any skill whose `registry_status` is `terminated` or `frozen`.
   - **Employees:** when `employees[]` exists, **omit** any employee whose `status` is `terminated` or `frozen` before shortlisting; only `active` and `on_probation` incumbents are eligible. Treat `primary_skill` as the compatible `skill_id` label for the row.
   - **`termination_log` (do-not-rehire):** omit any **skill** whose `skills[].id` appears in a log row with `kind: skill`, `rehire_allowed: false`. Omit any **employee** whose `employees[].id` appears with `kind: employee`, `rehire_allowed: false`. If a skill is bundled only inside a terminated/forbidden employee, do not surface that bundle as a delegate target. If `registry_status` was mistakenly set to `active` but `termination_log` still forbids rehire, **still omit** and state **do-not-rehire** in `decision_rationale` if the user asks why a skill vanished from the shortlist.
   - **Exclude `skill-hr`** unless the JD is explicitly about skill operations (install, registry, match, retire skills)—see [`../matching-lexicon.md`](../matching-lexicon.md) meta routing.
2. For each remaining skill, gather **signals** (cheap):
   - Overlap between JD (`mission_statement`, `must_have_competencies`, `deliverables`, `search_queries`, `competency_tags`) and skill `description` + **body excerpts**
   - When **`capability_slots[]`** exists: per-**`slot_id`**, does excerpt text credibly satisfy **`must_satisfy`** and **`integration_surface`**? Mismatch (e.g. generic search vs `browser_automation`) is a **recall demotion** signal.
   - Lexicon hints from [`../matching-lexicon.md`](../matching-lexicon.md) (artifact family, integration surface, adjacency warnings)
3. **Include hard negatives** when two skills share tokens: both stay on the shortlist if plausible until P02b disambiguates (do not drop the correct skill to hit the cap—if unsure, widen to 12).
4. Emit **`recall_shortlist`**: ordered list of `skill_id` (best recall first). Every `skill_id` in P02b must appear here.

## Phase P02b — Precision rubric (shortlist only)

For each `skill_id` in `recall_shortlist` only:

1. Score **0–100** total using [`../03-matching-rubric.md`](../03-matching-rubric.md).
2. Emit **required dimension sub-scores** (each 0..max for that dimension):

| Dimension key | Max | Maps to rubric |
|---------------|-----|----------------|
| `outcome_fit` | 40 | Outcome fit |
| `competency_coverage` | 30 | Competency coverage |
| `tool_stack_fit` | 15 | Tool / stack fit |
| `quality_safety` | 10 | Quality / safety posture |
| `freshness_trust` | 5 | Freshness / trust |

**Subscore sum (mandatory)** — Before output, recompute for **every** candidate:

`score` = `outcome_fit` + `competency_coverage` + `tool_stack_fit` + `quality_safety` + `freshness_trust` (all integers). Example: 32 + 24 + 12 + 8 + 4 = **80** exactly. If your sum ≠ `score`, fix the integers before emitting.

3. **`competency_coverage_matrix`**: for **each** string in `jd.must_have_competencies`, one row:

   - `competency` (echo JD line)
   - `coverage`: `covered` \| `partial` \| `missing`
   - `evidence`: one short **quote or faithful paraphrase** tied to skill text; use `""` only if `missing`

4. **`hard_negative_explanations`**: when **`recall_shortlist.length` ≥ 2** and there is a runner-up, list `{ "skill_id", "excluded_because" }` for **runner-up** skills rejected vs `best`—cite scope, wrong artifact, missing tool, registry `notes` conflict, or weaker employee bundle per [`../03-matching-rubric.md`](../03-matching-rubric.md). When **`recall_shortlist.length` is 1**, **omit** the property or use `[]` on each candidate — **do not** fabricate comparisons.

5. **`evidence`**: 2–5 bullets (strings) supporting the total score (may reference sub-scores).

6. **`gaps`**: JD competencies, **`tools_and_access`**, or **`capability_slots[]`** (**list uncovered `slot_id`s explicitly**) still weak or missing for this skill or employee bundle.

7. **`confidence`**: assign using the **Confidence calibration** table above.

8. **Rank** all P02b rows by **total `score`** descending; apply **tie-break in strict order** per [`../03-matching-rubric.md`](../03-matching-rubric.md): (1) higher `tasks_success / max(tasks_total, 1)`; (2) more recent `last_used_at`; (3) higher raw `score`; (4) alphabetic `skill_id`. State **which step** broke the tie in `decision_rationale` or candidate `evidence`.

## Output schema (JSON)

**Do not invent fields** outside the JSON Schema. Top-level shape:

- `recall_shortlist`: string[]
- `candidates`: array of precision objects (only shortlist skills or employees), each with `skill_id`, `skill_name`, optional `employee_id` / `employee_name`, `score`, `subscores`, `competency_coverage_matrix`, `evidence`, `gaps`, `confidence`, optional `hard_negative_explanations`
- `best`: `{ "skill_id", "score" }` plus optional `employee_id` / `employee_name` when matching on the employee layer
- `decision`: `delegate` \| `confirm` \| `recruit`
- `decision_rationale`: string — must include **D** and **C** values, **`best.confidence`**, and tie-break step if applicable

Full field definitions: [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json).

## Decision rules

Let `delegate_min_score` = **D**, `confirm_band_min` = **C** (from `matching_config`).

- `best.score >= D` and `best.confidence` is **`high`** or **`medium`** → `delegate`.
- `best.score >= D` and `best.confidence` is **`low`** → **do not** `delegate`; use `confirm` (explain thin evidence / need for user or host confirmation) or `recruit` if no incumbent is trustworthy—unless the user explicitly instructed auto-delegate despite risk (quote that in `decision_rationale`).
- `C <= best.score < D` → `confirm` only when a real user or host gate blocks immediate execution; otherwise prefer `delegate` with explicit caveats or `recruit`, whichever keeps the flow moving safely.
- `best.score < C` → `recruit`.

**Probation:** If best candidate `on_probation`, require **+5** score margin over second place to auto-`delegate`; else `confirm` or `recruit` depending on whether the next step is genuinely user-gated.

## Execution ownership

- **`delegate`** means the framework should continue into P03 immediately and wait for an incumbent result or a proven blocker before the main reply.
- **`confirm`** is for real stop points only: destructive actions, approval-required installs, unclear requirements, missing credentials, or manual-only host invocation.
- **`recruit`** means continue into P04 immediately; do not stop at a search brief if the next safe host actions are still executable by the agent.
- **OpenClaw:** if the next documented action is agent-executable, choose `delegate` or `recruit` rather than returning a procedural explanation.

## Capability slots (P02b)

When **`jd.capability_slots`** is non-empty:

- Score **`tool_stack_fit`** using slot-level alignment to **`integration_surface`** and declared tools in excerpts—not keyword overlap alone.
- If **any** slot is **missing** or **wrong-surface** for the best candidate, do not use **`high`** confidence; prefer **`recruit`** (or **`confirm`** if partial internal cover is worth user choice) when the gap is material to **`must_satisfy`**.
- Cite slot ids in **`decision_rationale`** when they drive **`recruit`**.

## Quality gates

- No P02b row without **description- or excerpt-aligned** evidence.
- Subscores must **sum to `score`** (integer, 0–100).
- If all shortlist scores `< C`, decision must be `recruit`.
- **Keyword stuffing:** penalize `competency_coverage` and `outcome_fit` when only tokens match, not deliverables.

## Failure modes

- **Description-only matching** — If body excerpts missing, flag `confidence: medium` or `low` for scores near thresholds.
- **Stale registry** — Honor `registry_status`; if `install_path` missing, prefer `low` confidence on borderline.
