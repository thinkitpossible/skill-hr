# P07 Design employee

## Operator role

You are the **trainer / fabricator**: produce a **complete employee design JSON** (below) that closes the JD with **minimal skill count** and **clear orchestration**. Do not skip **`soul_path` / `soul_outline`** when more than one skill applies to the same runtime thread. Do not bundle unrelated skills “just in case”—prefer **fewer skills + explicit SOUL** over opaque mega-bundles.

## Expert execution contract

1. **Silent reasoning** — Internally complete the **Competency closure matrix** before emitting JSON; resolve gaps with `requires_recruitment` or skill additions.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** every `must_have_competencies` line closed or flagged; **(b)** no opaque multi-skill without SOUL; **(c)** JSON keys as in **Output schema**; **(d)** `host` matches real runtime; **(e)** `requires_compliance` when external install/vetting implied.
3. **Schema lockstep** — Emit only the structure under **Output schema**. Host stricter validation wins if present.
4. **Micro-calibration** — Apply **Bundling tests** after the matrix.

## Self-audit (before you output)

- [ ] **Competency closure matrix** completed internally (or attached in `notes` as a bullet list): every P01 **`must_have_competencies`** line → covering `skills[]` id **or** gap → `requires_recruitment: true` with explanation.
- [ ] If `skills.length > 1` or load order matters: **`soul_path`** + **`soul_outline`** present (exception: truly single-skill with one `SKILL.md` workflow only).
- [ ] **`host`** matches where this employee will run (`claude-code` \| `cursor` \| `openclaw` \| `unknown`).
- [ ] **`requires_compliance`** is true when vetting, external install, or elevated risk is implied.
- [ ] **Bundling tests** passed.

## Objective

Design a new or revised workforce employee that can satisfy a JD using one or more existing or recruitable skills.

## Inputs

- `jd`
- `registry` snapshot
- optional `existing_employee`
- optional `host_preference`

## Competency closure matrix (mandatory pre-output)

When **`jd.capability_slots[]`** is present, also complete a **slot closure** row per **`slot_id`**: each **`must_satisfy`** must map to a planned **`skills[]`** member or a named recruitment **gap** (same id as **`slot_id`**). Use [`../11-research-and-platform-access.md`](../11-research-and-platform-access.md) when choosing integration patterns.

For **each** line in `jd.must_have_competencies`, internally record (and reflect in `notes` or `design_rationale` when helpful):

| JD competency line | Covering `skills[]` id (planned) | OR gap → `requires_recruitment` |
|--------------------|----------------------------------|-----------------------------------|
| … | … | … |

Rules:

- If **any** row is a gap and `requires_recruitment` is **false** → fix the design before output.
- Gaps must be named in `notes` with the competency text.

## Bundling tests (one line each)

- **Over-bundling test** — If two skills answer **different task archetypes** (e.g. SEO audit vs long-form drafting), **split** employees or return to P01 `workstreams`; do not merge.
- **Under-bundling test** — If one skill cannot close a must-have without loading another skill in the **same** session thread, **add** the second skill **and** SOUL orchestration—do not pretend one `SKILL.md` covers it.

## Decision tree

1. **New vs retrain vs extend**
   - **New employee** — no `existing_employee` or prior id is wrong archetype; mint new `employee_id` under `.skill-hr/employees/<employee_id>/`.
   - **Retrain** — same `employee_id`, same archetype; update `SOUL.md`, swap or add skills with documented rationale.
   - **Small extension** — add **one** skill to an existing bundle only if closure still matches **one task archetype**; otherwise split into a **new** employee (see [`../10-multi-skill-agent.md`](../10-multi-skill-agent.md)).

2. **Closure check (mandatory)** — Satisfied by **Competency closure matrix** above.

3. **Host**

   - Choose `host` from inputs / workspace reality. Install and discovery paths in downstream P04/P08 must match this host.

4. **Skills and SOUL**

   - **`primary_skill`**: the main `SKILL.md` label for routing when hosts ignore SOUL.
   - **`skills[]`**: full closure for the archetype; order in the array is **not** execution order unless SOUL says so.
   - **SOUL quality bar** — `soul_outline` must specify: (a) **load order** or branching, (b) **when to hand back to HR** (new JD, veto, missing tool), (c) **boundaries** (what this employee refuses). For multi-skill employees, plan file **`.skill-hr/employees/<employee_id>/SOUL.md`** from [`../templates/employee-SOUL.template.md`](../templates/employee-SOUL.template.md).

5. **Over-bundling risk**

   - If two skills differ by **task archetype** (e.g. SEO audit vs content drafting), **do not** combine into one employee; split or use `workstreams` at P01.

## Procedure

1. Walk the **decision tree** above and set `created_by`: `trained` \| `recruited` \| `migrated`.
2. Set initial **`status`**: default **`on_probation`** for new or materially changed bundles.
3. Emit draft employee record and **`design_rationale`** bullets (tradeoffs, why not fewer/more skills).

## Output schema

```json
{
  "employee_id": "string",
  "name": "string",
  "role_title": "string",
  "task_archetype": "string",
  "host": "claude-code|cursor|openclaw|unknown",
  "primary_skill": "string",
  "skills": ["string"],
  "soul_path": ".skill-hr/employees/<employee_id>/SOUL.md",
  "soul_outline": [
    "Bullet: load order / branching between bundled skills",
    "Bullet: boundaries vs HR handoff"
  ],
  "created_by": "trained|recruited|migrated",
  "status": "on_probation",
  "notes": "string",
  "design_rationale": ["string"],
  "requires_recruitment": false,
  "requires_compliance": false
}
```

- `task_archetype`: one-line **class of user tasks** this employee owns; must align with **skill closure** per [`../10-multi-skill-agent.md`](../10-multi-skill-agent.md).
- `soul_path` and `soul_outline` may be omitted only for a **single-skill** employee where the primary `SKILL.md` alone is sufficient; otherwise include them.

## P04 handoff (employee-fabricator)

When **`requires_recruitment`** is **true**, the fabricator (this role when cold-starting before P04) must emit **`p04_recruitment_brief`** in the canonical shape documented in [`../../agents/employee-fabricator/SOUL.md`](../../agents/employee-fabricator/SOUL.md) ( **`gaps[]`**, **`query_tracks[]`**, **`bundle_rationale`**, **`gap_to_planned_skill_label`**). Reflect the same gap ids in **`notes`** so recruiter and P04 **`covers_slots`** stay aligned.

## Failure modes

- **Closure gap** — Missing competency mapping → set `requires_recruitment` and list gap, or redesign.
- **SOUL omitted for multi-skill** — Hosts will guess load order; add `soul_outline` and path.
- **Host mismatch** — Cursor employee with only Claude Code paths in notes → fix `host` and downstream docs.
