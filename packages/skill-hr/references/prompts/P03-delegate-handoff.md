# P03 Delegation handoff (incumbent brief)

## Objective

Produce a **handoff package** so the selected **employee** (incumbent) executes without redundant HR chatter, works until a real completion checkpoint, and reports back in a shape you can log. The incumbent may be a single-skill worker or a **multi-skill employee**; when `soul_path` is set, execution is **SOUL-first** (see below).

## Inputs

- `jd`: P01 JSON.
- `selected_skill`: `skill_id`, `name`, `description`, optional `employee_id`, `employee_name`, optional **`soul_path`** (from registry `employees[]`), and `references` hints.
- `user_verbatim`: key user quotes.
- `incident_stub`: proposed `incident_id` or filename stem.

## Procedure

1. Write **`context_for_incumbent`**: mission, success criteria, deliverables, constraints—no internal HR scoring prose.
   - If the selected worker is a multi-skill employee, name the employee once and call out the primary skill plus any secondary skills that materially matter.
   - If **`soul_path`** is present: state that the incumbent must **read that `SOUL.md` first**, then load each domain `SKILL.md` **only as the SOUL instructs** (order, branching). If **`soul_path`** is absent: state that the incumbent follows the **`primary_skill`**’s `SKILL.md` as the main workflow (other bundled skills are not auto-invoked unless the user/host loads them).
2. Add **`do_not_do`**: scope cuts, forbidden actions (from user or policy).
3. Specify **`completion_checkpoint`**: what counts as "done enough to report back" for this assignment. For multi-skill employees, prefer a checkpoint that fits the SOUL’s orchestration (or the primary skill if no SOUL).
4. Specify **`report_back_format`**: exact fields the incumbent should return after work (see below).
5. If the **lead** skill has a **canonical first step** visible in its SKILL.md opening, mention it once (do not paste entire SKILL.md). When SOUL governs order, you may mention first-step for the skill the SOUL loads first.

## Completion rule

- Tell the incumbent to **do the work first** and report back only after reaching the stated completion checkpoint or after proving a blocker with evidence.
- "I would do X next" is **not** a valid completion checkpoint by itself.
- Valid checkpoints include a produced artifact, a verified install, a successful command or test run, an edited target file, or a blocker demonstrated with concrete evidence.

## Plugin- and tool-first hosts (e.g. Coze)

If the incumbent needs **plugins, HTTP tools, or MCP** to gather data, the handoff must tell the incumbent explicitly:

- **Invoke the required tool in the first productive turn** (after at most one short optional intent sentence).
- **Forbidden:** repeating variations of “I will start searching / collecting data” **without** an intervening successful tool call or a **single** evidenced blocker message.
- **On tool failure:** one concise reply with the host-reported error, then stop or escalate—no preamble loop.

Host-specific notes: [`../hosts/coze.md`](../hosts/coze.md).

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

`handoff_message_template` should be copy-pasteable. Use **one** of:

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
