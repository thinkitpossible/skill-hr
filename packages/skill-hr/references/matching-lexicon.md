# Matching lexicon (P02a recall hints)

Use for **broad recall** only: keyword and synonym alignment between JD text and skill text. **P02b** must still score with the full rubric and evidence quotes—never promote a skill on lexicon match alone.

## Artifact families

| Family | Example tokens |
|--------|----------------|
| PDF | pdf, acroform, xfa, fillable form, extract fields |
| Spreadsheet | xlsx, xls, csv (when JD means formulas/pivot—not plain parse), workbook |
| Word | docx, tracked changes, redline, OOXML |
| Slides | pptx, deck, speaker notes, slide master |
| Slides pipeline (decomposed) | storyline, outline, narrative arc, slide-by-slide plan, template, slide master, speaker notes, `.pptx` OOXML, python-pptx |
| Image raster | png, jpeg, sprite, transparency, bitmap generation |
| Image / visual sourcing | stock photo, reverse image, image search API, illustration brief, transparent png, sprite sheet |
| Image generation (AI raster) | text-to-image, diffusion, brand-safe imagery, mockup |
| Vector / code-native UI | svg path, html artifact, css-only layout, canvas-design, poster (static) vs editable pptx |

## Integration surfaces

| Surface | Example tokens |
|---------|----------------|
| Browser automation | playwright, chromium, dom, e2e, screenshot |
| MCP | model context protocol, mcp server, tool schema, fastmcp |
| Feishu / Lark | feishu, lark, wiki url, bitable |
| Git | rebase, branch strategy, trunk-based, merge conflict |
| Open web / search | web search, serp, indexed pages, news search |
| Social / forums (read) | timeline, hashtag, subreddit, thread, influencer mention (public) |
| Browser agent (broad) | open link, extract article, logged-in UI, multi-site workflow |

## Competency adjacency (often confused)

| JD intent | Often-wrong neighbor | Discriminant |
|-----------|----------------------|--------------|
| On-page SEO **audit** | SEO **content writing** | audit vs draft longform |
| Security **review** | Security **implementation** | findings vs code changes |
| **Interview design** from resume | **Resume writing** for job seeker | hiring manager vs candidate |
| **Skill / HR ops** | Generic **coding** skill | registry, install, JD/match language |
| **Notebook** authoring | **Python script** only | ipynb structure vs .py |
| **MCP** server | **REST** API only | host tool discovery vs HTTP routes |
| **Deck / `.pptx` authoring** | **HTML canvas / one-off poster** skill | editable slides vs static visual artifact; OOXML vs web artifact |
| **Outline / narrative for slides** | **pptx file skill only** | storyline and content architecture vs file assembly |
| **Image search / assets** | **Image generation** | licensed or found imagery vs synthetic raster |
| **Generic web search** | **Browser automation** or **vendor API** | indexable pages only vs SPA/login or official API |
| **Platform-specific connector** (e.g. Feishu) | **Generic browser agent** | typed API/docs vs fragile DOM scrape |
| **pptx / slides CLI** (library skill) | **presentation copywriting only** | file creation vs wordsmithing without OOXML |

## Meta routing

- If `must_have_competencies` or `search_queries` mention **skill install**, **registry**, **which skill to use**, **fire/remove skill**: include **`skill-hr`** in P02a candidates (if installed).
- Otherwise: **exclude `skill-hr`** from scoring pool per `SKILL.md` self-routing.

## Research surfaces (P01 slots)

When the JD uses **`capability_slots[].integration_surface`**, align recall tokens with [`11-research-and-platform-access.md`](11-research-and-platform-access.md)—do not collapse `social_read` or `browser_automation` into `open_web` unless the skill text explicitly covers that surface.
