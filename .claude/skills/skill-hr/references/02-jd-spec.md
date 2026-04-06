# Job description (JD) specification

## Required fields

Aligned with P01 output schema:

- `role_title` — Short label for incidents and search.
- `mission_statement` — Single-sentence purpose.
- `must_have_competencies` — Non-empty; observable.
- `deliverables` — Concrete artifacts.
- `success_criteria` — Checklist for P05.
- `complexity_tier` — `S` \| `M` \| `L`.
- `search_queries` — 3–5 short strings for P02a recall (see P01).
- `competency_tags` — 3–8 normalized tags for P02a (see P01).

## Optional but recommended

- `nice_to_have`, `tools_and_access`, `constraints`, `risk_notes`.
- `capability_slots[]` — Decomposed **hirable capability slices** for composite / pipeline jobs (consumed by P02 slot coverage and P04 per-gap query tracks). See §Capability slots below.

## Program layer (boss goal, excellence, multi-role splits)

Invoking **skill-hr** usually means the task is **not trivial** and may need **more than one** competency or incumbent. P01 should capture the stakeholder frame **before** atomizing roles.

| Field | Required when | Description |
|-------|----------------|-------------|
| `boss_goal` | Recommended for `M` / `L` | One sentence: what the stakeholder needs to be true when the **whole** engagement completes (may align with top-level `mission_statement`). |
| `excellence_bar` | Recommended for `M` / `L` | Observable signals that separate **minimal completion** from **high-quality / exemplary** delivery; P05 uses this for `delivery_quality`. |
| `orchestration_notes` | Optional | How workstreams run: sequential gates, parallel tracks, approvals, or “single SOUL employee” vs multiple handoffs. |
| `workstreams[]` | When `complexity_tier` is `M` or `L`, or competencies clearly split | Sub-jobs; see below. Omit or use `[]` for a single-role `S` task. |

### `workstreams[]` item

Each stream is a **hirable slice** of the program (its own match/recruit/delegate path when you split execution):

| Field | Type | Description |
|-------|------|-------------|
| `workstream_id` | string | Stable id, e.g. `ws-research`, `ws-impl` |
| `role_title` | string | Label for incidents and P02 |
| `must_have_competencies` | string[] | Non-empty per stream |
| `deliverables` | string[] | Concrete artifacts for this stream |
| `success_criteria` | string[] | Checkable; feed P05 for this stream |
| `depends_on` | string[] | Other `workstream_id` values that must complete first (DAG) |
| `parallel_group` | string, optional | Same group id → may run in parallel when no `depends_on` conflict |

**Splitting rule:** Prefer several **sharp** workstreams over one kitchen-sink JD when domains differ (e.g. security review vs feature build), checkpoints differ, or the excellence bar needs a **dedicated** quality pass. Prefer **one** multi-skill employee + SOUL when the same execution thread should hold context across skills (see [`10-multi-skill-agent.md`](10-multi-skill-agent.md)).

**Registry alignment:** Each workstream should map cleanly to **task-type employees** in `.skill-hr/registry.json` when possible: **one stream → one specialist** whose `skills[]` is the **skill closure** for that stream’s archetype, or **one program** → **one** bundled employee when `orchestration_notes` call for a single thread and the archetype is unified. See **Task-type specialization** and **Skill closure** in [`10-multi-skill-agent.md`](10-multi-skill-agent.md).

### `capability_slots[]` item (optional)

Use when the user outcome is a **pipeline** of distinct capabilities inside one program (e.g. research across surfaces → synthesis; outline → visual assets → `.pptx` assembly). Slots are **not** a substitute for `workstreams[]` when separable owners, legal gates, or DAG checkpoints require different incumbents—use streams for that. Slots **are** for: one archetype / one thread that still needs **explicit closure** across skills (multi-skill employee + SOUL) or for sharpening P02/P04 when a single JD would hide gaps.

| Field | Type | Description |
|-------|------|-------------|
| `slot_id` | string | Stable id referenced in P02 `gaps` / P04 `covers_slots` (e.g. `slot-pptx`, `slot-image-search`). |
| `capability_label` | string | Short HR-facing label. |
| `must_satisfy` | string | One **testable** line for this slot. |
| `integration_surface` | string, optional | Where execution or evidence lives: `open_web`, `news`, `forums`, `social_read`, `browser_automation`, `mcp_tools`, `vendor_api`, `cli`, `local_files`, `unknown`. Guidance: [`11-research-and-platform-access.md`](11-research-and-platform-access.md). |
| `recruit_query_hints` | string[], optional | 2–4 P04-oriented queries **per slot**; prefer over one blended web search. |

**Usage rule (P01):** For `complexity_tier` `M` or `L` **pipeline** jobs, emit non-empty `capability_slots[]` **or** document in `orchestration_notes` why the job is atomic without slots. Do not duplicate the same decomposition in both `workstreams[]` and `capability_slots[]` without purpose—pick the structure that matches execution (parallel separable streams vs one bundled pipeline).

## Retrieval-oriented fields (required by P01; consumed by P02a)

Fed to **P02a** broad recall; keep stable and specific:

- **`search_queries`** — short phrases for lexical / host search over installed skills (artifact types, product names, verbs like “audit” vs “draft”).
- **`competency_tags`** — normalized tags, ideally prefixed by dimension from the competency model (e.g. `domain:security`, `artifact:xlsx`, `integration:browser`).

**Quality:** Queries should not duplicate `role_title` only; include **orthogonal** angles (deliverable format, stack, risk). Tags should be **exclusive enough** to separate commonly confused skills (e.g. SEO audit vs SEO article writing).

## JD quality checklist (before matching)

0. **Program bar** — For `M` / `L`: are `boss_goal` and `excellence_bar` filled? If competencies span domains, are `workstreams[]` defined or is there an explicit rationale in `orchestration_notes` for a single incumbent? For **pipeline** jobs, are `capability_slots[]` filled or omission justified?
1. **Uniqueness** — Could a stranger pick the right skill from `role_title` + `mission_statement` alone?
2. **Measurability** — Each success criterion is yes/no or has an explicit metric.
3. **Scope** — `do_not_do` implied by constraints (if not, add to P03).
4. **Dependencies** — Credentials, API keys, VPN, or hardware called out in `risk_notes`.
5. **Alignment** — No competency listed that is not needed (trim bloat to improve matching).

## Anti-patterns

- **Tool-only JD** — "Use Claude" is not a competency; name the outcome.
- **Kitchen-sink JD** — Split into `workstreams[]` (or sequential program phases) if multiple unrelated deliverables; do not overload one `role_title` with every competency.

## Versioning

If the user changes requirements mid-flight, append **JD revision** in the incident body (`v2`, `v3`) rather than silently overwriting P01 output in older incidents.
