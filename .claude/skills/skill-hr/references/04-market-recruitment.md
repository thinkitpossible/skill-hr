# Market recruitment (external skills)

## Goals

Find a **third-party** skill when internal pool fails. Maximize fit and safety; minimize surprise installs; keep the framework moving until a real approval gate or blocker is hit.

**Surfaces and access:** When the JD involves research beyond open-web search, platforms, or logged-in UIs, read [`11-research-and-platform-access.md`](11-research-and-platform-access.md) and align queries to **integration surfaces**, not one blended “best skill” search.

## Do-not-rehire gate (registry)

Before recommending or installing a candidate, read `.skill-hr/registry.json` **`termination_log[]`** (and `skills[]` / `employees[]` status):

- **Exclude** any market candidate whose logical `skill_id` matches a log entry with `kind: skill`, `rehire_allowed: false`.
- **Exclude** candidates whose **`source_url`** matches a terminated skill’s `source_url` on a log row with `rehire_allowed: false` (same package must not be auto-recruited again).
- Do not propose re-installing an **employee** identity that appears as `kind: employee` with `rehire_allowed: false`; design a new employee id if the user truly wants a replacement bundle.

If the only viable candidates are blocked by this gate, document it and follow [07-escalation.md](07-escalation.md) or obtain explicit user direction to set `rehire_allowed: true` with rationale.

## Search strategy

1. Start from **`p04_recruitment_brief`** (when present): each **`gaps[]`** / JD **`capability_slots[]`** row must have **≥2** targeted queries in P04 **`query_tracks[]`** for that `gap_id` / `slot_id` (see [`prompts/P04-market-search-brief.md`](prompts/P04-market-search-brief.md)).
2. Build **`query_family`** as the **deduplicated union** of all track queries (5–12 strings total when possible), so legacy consumers still see one flat list.
3. **Multi-channel** (use as appropriate; do not rely on a single generic web search):
   - GitHub / GitLab: `SKILL.md`, `skills/` layout, `site:github.com`
   - MCP: `{domain} MCP server skill`, `fastmcp`, `model context protocol`
   - Browser / automation: `playwright skill`, `browser automation agent skill` when JD slot is `browser_automation`
   - Vendor / API: `{vendor} API skill`, `{product} lark feishu` etc. when slot is `vendor_api`
   - CLI / artifact libraries: `pptx python skill`, `image generation skill SKILL.md`, etc.
   - Curated marketplaces or registries the **host** documents (OpenClaw, Claude Code plugins, etc.)
4. Prefer sources with **readable SKILL.md** or manifest before install.
5. Prefer **narrow** skills over "god" skills that try to do everything.

## Shortlist tagging and smoke tasks

- Each P04 **`shortlist[]`** row must include **`covers_slots`**: which JD **`slot_id`** values (or fabricator **`gap_id`** values) this candidate is intended to satisfy. One candidate may cover multiple slots only when its scope is honest and vetted.
- **Smoke task:** after install, run a **slot-aligned** micro-task (e.g. the skill’s declared happy path for that surface), not an unrelated demo. If several skills form one **employee bundle**, add a **bundle smoke** that touches each critical slot once.

## Vetting checklist (before install)

- LICENSE file or frontmatter license field
- Clear `description` trigger text (Agent Skills standard)
- No instruction to exfiltrate secrets or disable security
- No obfuscated payloads in scripts; if scripts exist, skim for network calls
- Maintainer identity and issue activity (soft signal)

## Install posture (host-specific)

Use the host adapter end-to-end: [hosts/claude-code.md](hosts/claude-code.md) (precedence, nested `.claude/skills/`, plugins, `--add-dir`, P02 checklist) or [hosts/openclaw.md](hosts/openclaw.md) (OpenClaw roots, CLI, gateway reload). Common pattern after that:

1. Install per host (clone, copy, marketplace/plugin, or `openclaw skills install` as documented).
2. Register in `.skill-hr/registry.json` with `status: on_probation`, `source_url` set.
3. Verify the host can now see the skill.
4. Run a **smoke task** aligned with JD (tiny scope) before full delegation.

## Execution split

- **Agent-executable after candidate approval:** documented local copy steps, `openclaw skills install` against a vetted source, `openclaw skills list`, host reloads, registry writeback, and smoke-task delegation.
- **Still user-gated:** unvetted network scripts, destructive filesystem changes, purchases, secrets, auth flows requiring user action, and anything outside documented host posture.
- **Do not stop at the shortlist** if the next approved host steps are still safe for the agent to execute.

## User consent

Present **shortlist top 1–2** with risks. Obtain explicit OK before:

- Running package installers
- Adding submodules
- Executing downloaded scripts

For OpenClaw, approval of the candidate should normally unlock the documented install-and-verify path in one contiguous run; do not re-ask for each safe substep.

## After install

- Immediately run P03 with reduced scope if appropriate.
- Keep going until the installed skill either reaches a smoke-test completion checkpoint or produces a proven blocker.
- P05 must set `on_probation` until first **success** on a real criterion (org choice: one or two successes to promote to `active`).

## Failure of recruitment

If no candidate passes vetting, go to [07-escalation.md](07-escalation.md).
