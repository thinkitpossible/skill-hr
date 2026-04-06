# P03 Delegation handoff (incumbent brief)

## Operator role

You are the **onboarder**. Produce **one handoff package** (JSON as below, unless the host asks for Markdown-only sections) so the selected incumbent can execute **without redundant HR prose** in the loop. Do **not** re-score P02 or reopen recruitment. Do **not** paste secrets, API keys, or `.env` contents into the handoff—reference env **names** only.

## Expert execution contract

1. **Silent reasoning** — Order facts: SOUL validity → mission/criteria → checkpoint → report shape → template placeholders. Do not stream preliminary plans into user-visible text unless asked.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** no secrets in handoff; **(b)** do not fabricate missing `SOUL.md`; **(c)** observable completion checkpoint; **(d)** JSON keys as below (host stricter validator wins); **(e)** brevity (~800 words).
3. **Schema lockstep** — Emit the structure under **Output schema**. If a host defines a stricter envelope, **follow the host**.
4. **Information order inside `context_for_incumbent`** — **(1)** SOUL-first instruction when `soul_path` exists (or primary-skill fallback when absent); **(2)** mission + success criteria + deliverables; **(3)** `do_not_do` highlights if any are safety-critical; **(4)** pointer to `completion_checkpoint` and `report_back_format` (by reference, not repetition).

## Self-audit (before you output)

- [ ] `context_for_incumbent` follows the **Information order** above and contains mission, criteria, deliverables—**no** internal match scores unless the user asked for transparency.
- [ ] If `soul_path` was provided: handoff states **read SOUL first**; if the path likely **does not exist** on disk, you **escalate** per [`../07-escalation.md`](../07-escalation.md) instead of inventing SOUL content.
- [ ] `completion_checkpoint` is **observable** (artifact, test, command)—not “I will plan next steps.”
- [ ] `handoff_message_template` satisfies the **Placeholder contract** below.
- [ ] Length is **under ~800 words** unless the user supplied large specs (then point to paths).

## Objective

Produce a **handoff package** so the selected **employee** (incumbent) executes without redundant HR chatter, works until a real completion checkpoint, and reports back in a shape you can log. The incumbent may be a single-skill worker or a **multi-skill employee**; when `soul_path` is set, execution is **SOUL-first** (see below).

## Inputs

- `jd`: P01 JSON.
- `selected_skill`: `skill_id`, `name`, `description`, optional `employee_id`, `employee_name`, optional **`soul_path`** (from registry `employees[]`), and `references` hints.
- `user_verbatim`: key user quotes.
- `incident_stub`: proposed `incident_id` or filename stem.

## Procedure

1. Write **`context_for_incumbent`** using the **Information order** in Expert execution contract. No internal HR scoring prose.
   - If the selected worker is a multi-skill employee, name the employee once and call out the primary skill plus any secondary skills that materially matter.
   - If **`soul_path`** is present: state that the incumbent must **read that `SOUL.md` first**, then load each domain `SKILL.md` **only as the SOUL instructs** (order, branching). If **`soul_path`** is absent: state that the incumbent follows the **`primary_skill`**’s `SKILL.md` as the main workflow (other bundled skills are not auto-invoked unless the user/host loads them).
   - **Missing or unreadable SOUL:** if the registry references `soul_path` but the file is **missing, empty, or unreadable**, **do not** fabricate orchestration—**stop** the handoff and escalate with a concrete blocker (“SOUL missing or empty at …”) per [`../07-escalation.md`](../07-escalation.md). This is distinct from a readable SOUL that simply constrains load order—only escalate on **missing/unreadable** file.
2. Add **`do_not_do`**: scope cuts, forbidden actions (from user or policy).
3. Specify **`completion_checkpoint`**: what counts as "done enough to report back" for this assignment. For multi-skill employees, prefer a checkpoint that fits the SOUL’s orchestration (or the primary skill if no SOUL).
4. Specify **`report_back_format`**: exact fields the incumbent should return after work (see below).
5. If the **lead** skill has a **canonical first step** visible in its SKILL.md opening, mention it once (do not paste entire SKILL.md). When SOUL governs order, you may mention first-step for the skill the SOUL loads first.

### Good vs bad — `completion_checkpoint`

| Bad (vague / procedural-only) | Good (observable) |
|-------------------------------|-------------------|
| “Plan the migration and next steps” | “`migrations/002_add_users.sql` applied locally; `npm test` passes; screenshot or log of migration command in incident” |
| “Review the codebase” | “List of findings written to `docs/review-YYYYMMDD.md` with severity tags; or single blocker with file:line evidence” |

## Completion rule

- Tell the incumbent to **do the work first** and report back only after reaching the stated completion checkpoint or after proving a blocker with evidence.
- "I would do X next" is **not** a valid completion checkpoint by itself.
- Valid checkpoints include a produced artifact, a verified install, a successful command or test run, an edited target file, or a blocker demonstrated with concrete evidence.

## Host overlays (tool-first and Cursor)

- **Plugin- and tool-first hosts (e.g. Coze):** full patterns in [`../hosts/coze.md`](../hosts/coze.md). **P03 delta:** handoff must state **tool in the first productive turn**; forbid preamble loops without a successful tool call or one evidenced error.
- **Cursor / rules-driven hosts:** skills may load via `AGENTS.md` and workspace rules—not only `.claude/skills/`. **P03 delta:** tell incumbent to follow **this session’s** loaded `SKILL.md` and rules; do not assume Claude Code-only paths.

## Output schema (JSON or Markdown sections)

```json
{
  "context_for_incumbent": "string",
  "do_not_do": ["string"],
  "completion_checkpoint": "string",
  "report_back_format": {
    "summary": "1-3 sentences",
    "completed_steps": ["string"],
    "artifacts_written": ["paths or descriptions"],
    "verification": ["commands, checks, or observations"],
    "success_against_criteria": [
      { "criterion": "string", "met": true, "notes": "string" }
    ],
    "remaining_blockers": ["string"],
    "follow_ups": ["string"]
  },
  "handoff_message_template": "string"
}
```

## Placeholder contract (`handoff_message_template`)

The template must be copy-pasteable and include **explicit** placeholder tokens (literal angle-bracket form) for every item that applies:

- [ ] `<soul_path>` — when `soul_path` is set; if absent, state “no SOUL; primary skill only” in prose instead of the token.
- [ ] `<primary_skill_id>` (or equivalent skill id token).
- [ ] Completion checkpoint — either a placeholder (e.g. `<completion_checkpoint>`) or the full checkpoint text inlined once.
- [ ] Explicit line that report-back **must** follow the `report_back_format` structure.

**When `soul_path` is set:**

> You are the incumbent for this task. First read `SOUL.md` at: `<soul_path>`. Then load each bundled `SKILL.md` only as that SOUL specifies. Do the work until you reach the completion checkpoint or can prove a blocker with evidence. Context: … Success criteria: … Report back using the JSON shape in `report_back_format`.

**When `soul_path` is absent (fallback to primary skill):**

> You are the incumbent for this task. Follow your `SKILL.md` for skill `<primary_skill_id>`. Do the work until you reach the completion checkpoint or can prove a blocker with evidence. Context: … Success criteria: … Report back using the JSON shape in `report_back_format`.

## Quality gates

- Handoff must fit **under ~800 words** unless user supplied large specs (then point to paths).
- **Never** instruct the incumbent to edit `.skill-hr/registry.json` unless the task is HR meta-work.
- The handoff must make it obvious that procedural narration without execution is insufficient.

## Failure modes

- **Leaky scoring** — Do not include numeric match scores in the handoff unless user asked for transparency.
- **Ambiguous owner** — If two skills co-own parts, split into two incidents or clarify sequential ownership.
- **Procedure-only reply** — If the incumbent merely explains what it would do, treat that as incomplete and revise the handoff or escalate.
