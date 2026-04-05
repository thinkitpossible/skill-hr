# Market recruitment (external skills)

## Goals

Find a **third-party** skill when internal pool fails. Maximize fit and safety; minimize surprise installs; keep the framework moving until a real approval gate or blocker is hit.

## Search strategy

1. Start from P04 `query_family`.
2. Prefer sources with **readable SKILL.md** or manifest before install:
   - GitHub / GitLab repositories with `SKILL.md` or `skills/` layout
   - Curated marketplaces or registries the user trusts
3. Prefer **narrow** skills over "god" skills that try to do everything.

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
