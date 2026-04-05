# Example: Multi-agent HR department flow

This walk-through shows how **hr-director** coordinates other agents and the **hr_dispatch** task board. Adjust paths: use `skill-hr/scripts/hr_dispatch.py` when the skill is installed as `skill-hr/`.

## Scenario

User: *“Parse this invoice PDF into a JSON line item list and validate totals.”*

## 1. Open task board

From the **workspace root** (folder that should contain `.skill-hr/`):

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py create HR-20260405-001 "Invoice PDF to JSON validation"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 hr-director job-analyst "Intake: user request captured"
python3 packages/skill-hr/scripts/hr_dispatch.py progress HR-20260405-001 "Director routing to Job Analyst" "Intake🔄|JD|Match|Handoff|Execute|Debrief"
```

## 2. Job Analyst (P01)

- Loads `agents/job-analyst/SOUL.md`, `references/prompts/P01-intake-to-jd.md`, `references/02-jd-spec.md`.
- Produces structured JD with `search_queries` / `competency_tags` (e.g. `pdf`, `extraction`, `tabular`).

Director updates board:

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 JDReady "P01 complete"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 job-analyst hr-director "JD ready"
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 Matching "Start P02"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 hr-director talent-assessor "Match installed pool"
```

## 3. Talent Assessor (P02)

- Loads `agents/talent-assessor/SOUL.md`, rubric, P02 prompt, `schemas/p02-output.schema.json`.
- Emits `delegate` / `confirm` / `recruit` with scored candidates.

Example outcome: **`delegate`** to skill `pdf`.

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 talent-assessor hr-director "decision=delegate best=pdf"
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 Matched "pdf selected"
```

(If **`recruit`**: `state Recruiting`, `flow` to **recruiter** → **Vetting** with **compliance** → back to **Matched**.)

## 4. Onboarder (P03)

- Builds handoff package (checkpoint: written JSON artifact + totals check).

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 Delegated "P03 handoff issued"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 hr-director onboarder "Prepare handoff"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 onboarder hr-director "Handoff ready for pdf skill"
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 InProgress "Domain skill executing"
```

## 5. Domain skill + Performance Manager (P05)

After the `pdf` skill finishes:

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 Debrief "Awaiting P05"
python3 packages/skill-hr/scripts/hr_dispatch.py flow HR-20260405-001 hr-director perf-manager "Trial debrief"
```

- **perf-manager** updates `.skill-hr/registry.json` counters and writes `.skill-hr/incidents/…md` with frontmatter including `hr_task_id` and `hr_task_state`.

```bash
python3 packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 Closed "P05 success"
python3 packages/skill-hr/scripts/hr_dispatch.py show HR-20260405-001
```

## Permission recap

See `agents/GLOBAL.md`: only **hr-director** routinely invokes other agents; **recruiter** and **perf-manager** may invoke **compliance** for vetting / termination safety.

## Single-agent mode

If the host has only one agent session, load **`agents/hr-director/SOUL.md`** and execute the same steps **sequentially** using the prompts in `references/prompts/` without separate subagent calls; still use `hr_dispatch.py` if you want a durable board.
