# skill-hr

**Language / 语言:** [简体中文](README.md) | English (this page)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Anthropic-blue)](https://support.anthropic.com/en/articles/12580037-what-are-skills)
[![agentskills.io](https://img.shields.io/badge/spec-agentskills.io-8A2BE2)](https://agentskills.io)

[![GitHub stars](https://img.shields.io/github/stars/thinkitpossible/skill-hr?style=social&label=Star)](https://github.com/thinkitpossible/skill-hr)

**Meta Agent Skill · HR / orchestration for the Skill ecosystem**

> **Too many skills installed—still guessing who to dispatch on each task?**  
> **Stop stacking plugins; hire an HR function for your host.**

Your colleagues, friends, and advisors are already packaged as Skills—but they do not always ship reliably. When a task lands, you still bounce between “pick one at random” and “maybe install another?” You are not short on icons; you are short on HR that can **retain, retire, and record**. **skill-hr** does not replace domain work (code, slides, spreadsheets). It hires, routes, trials, debriefs, and keeps the ledger so you graduate from “skill collector” to someone who can actually decide.

![skill-hr hero visual](docs/readme-assets/01-hero-skill-hr.png)

- **Structured JDs**: every assignment starts as a job description (P01), then you pick who runs it; supports **`workstreams[]`** programs (drive P02→P03→execution→P05 per stream using `depends_on` / `parallel_group`).
- **Scored internal bench**: installed skills are matched with a rubric (P02), not gut feel.
- **Recruiting + records**: on weak/no match, **`employee-fabricator`** cold-starts the target employee and a P04 brief before external recruit; then market briefs and vetting (P04); **registry + incidents** are your HRIS; default is **logical termination** (`terminated`); **physical uninstall only after you explicitly OK it**.
- **Workforce upgrade**: `registry.json` supports first-class multi-skill **`employees[]`** (see [`registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json)); **`trainer`** owns design and retraining (P07/P08).
- **Research / platform-heavy tasks**: P01 can also load [`11-research-and-platform-access.md`](packages/skill-hr/references/11-research-and-platform-access.md) (surfaces, access, compliance).
- **Multi-agent HR department (optional)**: besides “one session runs the whole flow,” you can split by role—each persona has a `SOUL.md` under [`agents/`](packages/skill-hr/agents/); shared rules in [`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md). Task board and legal state transitions go through [`scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py) into **`.skill-hr/hr_tasks.json`** (see [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)).

Open-source **meta [Agent Skill](https://support.anthropic.com/en/articles/12580037-what-are-skills)**: treat Skills as a workforce with headcount, hiring, and performance—**executable people ops**, not a throwaway metaphor. The installable bundle lives under [`packages/skill-hr/`](packages/skill-hr/).

<span id="positioning"></span>

## Positioning: not “one more domain skill,” but HR

A hundred installed skills without JDs, scoring, trials, and a ledger is still a bazaar—busy, but not an organization. **skill-hr** is not here to write code, draw, build spreadsheets, or analyze PDFs—that stays with domain skills. It owns the **org layer**: structured JDs (P01), rubric-scored bench matching (P02), delegation and handoff (P03), market recruiting and vetting (P04), trial and debrief (P05), performance and logical termination (P06), with state in **registry / hr_tasks / incidents**.

**In one line: domain skills execute work; skill-hr runs the organization.**

---

<span id="workflow-p01-p06"></span>

## Workflow (P01–P06)

When work arrives, do not raffle the bench—run the pipeline. Each step has templates, artifacts, and paper trail. This is not a metaphor—it is an executable HR lifecycle (control plane in [`SKILL.md`](packages/skill-hr/SKILL.md), stage templates in [`references/prompts/`](packages/skill-hr/references/prompts/)).

![skill-hr lifecycle diagram](docs/readme-assets/02-lifecycle-flow.png)

- **P01 — Intake → JD**: turn fuzzy asks into a job description (goals, I/O, risks, done criteria).
- **P02 — Match Installed**: score the on-disk bench against the JD with a rubric—not vibes.
- **P03 — Delegate / Handoff**: ship a real handoff package (boundaries, artifacts, acceptance).
- **P04 — Recruit**: if the bench is thin, recruit externally—brief first, vet, then install.
- **P05 — Trial / Debrief**: trial runs plus debrief with structured output ([`p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json)).
- **P06 — Performance / Termination**: default to **logical termination** (`terminated`); physical uninstall only after explicit OK and path audit.

---

<span id="quick-start"></span>

## 30-second quick start

1. **Copy** [`packages/skill-hr/`](packages/skill-hr/) into your host skills tree as **`skill-hr/`** so **`skill-hr/SKILL.md`** exists.
2. **Claude Code**: read [`references/hosts/claude-code.md`](packages/skill-hr/references/hosts/claude-code.md). Typical paths: `<repo>/.claude/skills/skill-hr/` or `~/.claude/skills/skill-hr/`.
3. **OpenClaw**: read [`references/hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md).

**Optional: scan the on-disk bench (P02 aid)**

```bash
python packages/skill-hr/scripts/scan_claude_code_skills.py <workspace> [--include-user]
```

**Optional: validate HR ledger JSON**

```bash
python packages/skill-hr/scripts/validate_registry.py .skill-hr/registry.json
```

**Optional: task board in multi-agent mode (state machine + handoff audit)**

Run from the **workspace root** (first `create` will create `.skill-hr/` if needed):

```bash
python packages/skill-hr/scripts/hr_dispatch.py create HR-20260405-001 "Example task"
python packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 JDReady "P01 done"
python packages/skill-hr/scripts/hr_dispatch.py list
```

End-to-end walk-through: [`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md).

**Optional: launch the local dashboard (business board + employee views + archive + templates)**

From the repository root, build the frontend and start the API + static server (default port `8787`):

```bash
python packages/skill-hr/scripts/launch_dashboard.py --workspace-root .
```

On OpenClaw, when the agent must return while the server keeps running, add **`--background`**. If you only copied the `skill-hr/` skill folder without this repo’s `dashboard/` tree, use a full checkout or run `server.py` with `--static-dir` per [`references/hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md). Copy-paste rules / tool snippets: [`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md).

Then open `http://127.0.0.1:8787`. The server reuses workspace `.skill-hr/registry.json`, `.skill-hr/hr_tasks.json`, and `incidents/`.

![runtime ledger and dashboard overview](docs/readme-assets/04-runtime-dashboard.png)

Behind the UI sit three ledgers—**`registry.json` / `hr_tasks.json` / `incidents/`**—so this is not a one-off dispatch toy; it is **Skill HRIS** with memory and audit semantics (see [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)).

Optional: add a one-liner in project instructions (e.g. `CLAUDE.md`) for **when** to invoke skill-hr; procedures stay in `SKILL.md` and `references/`. **Rules kick off work; the skill teaches how to run it.**  
`.skillhub.json` next to a skill (if any) is marketplace metadata; HR state lives in **`.skill-hr/registry.json`**; multi-agent runs also use **`.skill-hr/hr_tasks.json`**.

---

## Table of contents

- [Positioning](#positioning)
- [Workflow (P01–P06)](#workflow-p01-p06)
- [30-second quick start](#quick-start)
- [Multi-agent HR department](#multi-agent)
- [Why skill-hr](#why-skill-hr)
- [Host support](#hosts)
- [Without HR vs with skill-hr](#before-after)
- [What you get](#features)
- [OpenClaw: completion-first](#openclaw-completion)
- [Architecture diagrams](#architecture)
- [Docs (Reference)](#doc-map)
- [Cursor and AGENTS](#cursor-agents)
- [Safety](#safety)
- [Framework evaluation](#evaluation)
- [Validate registry](#validate-registry)
- [Who it is for](#for-who)
- [FAQ](#faq)
- [License](#license)

---

<span id="why-skill-hr"></span>

## Why skill-hr

Most skill stacks drift into the same failure mode: more installs, messier routing, gut-feel dispatch, bench blindness, “try another one” after failure, and ambiguous “delete” that hits real folders. That is not a system—it is luck. **skill-hr** exists to turn the Skill world from “good enough” into something that **runs like an organization**.

- **More skills, harder choices**—without a shared JD and scoring rubric, dispatch stays ad hoc.
- **Bench vs market**—easy to miss a strong internal match or to install from the web without vetting and handoff.
- **No paper trail on failure**—who is reliable, on probation, or should be logically fired stays fuzzy.
- **“Delete skill” is ambiguous**—must separate **removing from the dispatch pool** from **deleting directories on disk**.

skill-hr encodes the workflow in [`SKILL.md`](packages/skill-hr/SKILL.md) and `references/`, driven by prompt templates **P01–P08** (P01–P06 core flow; P07/P08 design and training), with workspace state under **`.skill-hr/`** (see [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)).

---

<span id="multi-agent"></span>

## Multi-agent HR department

When the host supports **multiple agent sessions**, you can split HR into dedicated roles (similar in spirit to audited, role-based multi-agent setups; see for example the community project [edict](https://github.com/cft0808/edict)). **Single-session hosts** still follow one `SKILL.md` Mandatory flow end to end; alternatively one process loads **hr-director** and applies each `SOUL.md` as a phase.

| Agent ID | Role (summary) |
|----------|----------------|
| `hr-director` | Orchestration, user comms, branch decisions |
| `job-analyst` | P01 job description / JD |
| `talent-assessor` | P02 internal matching and scoring |
| `employee-fabricator` | Cold-start target multi-skill employee; P04 brief before external recruit |
| `recruiter` | P04 market search and install coordination |
| `compliance` | Safety and veto gates |
| `onboarder` | P03 delegation and handoff package |
| `perf-manager` | P05 debrief / P06 termination |
| `trainer` | Employee design / retraining (P07/P08) |
| `hris-admin` | Registry and incidents discipline |

![multi-role HR org chart](docs/readme-assets/03-hr-department-org-chart.png)

- **Everyone reads**: [`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md) (permission matrix, red lines, `hr_dispatch.py` usage)
- **Per-role briefs**: [`agents/*/SOUL.md`](packages/skill-hr/agents/)
- **Worked example**: [`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md)

---

<span id="hosts"></span>

## Host support

| Host | Status | Notes |
|------|--------|-------|
| **Claude Code** | Primary | Paths, nested `.claude/skills/`, `--add-dir`, plugin discovery: [`hosts/claude-code.md`](packages/skill-hr/references/hosts/claude-code.md). Pair P02 with the disk scan script when helpful. |
| **OpenClaw** | Primary | Deploy this bundle as **dedicated HR for skills**; completion-first semantics below. See [`hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md). |
| **Coze** | Reference | Plugin-first hosts and tool-before-chatter patterns: [`hosts/coze.md`](packages/skill-hr/references/hosts/coze.md). |
| **Cursor** | Optional | Project rules decide when to load skill-hr—[`.cursor/rules/skill-hr-always.mdc`](.cursor/rules/skill-hr-always.mdc) (tune `alwaysApply` / `globs`). |

---

<span id="before-after"></span>

## Without HR vs with skill-hr

| Without HR | With skill-hr |
|------------|---------------|
| Pick a skill or install another by gut | **Structured JD** (P01), then **scored internal match** (P02) |
| `curl \| sh` from the web | **Search brief + vetting** (P04), scripted install and handoff |
| “Try another one” after failure | **Trial and debrief** (P05), **termination report** (P06), registry/incidents |
| “Delete” might wipe folders | Default **logical termination** (`terminated`); **physical uninstall** only after explicit OK + path audit |

![without HR vs with skill-hr (boss mode)](docs/readme-assets/05-boss-mode-matrix.png)

**In one line**: skill-hr defaults to **logical termination in the ledger**; deleting folders is a separate, explicit, audited step. You are not adding “another chatty employee”—you are adding an auditable **HR function** that knows who should run, who to hire, who to retain, and who to retire.

---

<span id="features"></span>

## What you get

<details>
<summary><strong>Expand: full feature list and links</strong></summary>

- **Orchestration and gates**: [`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md) (mandatory flow, self-routing, safety, multi-agent overview)
- **Multi-agent global rules**: [`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md); **per-agent SOUL files**: [`agents/`](packages/skill-hr/agents/)
- **Task board CLI**: [`scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py)
- **Multi-agent walk-through**: [`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md)
- **Playbooks** (competencies, JD, matching, hiring, performance, termination, training/design, multi-skill employees, research/platform): [`references/`](packages/skill-hr/references/) (includes `09`–`11`)
- **Prompt templates P01–P08**: [`references/prompts/`](packages/skill-hr/references/prompts/)
- **Host install notes** (Claude Code, OpenClaw, Coze): [`references/hosts/`](packages/skill-hr/references/hosts/)
- **Registry / incident / hr_tasks schema**: [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)
- **Example registry**: [`examples/registry.example.json`](packages/skill-hr/examples/registry.example.json), [`examples/registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json) (`employees[]`)
- **JSON validation**: [`scripts/validate_registry.py`](packages/skill-hr/scripts/validate_registry.py)
- **Full-stack evaluation L0–L7** (P02 benchmark = layer L2): [`08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md)
- **P02 gold cases and metrics**: [`benchmarks/matching/`](packages/skill-hr/benchmarks/matching/)
- **P02 / P05 output schemas**: [`schemas/p02-output.schema.json`](packages/skill-hr/schemas/p02-output.schema.json), [`schemas/p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json)
- **Benchmark scorers**: [`scripts/compare_matching_benchmark.py`](packages/skill-hr/scripts/compare_matching_benchmark.py), [`scripts/run_matching_benchmark_llm.py`](packages/skill-hr/scripts/run_matching_benchmark_llm.py) (optional OpenAI-compatible API)
- **Claude Code on-disk skill scan (P02 aid)**: [`scripts/scan_claude_code_skills.py`](packages/skill-hr/scripts/scan_claude_code_skills.py)
- **Local HR dashboard**: [`dashboard/`](dashboard/) + one-shot launcher [`scripts/launch_dashboard.py`](packages/skill-hr/scripts/launch_dashboard.py); OpenClaw copy-paste notes in [`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md)

</details>

---

<span id="openclaw-completion"></span>

## OpenClaw: completion-first

On hosts like OpenClaw, the operating principle is simple: **if you can advance, advance; if you can finish, do not stop at a plan**—only pull the user back for real gates or proven **blockers**.

On OpenClaw, the framework is **completion-first**: keep executing documented, vetted, low-risk host steps until a real **completion checkpoint** or a proven **blocker**, then report.

- **`delegate`**: **dispatch now and keep executing** until the incumbent completes or proves blocked.
- **`confirm`**: reserve for **real user gates** (destructive actions, missing credentials, manual-only host steps).
- **Recruitment briefs** split **agent-continuable** steps from **user-gated** steps.
- **Phase-by-phase narration** belongs in `.skill-hr/incidents/`; user-facing replies default to **outcomes, artifacts, pending items, and blockers**.

<details>
<summary><strong>Expand: full wording (same as previous README)</strong></summary>

On OpenClaw, the framework is **completion-first**: if the next step is documented, vetted, and safe for the agent to execute, keep going until you reach a real **completion checkpoint** or a proven **blocker**, then report back.

- **`delegate`**: **dispatch now and keep executing** until the incumbent reaches completion or proves blocked.
- **`confirm`**: reserve for **real user gates** (destructive actions, missing credentials, host steps that are manual-only).
- **Recruitment briefs** split **agent-continuable steps** from **user-gated steps** so runs can flow through install, verification, and smoke delegation after approval.
- **Phase-by-phase narration** belongs in `.skill-hr/incidents/`; user-facing replies should default to **outcomes, artifacts, and blockers**, not a long “here is what I will do next.”

</details>

---

<span id="architecture"></span>

## Architecture diagrams

<details>
<summary><strong>Diagram 1: HR lifecycle (orchestration state machine)</strong></summary>

Behind each user request: **recruit → trial → debrief → retain or improve → hire again if needed**.

```mermaid
stateDiagram-v2
  direction LR
  [*] --> Intake: UserTask
  Intake --> JD: AnalyzeJD
  JD --> MatchInstalled: ScorePool
  MatchInstalled --> Delegate: BestAboveThreshold
  MatchInstalled --> Recruit: BelowThreshold
  Delegate --> Debrief: TaskEnds
  Debrief --> Retain: Success
  Debrief --> Terminate: Failure
  Recruit --> Trial: InstallAndBrief
  Trial --> Debrief
  Terminate --> Recruit: RetryOrEscalate
  Retain --> [*]
```

</details>

<details>
<summary><strong>Diagram 2: Four-step mapping (what HR does)</strong></summary>

```mermaid
flowchart TB
  subgraph step1 [Step 1 JD]
    A[New user task] --> B[Structured JD\nP01 + jd-spec]
  end
  subgraph step2 [Step 2 Internal match]
    B --> C{Installed skill\nscore above threshold?}
    C -->|Yes| D[Delegate P03\nLog incident]
  end
  subgraph step3 [Step 3 Market recruit]
    C -->|No| E[Web search brief P04\nVet and install]
  end
  subgraph step4 [Step 4 Trial and HR record]
    E --> F[Trial run + debrief P05]
    D --> F
    F --> G{Outcome}
    G -->|Success| H[Retain / update registry]
    G -->|Fail| I[Terminate in registry P06\nOptional uninstall with user OK]
    I --> E
  end
```

</details>

<details>
<summary><strong>Diagram 3: Repository layout vs runtime artifacts</strong></summary>

```mermaid
flowchart LR
  subgraph repo [Repository root]
    R[README.md]
    A[AGENTS.md]
    CR[.cursor/rules]
    D[dashboard frontend]
  end
  subgraph pkg [packages/skill-hr skill bundle]
    S[SKILL.md]
    AG[agents GLOBAL + SOUL]
    REF[references/00-11 etc]
    PR[prompts P01-P08]
    HO[hosts CC+OC+Coze]
    SC[scripts validate + hr_dispatch + launch_dashboard]
  end
  subgraph runtime [Workspace at runtime]
    REG[.skill-hr/registry.json]
    TASKS[.skill-hr/hr_tasks.json]
    INC[.skill-hr/incidents/]
  end
  repo --> pkg
  pkg -.->|creates or updates| runtime
```

</details>

**Bundle size hint**: about **40** Markdown files under `packages/skill-hr/` (`SKILL.md`, `references/00–11`, `matching-lexicon`, **P01–P08** prompts, **four** host notes, `agents/GLOBAL.md`, and **10** `agents/*/SOUL.md` files), plus repo-level docs and scripts.

---

<span id="doc-map"></span>

## Docs (Reference)

<details>
<summary><strong>Expand: documentation map</strong></summary>

| Topic | Link |
|-------|------|
| Control plane (triggers, flow, gates) | [`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md) |
| Multi-agent rules and personas | [`packages/skill-hr/agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md), [`packages/skill-hr/agents/`](packages/skill-hr/agents/) |
| HR task board CLI | [`packages/skill-hr/scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py) |
| Multi-agent example | [`packages/skill-hr/examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md) |
| All playbooks | [`packages/skill-hr/references/`](packages/skill-hr/references/) |
| Prompts P01–P08 | [`packages/skill-hr/references/prompts/`](packages/skill-hr/references/prompts/) |
| Claude Code / OpenClaw / Coze | [`packages/skill-hr/references/hosts/`](packages/skill-hr/references/hosts/) |
| Registry / incident / hr_tasks spec | [`packages/skill-hr/references/06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md) |
| Example registry | [`packages/skill-hr/examples/registry.example.json`](packages/skill-hr/examples/registry.example.json), [`registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json) |
| Registry validator | [`packages/skill-hr/scripts/validate_registry.py`](packages/skill-hr/scripts/validate_registry.py) |
| L0–L7 evaluation plan | [`packages/skill-hr/references/08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md) |
| P02 benchmark data | [`packages/skill-hr/benchmarks/matching/`](packages/skill-hr/benchmarks/matching/) |
| P02 / P05 JSON Schema | [`packages/skill-hr/schemas/p02-output.schema.json`](packages/skill-hr/schemas/p02-output.schema.json), [`p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json) |
| P02 benchmark scripts | [`packages/skill-hr/scripts/compare_matching_benchmark.py`](packages/skill-hr/scripts/compare_matching_benchmark.py), [`run_matching_benchmark_llm.py`](packages/skill-hr/scripts/run_matching_benchmark_llm.py) |
| CC disk skill scan | [`packages/skill-hr/scripts/scan_claude_code_skills.py`](packages/skill-hr/scripts/scan_claude_code_skills.py) |
| Dashboard / OpenClaw workflow | [`dashboard/`](dashboard/), [`packages/skill-hr/scripts/launch_dashboard.py`](packages/skill-hr/scripts/launch_dashboard.py), [`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md) |

</details>

---

<span id="cursor-agents"></span>

## Cursor and AGENTS

- Optional rule: [`.cursor/rules/skill-hr-always.mdc`](.cursor/rules/skill-hr-always.mdc)
- Agent entry summary: [`AGENTS.md`](AGENTS.md)

---

<span id="safety"></span>

## Safety

- Third-party skills may be malicious—**vet** before install; do not run unreviewed **`curl | sh`**.
- **“Delete skill”** defaults to **logical termination** in the registry (`terminated`), not silent filesystem removal.
- **Physical uninstall** only after **explicit user confirmation** and path audit.
- Veto list: [`01-competency-model.md`](packages/skill-hr/references/01-competency-model.md)

---

<span id="evaluation"></span>

## Framework evaluation

The **full-stack** plan (L0–L7: package integrity, P01–P06 core stages, registry, safety, E2E) is [`08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md); employee design / multi-skill paths also use `09`/`10` and P07/P08. The “benchmark = P02 only” workflow is **layer L2**; commands and gold cases live in that doc and under [`benchmarks/matching/`](packages/skill-hr/benchmarks/matching/).

---

<span id="validate-registry"></span>

## Validate registry

```bash
python packages/skill-hr/scripts/validate_registry.py .skill-hr/registry.json
```

---

<span id="for-who"></span>

## Who it is for

If any of these sound like you, you are in the target audience:

- Teams with many installed skills but no reliable dispatch story  
- Anyone who wants agent/skill ecosystems to behave like an **organization**  
- Anyone who wants install → trial → retirement to be **process + paper trail**  
- Anyone who wants meta agents to manage **headcount and performance**, not just chat  
- Users of **Claude Code**, **OpenClaw**, **Cursor**, and similar hosts building skill governance  

---

<span id="faq"></span>

## FAQ

**How is this different from “install more plugins / skills”?**  
More installs only add candidates. skill-hr adds a **shared JD, scoring, recruiting, trial, ledger, and termination semantics** so the host dispatches with a process instead of luck.

**Does skill-hr replace domain skills?**  
No. It owns **selection, handoff, records, and retirement**; the chosen domain skill still executes work per its `SKILL.md`. See the opening of [`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md).

**Should `.skill-hr/` be committed to git?**  
Team choice: commit if you want a **shared project ledger and incidents**; use `.gitignore` or redact if sensitive.

**Do I copy P01–P08 into chat by hand?**  
No. They are **templates** under `references/prompts/`; after the skill loads, follow the Mandatory flow in [`SKILL.md`](packages/skill-hr/SKILL.md) and pull them progressively.

**What about marketplace skills?**  
**Vet** first; avoid unknown installers. See [Safety](#safety) and [`01-competency-model.md`](packages/skill-hr/references/01-competency-model.md).

**How does this relate to `skill-creator` or `find-skills`?**  
`skill-creator` focuses on **authoring/updating skills**; `find-skills` on **discovery and install leads**; skill-hr on **full lifecycle and HRIS-style state**. They compose: find or author a skill, then let skill-hr handle matching, delegation, and performance records.

**Do multi-agent mode and “one agent runs skill-hr” conflict?**  
No. Multi-agent is an **optional deployment**: use `agents/*/SOUL.md` plus `hr_dispatch.py` when you have multiple sessions; otherwise follow the single Mandatory flow in [`SKILL.md`](packages/skill-hr/SKILL.md).

---

<span id="license"></span>

## License

MIT — [`packages/skill-hr/LICENSE`](packages/skill-hr/LICENSE)

---

If this repo helps you, a **Star** on [GitHub](https://github.com/thinkitpossible/skill-hr) makes updates easier to find; open an **Issue** when something breaks.

[![Hand-drawn star curve — thanks for every star](docs/readme-assets/hand-drawn-star-curve.svg)](https://github.com/thinkitpossible/skill-hr)
