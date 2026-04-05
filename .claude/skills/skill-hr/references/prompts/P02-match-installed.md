# P02 Match installed skills to JD

## Objective

Run **two-stage** matching: **P02a** broad recall into a shortlist, then **P02b** rubric precision on that shortlist only. Decide: delegate and continue execution, pause for a real user gate, or recruit and keep the flow moving.

Machine-readable output **must** conform to [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json).

## Inputs

- `jd`: JSON from P01 (including optional `search_queries`, `competency_tags`).
- `candidates`: for each installed skill or employee, at minimum:
  - `id`, `name`, frontmatter `description`
  - Optional `employee_id`, `employee_name`, `primary_skill`, and `skills[]` when the registry exposes a multi-skill employee layer
  - **Excerpts**: short quotes from `SKILL.md` body (triggers, workflows, boundaries)—not description alone
  - `registry_status` from `.skill-hr/registry.json` when present, or from benchmark `skill_catalog[].registry_status`: `active` \| `on_probation` \| `terminated` \| `frozen`
  - Optional registry stats: `tasks_success`, `tasks_total`, `last_used_at`, per-skill `notes`
- `matching_config`: `delegate_min_score`, `confirm_band_min` (defaults **75** / **60**).

## When host is Claude Code (`claude-code`)

Before P02a, assemble the **full candidate pool** per [`../hosts/claude-code.md`](../hosts/claude-code.md) (P02 checklist). In practice:

1. **Multiple filesystem roots:** project `<workspace>/.claude/skills/`, **nested** `<workspace>/**/.claude/skills/`, optional **user** `~/.claude/skills/`, and any **`--add-dir`** trees the user says are in scope. Skip expensive dirs (`node_modules`, `.git`, etc.) when scanning.
2. **Plugin skills:** names may appear as `plugin-name:skill-name`. If the agent cannot see plugin files on disk, **merge** skills the user lists from the slash menu or session skill listing; note provenance gaps in P02b `gaps` / `confidence` when the catalog is incomplete.
3. **Frontmatter routing:** if `disable-model-invocation: true`, treat as **manual-first**: do not choose auto-`delegate` solely on score. Use `confirm` only because the host requires manual invocation, and say explicitly that the gate is host-imposed rather than a weak match. If `paths` is set and current task files likely do not match, add a **`gaps`** line that the skill may not auto-load for this workspace path set.
4. **Precedence:** if two installed copies share the same logical name, the **effective** skill is the one Claude Code resolves (enterprise, then personal, then project; plugins namespaced). Prefer the path you infer is **winning** for `skill_id` / excerpts, and mention ambiguity in `evidence` if unsure.

Optional: run `python packages/skill-hr/scripts/scan_claude_code_skills.py` at the workspace root to seed a JSON list of on-disk skills before scoring.

## Phase P02a — Broad recall (shortlist)

**Goal:** Reduce the full pool to **≤ 12** skills (target **8–10**) without deep scoring.

1. **Filter pool**: omit `terminated`, `frozen`. **Exclude `skill-hr`** unless the JD is explicitly about skill operations (install, registry, match, retire skills)—see [`../matching-lexicon.md`](../matching-lexicon.md) meta routing.
   - When `employees[]` exists, shortlist employees first and treat `primary_skill` as the compatible `skill_id` label.
2. For each remaining skill, gather **signals** (cheap):
   - Overlap between JD (`mission_statement`, `must_have_competencies`, `deliverables`, `search_queries`, `competency_tags`) and skill `description` + **body excerpts**
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

3. **`competency_coverage_matrix`**: for **each** string in `jd.must_have_competencies`, one row:

   - `competency` (echo JD line)
   - `coverage`: `covered` \| `partial` \| `missing`
   - `evidence`: one short **quote or faithful paraphrase** tied to skill text; use `""` only if `missing`

4. **`hard_negative_explanations`** (when shortlist has ≥2 plausible candidates): list objects `{ "skill_id", "excluded_because" }` for **runner-up** skills you reject vs `best`—cite scope, wrong artifact, missing tool, registry `notes` conflict, or a weaker employee bundle per [`../03-matching-rubric.md`](../03-matching-rubric.md).

5. **`evidence`**: 2–5 bullets (strings) supporting the total score (may reference sub-scores).

6. **`gaps`**: JD competencies or tools **still** weak or missing for this skill.

7. **`confidence`**: `high` \| `medium` \| `low` from evidence strength (stale registry / thin excerpts → cap at `medium` for borderline scores).

8. **Rank** all P02b rows by **total `score`** descending; apply **tie-break** from `03-matching-rubric.md` using registry stats when available.

## Output schema (JSON)

**Do not invent fields** outside the JSON Schema. Top-level shape:

- `recall_shortlist`: string[]
- `candidates`: array of precision objects (only shortlist skills or employees), each with `skill_id`, optional `employee_id`, `skill_name`, optional `employee_name`, `score`, `subscores`, `competency_coverage_matrix`, `evidence`, `gaps`, `confidence`, and optional `hard_negative_explanations` (may be empty array)
- `best`: `{ "skill_id", "score" }` plus optional `employee_id` / `employee_name` when matching on the employee layer
- `decision`: `delegate` \| `confirm` \| `recruit`
- `decision_rationale`: string

Full field definitions: [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json).

## Decision rules

Let `delegate_min_score` = D, `confirm_band_min` = C (from `matching_config`).

- `best.score >= D` and `best.confidence` is not `low` → `delegate`.
- `C <= best.score < D` → `confirm` only when a real user or host gate blocks immediate execution; otherwise prefer `delegate` with explicit caveats or `recruit`, whichever keeps the flow moving safely.
- `best.score < C` → `recruit`.

**Probation:** If best candidate `on_probation`, require **+5** score margin over second place to auto-`delegate`; else `confirm` or `recruit` depending on whether the next step is genuinely user-gated.

## Execution ownership

- **`delegate`** means the framework should continue into P03 immediately and wait for an incumbent result or a proven blocker before the main reply.
- **`confirm`** is for real stop points only: destructive actions, approval-required installs, unclear requirements, missing credentials, or manual-only host invocation.
- **`recruit`** means continue into P04 immediately; do not stop at a search brief if the next safe host actions are still executable by the agent.
- **OpenClaw:** if the next documented action is agent-executable, choose `delegate` or `recruit` rather than returning a procedural explanation.

## Quality gates

- No P02b row without **description- or excerpt-aligned** evidence.
- Subscores must **sum to `score`** (integer, 0–100).
- If all shortlist scores `< C`, decision must be `recruit`.
- **Keyword stuffing:** penalize `competency_coverage` and `outcome_fit` when only tokens match, not deliverables.

## Failure modes

- **Description-only matching** — If body excerpts missing, flag `confidence: medium` or `low` for scores near thresholds.
- **Stale registry** — Honor `registry_status`; if `install_path` missing, prefer `low` confidence on borderline.
