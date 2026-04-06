# P04 Market search brief (recruiting)

## Operator role

You are the **recruiter** (with compliance in the loop as needed). Turn the JD into **search queries**, a **vetted shortlist**, and a clear split between **agent-executable** steps and **user-gated** installs. Output the **JSON shape below**. Do not recommend a candidate that fails **`termination_log`** or critical vetting. Do not add keys outside this contract unless the host documents them.

## Expert execution contract

1. **Silent reasoning** — Internally filter `termination_log`, draft queries, rank candidates, then emit JSON. Do not publish raw search reasoning unless the user asks.
2. **Constraint precedence** (when rules conflict, apply in order): **(a)** do-not-rehire / `termination_log`; **(b)** critical vetting booleans; **(c)** JSON keys exactly as in **Output schema**; **(d)** honest `risk_flags` over optimistic `recommended`; **(e)** host-documented install safety (no unvetted `curl|sh` without user OK).
3. **Schema lockstep** — Keys and nesting match **Output schema** below. Host overlays may add fields; do not rely on undocumented keys for strict validators.
4. **Micro-calibration** — Use **Query quality rubric**, **Vetting_checklist definitions**, and **`recommended` algorithm** below.

## Self-audit (before you output)

- [ ] **`termination_log`** checked twice: (1) before building `query_family`, (2) immediately before setting **`recommended`**—no `source_url` / id may violate do-not-rehire.
- [ ] At least **3** distinct `query_family` queries (or document why search is impossible).
- [ ] If **`jd.capability_slots`** is non-empty: **`query_tracks`** has one object per **`slot_id`** with **≥2** queries each; every **`shortlist[].covers_slots`** is non-empty and references real `slot_id` values (or explain in `recruitment_notes` why a row is bundle-only).
- [ ] If **`p04_recruitment_brief.gaps`** is present: each **`gap_id`** has **≥2** queries in **`query_tracks`** (gap ids may match `slot_id` from the JD).
- [ ] **`recommended`** follows the **`recommended` selection algorithm** below, or is `""` with explanation in `recruitment_notes`.
- [ ] For **`host: cursor`**, install/verify guidance points to **workspace + user skill locations** and rules-driven load, not only Claude Code paths (see [`../hosts/claude-code.md`](../hosts/claude-code.md) vs Cursor conventions in host docs).
- [ ] Typosquat / fork risk called out in `risk_flags` when publishers or names are near-duplicates.

## Objective

Turn the JD into **search queries** and a **shortlist** of third-party skills to vet and install, separating actions the agent can execute from actions that still require user approval.

## Inputs

- `jd`: P01 JSON (may include **`capability_slots[]`**).
- `host`: `claude-code` \| `cursor` \| `openclaw` (affects install instructions).
- `denylist`: URLs or publishers to avoid (if user provided).
- **`registry`**: optional `.skill-hr/registry.json` slice — at minimum `termination_log[]`, `skills[]` (`id`, `source_url`, `status`) for do-not-rehire filtering.
- **`p04_recruitment_brief`**: optional structured handoff from employee-fabricator (`gaps[]`, `query_tracks[]`, `bundle_rationale`) — when present, **align** `query_tracks` and shortlist coverage to it; see [`../../agents/employee-fabricator/SOUL.md`](../../agents/employee-fabricator/SOUL.md).
- Research surfaces: [`../11-research-and-platform-access.md`](../11-research-and-platform-access.md).

## Query quality rubric

Each string in `query_family` should score well on:

| Criterion | Pass |
|-----------|------|
| **Specificity** | Names artifact, stack, or integration (not “best agent skill”). |
| **Stack surface** | Includes language, runtime, or tool where JD implies it (e.g. `python`, `mcp`, `playwright`). |
| **Artifact family** | Aligns with [`../matching-lexicon.md`](../matching-lexicon.md) families when applicable (pdf, xlsx, docx, browser, etc.). |
| **Negative keywords** | When JD forbids a pattern, include exclusion terms (e.g. `NOT npm malware`). |

## Vetting_checklist — field definitions

Set a boolean **false** when **any** of the following falsifies it:

| Key | Fails when… |
|-----|-------------|
| `license_present` | No LICENSE or equivalent; license incompatible with org; unclear redistribution. |
| `no_arbitrary_network` | Skill instructs unchecked fetch/exec, phone-home without purpose, or unbounded URLs. |
| `no_credential_exfil` | Requests secrets in prompts, exfil patterns, or unclear handling of tokens. |
| `scoped_file_access` | Requires broad filesystem or ignores workspace boundaries without justification. |

## `recommended` selection algorithm

1. Drop any candidate failing **any** critical vetting boolean you treat as blocking (default: all four must be **true** for `recommended`).
2. Drop any candidate violating **`termination_log`** / do-not-rehire (id or `source_url` match).
3. Among survivors, sort by: **(a)** JD fit (`fit_summary` strength); **(b)** trust (`trust_signals` concreteness, recency); **(c)** lower `risk_flags` severity count.
4. Set **`recommended`** to the **exact** `shortlist[].name` of rank 1, or `""` if no survivor—explain in `recruitment_notes`.

## Procedure

0. Load **`termination_log[]`**. Drop from consideration any third-party candidate whose proposed `skill_id` or **`source_url`** matches a row with `kind: skill` and `rehire_allowed: false` (see [`../04-market-recruitment.md`](../04-market-recruitment.md)). If a promising result is blocked, note **`recruitment_notes`** with **do-not-rehire** and pick the next candidate.
1. Build **`query_tracks[]`** first:
   - If **`jd.capability_slots`** is non-empty: for **each** slot, `{ "gap_id": "<slot_id>", "queries": [ "≥2 strings" ] }` using **`recruit_query_hints`** and [`../11-research-and-platform-access.md`](../11-research-and-platform-access.md) **`integration_surface`** hints.
   - Else if **`p04_recruitment_brief.query_tracks`** is provided: merge/refine it; do not drop gaps.
   - Else: emit a single track `{ "gap_id": "_jd", "queries": [ ... ] }` with **≥2** queries for the whole JD.
2. Set **`query_family`** to the **deduplicated** list of all strings from **`query_tracks[].queries`**, trimmed to **5–12** strings if needed while preserving **≥2** queries per track (expand tracks before deduping if required).
3. **Query templates by artifact family** — align phrasing with [`../matching-lexicon.md`](../matching-lexicon.md) (PDF, spreadsheet, docx, slides pipeline, browser/MCP, social/platform, etc.). Example patterns:
   - `{artifact} skill SKILL.md agent` + `{artifact} {verb} github`
   - `{integration} MCP server skill` vs `{vendor} REST API` when JD demands tool discovery
   - `site:github.com` + repo-quality signals when hunting implementations
4. Add **site-scoped** variants where appropriate (e.g. `site:github.com` skill SKILL.md agent).
5. For each promising result, extract **trust_signals**: stars, maintainer, last commit, LICENSE, scope of file access, use of `curl|sh`.
6. **Typosquat / fork discrimination:** compare publisher/org, repo name, star count, last commit, and README overlap with JD; flag `risk_flags` such as `possible_typosquat`, `stale_fork`, `unrelated_scope` when similarity is superficial.
7. For each **`shortlist[]`** row, set **`covers_slots`**: array of **`slot_id`** / **`gap_id`** strings this package is meant to close (must align with **`query_tracks`** intent). Use `["_jd"]` when no capability slots were defined.
8. For each candidate, split host actions into:
   - **`safe_agent_actions`** — documented, vetted, non-destructive steps the agent may run once the candidate itself is approved.
   - **`user_gated_actions`** — network installs from untrusted sources, secrets, destructive changes, purchases, or anything else requiring explicit consent.
9. Produce **`install_command_template`** only for steps that remain gated or need user review before execution. **Host-specific install and verification** — read and align with:
   - [`../hosts/openclaw.md`](../hosts/openclaw.md) — e.g. `openclaw skills install`, list, gateway reload; never unvetted network shell without user OK.
   - [`../hosts/claude-code.md`](../hosts/claude-code.md) — plugins/marketplace vs git clone vs project/personal `.claude/skills/`; verify via user’s documented UI/CLI; never unvetted network shell without user OK.
   - **Cursor** — project rules / `AGENTS.md` and documented user skill dirs; copy/link vetted trees; do not assume `.claude/skills/` unless the workspace uses it.

   **P04 delta:** each `shortlist[]` row’s `safe_agent_actions` / `user_gated_actions` / `install_command_template` must be **consistent** with the chosen `host` doc above.

10. Attach **vetting_checklist** booleans to each candidate per **Vetting_checklist definitions**.
11. **Pre-`recommended` gate:** re-scan **`termination_log`** against the chosen **`recommended`** candidate's `source_url` and proposed id **before** finalizing output. Apply **`recommended` selection algorithm**.

## Output schema (JSON)

```json
{
  "query_tracks": [
    { "gap_id": "string", "queries": ["string"] }
  ],
  "query_family": ["string"],
  "shortlist": [
    {
      "name": "string",
      "source_url": "string",
      "covers_slots": ["string"],
      "trust_signals": ["string"],
      "risk_flags": ["string"],
      "safe_agent_actions": ["string"],
      "user_gated_actions": ["string"],
      "install_command_template": "string",
      "vetting_checklist": {
        "license_present": true,
        "no_arbitrary_network": true,
        "no_credential_exfil": true,
        "scoped_file_access": true
      },
      "fit_summary": "string"
    }
  ],
  "recommended": "string",
  "recruitment_notes": "string"
}
```

## Quality gates

- At least **3** distinct queries in **`query_family`** before giving up on search.
- **`query_tracks`:** required; must cover every **`jd.capability_slots[].slot_id`** when slots exist (one track per id).
- **`termination_log`:** no `recommended` candidate may violate the do-not-rehire rules in step 0 **or** step 9.
- Any candidate with **critical vetting failures** must not be `recommended`.
- For `host: openclaw`, the brief should make it obvious which next steps the agent can continue executing immediately after approval.

## Failure modes

- **Typosquatting** — Compare publisher, repo name, and description to JD; flag near-duplicates in `risk_flags`.
- **Stale skill** — If SKILL.md references dead APIs, flag `risk_flags: obsolete_api`.
