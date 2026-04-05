# Host adapter: Claude Code

**HR deployment note:** On Claude Code, `skill-hr` runs the same JD → match → recruit → handoff → performance / termination loop as in `SKILL.md`. Registry and incidents use **workspace** paths from `references/06-state-and-artifacts.md` (`.skill-hr/`) so HR records can live in the repo.

## Source of truth (keep current with upstream)

Authoritative behavior changes with Claude Code releases. Prefer:

- [Extend Claude with skills](https://docs.anthropic.com/en/docs/claude-code/skills) (locations, precedence, frontmatter, plugins)
- [Claude Code documentation](https://docs.anthropic.com/claude-code) (index)

## Where skills load from (precedence)

When the **same skill name** exists in more than one place, **higher row wins** (enterprise overrides personal overrides project). **Plugin** skills use a separate namespace so they do not collide with disk skills.

| Precedence (high → low) | Typical path / meaning |
|-------------------------|----------------------|
| Enterprise | Managed org settings (see [settings](https://docs.anthropic.com/en/settings#settings-files)) |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` — all your projects |
| Project | `<workspace>/.claude/skills/<skill-name>/SKILL.md` — this repo only |
| Plugin | Skills shipped inside an enabled plugin; invoked as **`plugin-name:skill-name`** (namespaced) |

**Windows:** personal root is `%USERPROFILE%\.claude\skills\`.

**Nested discovery (monorepos):** While you work under subdirectories, Claude Code can also discover skills under nested `.claude/skills/` (e.g. `packages/frontend/.claude/skills/…`). Treat every such tree as an additional **candidate root** for P02.

**`--add-dir`:** Directories granted via `--add-dir` are primarily for file access, but **`.claude/skills/` inside those directories is an exception**: those skills load and participate in discovery. Other `.claude/` config from add-dir may not load the same way—see the [permissions / additional directories](https://docs.anthropic.com/en/permissions#additional-directories-grant-file-access-not-configuration) docs.

## Installing `skill-hr`

1. Copy this repository folder **`packages/skill-hr/`** into a skill root as **`skill-hr/`**, preserving **`references/`**, **`scripts/`**, **`schemas/`**, so `SKILL.md` resolves as **`skill-hr/SKILL.md`**.
2. **Typical choices:**
   - **All your projects:** `~/.claude/skills/skill-hr/`
   - **This repo only:** `<workspace>/.claude/skills/skill-hr/` (good for team sharing via git)
3. **Reload:** start a new session or use whatever your CC version documents for picking up new skills; confirm the skill appears in the slash menu or skill listing for that version.

## Discovering the installed pool for P02 (checklist)

Build `candidates` by **merging** filesystem discovery, **plugin / session listings**, and **`.skill-hr/registry.json`**. Do **not** assume a single skills root.

1. **Project root:** `<workspace>/.claude/skills/*/` — each immediate child with `SKILL.md`.
2. **Nested roots:** under `<workspace>`, find other `**/.claude/skills/` directories (respect cost: prefer `packages/`, skip heavy trees like `node_modules/`, `.git/`). Each child folder with `SKILL.md` is one skill.
3. **Personal:** `~/.claude/skills/*/` (if policy allows reading outside the workspace).
4. **Add-dir roots:** for each `--add-dir` path the user/session reports, repeat step 1–2 under that directory.
5. **Plugin skills:** agents often **cannot** enumerate every plugin-only skill from disk alone. Ask the user to paste **slash-menu / skill list** output, or merge names like `plugin:skill` when known. Flag unknown provenance in `gaps` / notes.
6. **Registry merge:** for each discovered skill `id`, attach `registry_status`, stats, and `notes` from `.skill-hr/registry.json` when present. Optionally persist `cc_scope` / `cc_invoke` per `06-state-and-artifacts.md`.

**Helper:** run `python packages/skill-hr/scripts/scan_claude_code_skills.py` from the workspace for a JSON snapshot of on-disk skills (see script docstring for plugin limitations).

### Frontmatter and delegation policy (P02)

Read each `SKILL.md` frontmatter in addition to body excerpts. Fields that affect HR behavior:

| Frontmatter | HR implication |
|-------------|----------------|
| `disable-model-invocation: true` | Model should **not** auto-run this skill; user typically invokes `/skill-name`. For P02: still score fit, but prefer **`decision: confirm`** (or explicit user `/skill`) over auto-`delegate` unless the user already asked to run that skill. |
| `user-invocable: false` | Background / Claude-only skill; user slash menu may hide it—do not assume the user can `/invoke` it. |
| `paths` | Auto-load may be limited to matching files; if current task files do not match, add a **`gaps`** note (“skill may not auto-activate for this path set”). |
| `context: fork` / subagent | Handoff (P03) should mention isolation or tooling limits if relevant. |

**Description length:** Claude Code may truncate descriptions in listings (~250 characters). Prefer reading full `SKILL.md` for P02 excerpts.

## Recruitment and install (market vs git vs copy)

- **Marketplace / plugins:** When a vetted skill is published as a plugin, prefer the **documented** install path for your CC version (e.g. plugin marketplace flows described in official skills docs). Still run **vetting** (`references/01-competency-model.md`, `04-market-recruitment.md`); marketplace ≠ trusted by default.
- **Public git:** `git clone` or copy the skill folder into **project** `.claude/skills/<name>/` (team-visible) or **personal** `~/.claude/skills/<name>/`, then verify the skill is visible for the session.
- **No silent risk:** never run unvetted `curl | sh` or delete skill trees without explicit user confirmation.

After install, register in `.skill-hr/registry.json` with `status: on_probation` and `source_url` when known; run a **smoke** task before full delegation (`04-market-recruitment.md`).

## Verification (non-prescriptive)

Exact commands and UI differ by Claude Code version. After install or recruitment, confirm using **that version’s** documented method (e.g. skill appears in the `/` menu, or a documented list command). Do not hard-code brittle CLI strings in incidents; record **what was verified** in human terms.

## Tools assumption

Claude Code agents typically have shell, file read/write, and optional MCP. Recruitment flows should **prefer** reproducible `git clone` or documented plugin install over opaque installers when the source is public and vetted.

## Incident and registry paths

Use **workspace root** paths from `references/06-state-and-artifacts.md` so HR state travels with the repo when desired.

## Maintenance

When Claude Code changes default paths, precedence, or frontmatter keys, update this file in **one focused edit** and align P02/P04 host notes if needed.
