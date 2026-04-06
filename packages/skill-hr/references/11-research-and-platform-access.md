# Research surfaces and platform access

Use this reference when a JD involves **gathering evidence**, **monitoring sources**, or **acting through third-party platforms** (not only “run a web search”). It informs P01 `capability_slots[].integration_surface`, P02 disambiguation, P04 query tracks, and compliance notes.

## Information and execution surfaces

| Surface | Typical evidence or action | Skill / integration patterns |
|--------|----------------------------|------------------------------|
| **open_web** | Indexable pages, public docs | Generic web search, fetch, lightweight scraping where allowed |
| **news** | Articles, press, wire items | News APIs, RSS, dated search operators |
| **forums** | Threads, Q&A, long-tail discussion | Forum-specific APIs, export tools, or browser automation where policy allows |
| **social_read** | Posts, profiles, public timelines | Official APIs, documented export, or user-assisted capture—**not** credential stuffing or ToS violations |
| **browser_automation** | Logged-in or dynamic UIs (SPA, captchas) | Playwright-style skills, browser MCP; often **user_gated** (session, login) |
| **mcp_tools** | Host-exposed tools with schemas | MCP server skills, FastMCP; map each platform need to a **named** tool surface |
| **vendor_api** | First-party REST/GraphQL/SDK | Feishu, Slack, GitHub, etc.—match **vendor** in JD to connector skills |
| **cli** | Local binaries, CLIs | `pptx`, `ffmpeg`, `op`, documented CLIs in `tools_and_access` |
| **local_files** | Workspace-only inputs | No network; parsing, conversion, batch files |
| **unknown** | Surface not yet classified | Use only briefly; replace in `risk_notes` once clarified |

**Rule:** “Internet research” is **not** one surface. Split **where** answers may live (open web vs forum vs social vs app-in-browser) into slots or workstreams so P02 and P04 do not default to a single generic search skill.

## Recruitment implications

1. **Match surface to skill type** — A skill that only issues search queries does **not** satisfy `browser_automation` or `vendor_api` slots unless its body commits to that stack.
2. **MCP and APIs** — When `integration:mcp` or `vendor_api` appears in tags, P04 should include queries such as `{platform} MCP server skill`, `{vendor} API agent skill SKILL.md`, not only `site:github.com` generic terms.
3. **Human-gated access** — Logins, OAuth, 2FA, and enterprise SSO usually imply **`user_gated_actions`** in P04 and explicit **`risk_notes`** on the JD (credentials, session handoff).
4. **Smoke tasks** — After install, smoke scope should reflect the **surface** (e.g. “fetch one public page” vs “invoke one MCP tool” vs “open browser to localhost”), not a unrelated generic task.

## Compliance and ToS (non-negotiable)

- **Do not** instruct skills or users to bypass authentication, rate limits, paywalls, or robots/terms restrictions.
- **Do not** present scraping behind login as “research” without user ownership of the account and acceptance of platform rules.
- When `social_read` or `browser_automation` touches third-party UIs, add **`risk_notes`** and P04 **`risk_flags`** for automation policy, account liability, and data handling.
- Veto conditions in [`01-competency-model.md`](01-competency-model.md) still apply; skills that encourage exfiltration or blind remote execution remain **out of bounds**.

## Links

- JD decomposition: [`02-jd-spec.md`](02-jd-spec.md) (`capability_slots[]`).
- P02 recall hints: [`matching-lexicon.md`](matching-lexicon.md).
- Market search: [`04-market-recruitment.md`](04-market-recruitment.md), [`prompts/P04-market-search-brief.md`](prompts/P04-market-search-brief.md).
