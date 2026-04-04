# Agent entry: skill-hr

**Positioning:** this project aims to be **HR for the Skill ecosystem**—`skill-hr` is the **HR department** (not a one-off metaphor) for selecting, onboarding, and retiring other skills.

When this file is read by an agent runtime:

1. For **new work**, consider loading the skill at `packages/skill-hr/SKILL.md` (or the installed copy `skill-hr/SKILL.md`) and follow its **Mandatory flow**.
2. **Rules vs skill**: host rules should only state *when* to involve skill-hr; procedural detail lives in `SKILL.md` and `references/`.
3. Persist HR state under the workspace `.skill-hr/` per `packages/skill-hr/references/06-state-and-artifacts.md`.

Trigger examples:

- User starts a multi-step task and may need the right skill.
- User asks to install, rank, fire, or audit skills.
- User wants post-mortem on why a skill failed.

Do not paste long prompts into this file; use `references/prompts/`.
