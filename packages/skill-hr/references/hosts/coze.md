# Coze (扣子) and similar plugin-first hosts

Use this when **skill-hr** (or a matched incumbent such as `coze-web-search`) runs on **Coze** or another host where **data collection depends on plugins / HTTP tools**, not only free-form chat text. If the incumbent is a multi-skill **employee** with **`soul_path`**, **SOUL governs** which skill (and thus which plugin/tool expectations) is active first; still enforce tool-first execution for whichever step requires external data.

## Why “strong match” can still look like a loop

Internal matching (P02) scores **skill descriptions and competencies** against the job. It does **not** prove that, in this session, the host **executed** the search (or other) plugin successfully. If the model never emits a valid plugin call, or the call fails and the model retries in natural language, the user may see many variants of “I will start searching…” with no data.

## Non-negotiable execution rules (incumbent + orchestrator)

1. **Tool-first:** After handoff (P03), the incumbent’s **first productive step** must be an **actual plugin or tool invocation** required by the **active** skill workflow (after reading **employee `SOUL.md`** when `soul_path` is set, then the relevant `SKILL.md`), e.g. web search—not a long preamble.
2. **At most one short intent line** before the first tool call (optional). **Do not** repeat paraphrases of “starting search / collecting data” without a tool call in between.
3. **Blocker once:** If the plugin is missing, disabled, rate-limited, or returns an error, respond with **one** concise message that includes the **host-reported error or observation**, then stop or escalate per `references/07-escalation.md`. **Do not** loop on the same preamble.
4. **Orchestrator:** The HR director flow must still **run the incumbent for real**: **`SOUL.md` first when `soul_path` is set**, then the **`SKILL.md`(s)** the SOUL specifies (otherwise the **`primary_skill`** `SKILL.md`). Treat “procedure-only” output as **incomplete** until the completion checkpoint or evidenced blocker (see `agents/hr-director/SOUL.md` and `references/prompts/P03-delegate-handoff.md`).

## Operator checks (runtime evidence on Coze)

In the Coze bot debugger or execution trace, verify for the failing turn:

- Whether a **plugin call** for the search skill was **recorded**.
- Success vs failure and **error text** if any.
- Whether the UI **concatenated** multiple model continuations into one bubble (retry / streaming artifact).

Use that trace—not repeated chat text alone—to distinguish “model stuck” from “plugin never ran.”

## Paste into Coze system prompt or P03 `handoff_message_template` (hard gate)

If the bot still prints many lines like “让我开始搜索…” with **no plugin execution in trace**, append **verbatim** (or translate labels only, keep structure):

**English (host-neutral wording):**

```text
[TOOL-FIRST GATE — non-optional]
After this handoff, your very next model action MUST be a real plugin/tool invocation required for data collection (e.g. web search). Rules:
- At most ONE short sentence of intent (≤20 words) before the first tool call; then call the tool immediately.
- FORBIDDEN: repeating “I will start searching / collecting data” or paraphrases without a successful tool call between them.
- If no tool can run: reply ONCE with "BLOCKER:" + exact host/plugin error or reason, then stop. Do not retry the same preamble.
```

**中文（可直接贴入人设/系统提示）：**

```text
【工具优先 — 必须遵守】
委派后，你的下一步必须是真实的插件/工具调用（例如联网搜索），而不是继续用自然语言描述“将要搜索”。
- 在第一次工具调用前，最多一句简短说明（不超过 20 字）；然后立刻调用工具。
- 禁止：在没有成功工具调用的前提下，反复改写“让我开始搜索/开始收集数据”等空话。
- 若无法调用工具：只回复一次「BLOCKER:」+ 平台/插件返回的具体错误或未启用原因，然后停止；不要重复开场白。
```

**Sync check:** If your Coze bot does not load this repo’s `references/hosts/coze.md`, paste the block above into the bot’s **system / persona / workflow pre-prompt** so the constraint actually reaches the model.
