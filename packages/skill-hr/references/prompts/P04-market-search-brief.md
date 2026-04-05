# P04 Market search brief (recruiting)

## Objective

Turn the JD into **search queries** and a **shortlist** of third-party skills to vet and install, separating actions the agent can execute from actions that still require user approval.

## Inputs

- `jd`: P01 JSON.
- `host`: `claude-code` \| `cursor` \| `openclaw` (affects install instructions).
- `denylist`: URLs or publishers to avoid (if user provided).

## Procedure

1. Build **query_family** (5–12 queries): keywords, task type, file formats, stack names.
2. Add **site-scoped** variants where appropriate (e.g. `site:github.com` skill SKILL.md agent).
3. For each promising result, extract **trust_signals**: stars, maintainer, last commit, LICENSE, scope of file access, use of `curl|sh`.
4. For each candidate, split host actions into:
   - **`safe_agent_actions`** — documented, vetted, non-destructive steps the agent may run once the candidate itself is approved.
   - **`user_gated_actions`** — network installs from untrusted sources, secrets, destructive changes, purchases, or anything else requiring explicit consent.
5. Produce **`install_command_template`** only for steps that remain gated or need user review before execution.
   - When `host` is **`openclaw`**, align with `references/hosts/openclaw.md`: prefer documented flows such as **`openclaw skills install …`**, copying a vetted local folder into a skill root, **`openclaw skills list`**, and a reload path such as a new session or **`openclaw gateway restart`**. Never run unvetted shell from the network without user OK.
   - When `host` is **`claude-code`**, align with `references/hosts/claude-code.md`: prefer **documented plugin / marketplace** install flows when the skill is shipped as a plugin; otherwise **`git clone`** or copy into **project** `<workspace>/.claude/skills/<name>/` (team-shared) or **personal** `~/.claude/skills/<name>/`. Verification must use **the user’s Claude Code version** (slash menu / documented listing)—do not invent version-specific CLI. Never run unvetted shell from the network without user OK.
6. Attach **vetting_checklist** booleans to each candidate.

## Output schema (JSON)

```json
{
  "query_family": ["string"],
  "shortlist": [
    {
      "name": "string",
      "source_url": "string",
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

- At least **3** distinct queries before giving up on search.
- Any candidate with **critical vetting failures** must not be `recommended`.
- For `host: openclaw`, the brief should make it obvious which next steps the agent can continue executing immediately after approval.

## Failure modes

- **Typosquatting** — Compare publisher, repo name, and description to JD; flag near-duplicates.
- **Stale skill** — If SKILL.md references dead APIs, flag `risk_flags: obsolete_api`.
