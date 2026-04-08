# skill-hr

**语言 / Language:** 简体中文（本页） | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Anthropic-blue)](https://support.anthropic.com/en/articles/12580037-what-are-skills)
[![agentskills.io](https://img.shields.io/badge/spec-agentskills.io-8A2BE2)](https://agentskills.io)

[![GitHub stars](https://img.shields.io/github/stars/thinkitpossible/skill-hr?style=social&label=Star)](https://github.com/thinkitpossible/skill-hr)

**Meta Agent Skill · Skill 生态 HR / 编排**

> **技能装了一箩筐，任务一来还是不知道派谁？**  
> **别再加插件了，先给宿主招个 HR。**

你的同事、朋友、专家顾问都已经装进 Skills 里，但他们不总能稳定交付——任务一来，你还是在「随便点一个试试」和「要不再装一个」之间反复横跳。你缺的不是更多图标，而是一个敢留任、敢淘汰、敢记账的 HR：`skill-hr` 不替你写代码或做表，它负责招人、选人、派工、试用、复盘与台账，让你从「插件收藏家」变成能拍板的人。

![技能人事主视觉](docs/readme-assets/01-hero-skill-hr.png)

- **JD 结构化**：任务先落成岗位说明（P01），再谈派谁；支持 **`workstreams[]` 多流编排**（按 `depends_on` / `parallel_group` 驱动 P02→P03→执行→P05）。
- **内池打分**：已安装技能按 rubric 匹配（P02），不是拍脑袋。
- **招聘 + 台账**：弱匹配 / 无匹配时先由 **`employee-fabricator`** 冷启动目标员工与 P04 简报，再走市场简报与 vetting（P04）；**registry / incidents** 当 HRIS；默认 **逻辑淘汰**（`terminated`），**物理卸载只在你点头之后**。
- **员工层升级**：`registry.json` 现支持 **`employees[]` 多技能员工**（示例见 [`registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json)）；**`trainer`** 负责设计与再训练（P07/P08）。
- **研究与平台类任务**：P01 可叠加 [`11-research-and-platform-access.md`](packages/skill-hr/references/11-research-and-platform-access.md)（调研面、平台权限、合规）。
- **多角色 HR 部门（可选）**：除「单会话跑完全流程」外，可按角色拆分——[`agents/`](packages/skill-hr/agents/) 下每人格一份 `SOUL.md`，共享规则见 [`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md)；任务看板与合法状态迁移由 [`scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py) 写入 **`.skill-hr/hr_tasks.json`**（详见 [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)）。

开源 **元 [Agent Skill](https://support.anthropic.com/en/articles/12580037-what-are-skills)**：把 Skill 当成一支要管编制、招聘、绩效的队伍——**可执行的 people-ops**，不是一句比喻。可安装包在 [`packages/skill-hr/`](packages/skill-hr/)。

<span id="positioning"></span>

## 定位：不是多一个业务 Skill，而是人事部

装了一百个 skill，若没有 JD、没有打分、没有试用与台账，生态只会越来越像杂货铺——热闹，但不运转。`skill-hr` 不负责写代码、画图、做表、分析 PDF——这些仍由领域 skill 完成。它负责的是组织层：把任务落成 JD（P01）、在内池按 rubric 匹配（P02）、委派与交接（P03）、市场招聘与 vetting（P04）、试用复盘（P05）、绩效与逻辑淘汰（P06），并把状态写进 **registry / hr_tasks / incidents**。

**一句话：业务 skill 负责干活，`skill-hr` 负责组织。**

---

<span id="workflow-p01-p06"></span>

## 工作流程（P01–P06）

任务进门，先别抓阄选人——按下面这条流水线走，每一步都有模板、有产物、有台账。整套能力不是一句比喻，而是一套可执行的 HR 生命周期（总调度见 [`SKILL.md`](packages/skill-hr/SKILL.md)，阶段模板见 [`references/prompts/`](packages/skill-hr/references/prompts/)）。

![技能人事生命周期图](docs/readme-assets/02-lifecycle-flow.png)

- **P01 — Intake → JD**：把模糊需求落成岗位说明（目标、输入输出、风险与完成标准）。
- **P02 — Match Installed**：用 JD 对已在册技能池打分，不靠拍脑袋。
- **P03 — Delegate / Handoff**：给出可交接包（边界、产出、验收口径）。
- **P04 — Recruit**：内池不够再外招；先 brief、再 vetting、再安装。
- **P05 — Trial / Debrief**：试用与复盘，输出可校验结构（[`p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json)）。
- **P06 — Performance / Termination**：默认 **逻辑淘汰**（`terminated`）；物理卸载仅在你确认并完成路径审计之后。

---

<span id="quick-start"></span>

## 30 秒上手

1. 将 [`packages/skill-hr/`](packages/skill-hr/) **复制**到宿主 skills 目录下的 **`skill-hr/`**，确保存在 **`skill-hr/SKILL.md`**。
2. **Claude Code**：读 [`references/hosts/claude-code.md`](packages/skill-hr/references/hosts/claude-code.md)。常见路径：`<repo>/.claude/skills/skill-hr/` 或 `~/.claude/skills/skill-hr/`。
3. **OpenClaw**：读 [`references/hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md)。

**可选：内池扫描（P02 辅助）**

```bash
python packages/skill-hr/scripts/scan_claude_code_skills.py <工作区> [--include-user]
```

**可选：校验 HR 台账 JSON**

```bash
python packages/skill-hr/scripts/validate_registry.py .skill-hr/registry.json
```

**可选：多角色模式下的任务看板（状态机 + 流转审计）**

在工作区根目录执行（首次 `create` 会创建 `.skill-hr/`）：

```bash
python packages/skill-hr/scripts/hr_dispatch.py create HR-20260405-001 "示例任务"
python packages/skill-hr/scripts/hr_dispatch.py state HR-20260405-001 JDReady "P01 完成"
python packages/skill-hr/scripts/hr_dispatch.py list
```

完整示例见 [`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md)。

**可选：启动本地 Dashboard（业务看板 + 员工看板 + 归档 + 模板）**

在仓库根目录一键构建前端并启动 API + 静态站（默认端口 `8787`）：

```bash
python packages/skill-hr/scripts/launch_dashboard.py --workspace-root .
```

OpenClaw 上需要 agent 执行完即返回时，加 **`--background`**。仅拷贝了 `skill-hr/` 技能目录、没有本仓库的 `dashboard/` 时，请用完整 clone，或按 [`references/hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md) 用手动 `server.py --static-dir …`。可复制规则/工具说明见 [`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md)。

然后打开 `http://127.0.0.1:8787`。服务会复用工作区根目录下的 `.skill-hr/registry.json`、`.skill-hr/hr_tasks.json` 与 `incidents/`。

![运行时台账与 Dashboard 示意](docs/readme-assets/04-runtime-dashboard.png)

Dashboard 背后是三份台账 **`registry.json` / `hr_tasks.json` / `incidents/`**——不是一次性派工界面，而是带记忆与审计语义的 **Skill HRIS**（规范见 [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)）。

建议在项目说明（如 `CLAUDE.md`）里 **一句话写清何时启用 skill-hr**；细则只在 `SKILL.md` 与 `references/`。**规则负责喊开工，skill 负责教怎么干。**  
技能旁的 `.skillhub.json`（若有）是集市元数据；人事记录请用 **`.skill-hr/registry.json`**；多角色编排时另有一份 **`.skill-hr/hr_tasks.json`**。

---

## 目录

- [定位](#positioning)
- [工作流程（P01–P06）](#workflow-p01-p06)
- [30 秒上手](#quick-start)
- [多角色 HR 部门](#multi-agent)
- [为什么是 skill-hr](#why-skill-hr)
- [宿主支持](#hosts)
- [没有 HR vs 有 skill-hr](#before-after)
- [能力一览](#features)
- [OpenClaw：完成优先](#openclaw-completion)
- [架构与图示](#architecture)
- [文档（Reference）](#doc-map)
- [Cursor 与 AGENTS](#cursor-agents)
- [安全](#safety)
- [框架测评](#evaluation)
- [校验 registry](#validate-registry)
- [适合谁](#for-who)
- [常见问题（FAQ）](#faq)
- [许可证](#license)

---

<span id="why-skill-hr"></span>

## 为什么是 skill-hr

大多数人的技能生态会逐渐变成：越装越乱、靠感觉派工、家里有人仍想外装、失败了就换下一个、一句「删掉」却动到真目录。这不叫体系，叫撞大运。`skill-hr` 的目标很简单：**把 Skill 世界从「凑合用」拉成「像公司一样运转」的可执行流程**。

- **技能越多，越难选对**：缺统一 JD 与打分标准，委派靠直觉。
- **内池与市场脱节**：不知道「家里有没有合适的人」，出门安装又缺 vetting 与交接剧本。
- **翻车没台账**：谁稳、谁该 probation、谁该逻辑淘汰，没有结构化记录。
- **「删技能」语义危险**：必须区分 **从委派池移除** 与 **动磁盘上的目录**。

skill-hr 把上述环节写进 [`SKILL.md`](packages/skill-hr/SKILL.md) 与 `references/`，用 **P01–P08** 提示词模板（P01–P06 主流程，P07/P08 员工设计与训练）驱动，状态落在工作区 **`.skill-hr/`**（见 [`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)）。

---

<span id="multi-agent"></span>

## 多角色 HR 部门

宿主支持 **多个 agent 会话** 时，可把 HR 拆成专职角色（类似多代理编排里的「分角色、可审计」思路；概念上可参考社区项目 [edict](https://github.com/cft0808/edict) 的多 Agent 分工）。**单会话宿主** 仍由一份 `SKILL.md` 按 Mandatory flow 顺序执行即可；也可由 **hr-director** 人格在内部按阶段加载各 `SOUL.md`。

| Agent ID | 职责摘要 |
|----------|----------|
| `hr-director` | 编排、对用户沟通、分支决策 |
| `job-analyst` | P01 岗位说明 / JD |
| `talent-assessor` | P02 内池匹配与打分 |
| `employee-fabricator` | 冷启动目标多技能员工、P04 招聘简报（外招前） |
| `recruiter` | P04 市场搜索与安装协调 |
| `compliance` | 安全与 veto 门禁 |
| `onboarder` | P03 委派与交接包 |
| `perf-manager` | P05 复盘 / P06 淘汰 |
| `trainer` | 员工设计 / 再训练（P07/P08） |
| `hris-admin` | registry、incidents 规范落盘 |

![多角色人事部门示意](docs/readme-assets/03-hr-department-org-chart.png)

- **全员必读**：[`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md)（权限矩阵、红线、`hr_dispatch.py` 用法）
- **各角色细则**：[`agents/*/SOUL.md`](packages/skill-hr/agents/)
- **走通示例**：[`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md)

---

<span id="hosts"></span>

## 宿主支持

| 宿主 | 状态 | 说明 |
|------|------|------|
| **Claude Code** | 主推 | 路径优先级、嵌套 `.claude/skills/`、`--add-dir`、插件技能发现等见 [`hosts/claude-code.md`](packages/skill-hr/references/hosts/claude-code.md)；P02 建议配合磁盘扫描脚本。 |
| **OpenClaw** | 主推 | 把本包当作 **Skill 的专职 HR** 部署；完成优先语义见下文。详见 [`hosts/openclaw.md`](packages/skill-hr/references/hosts/openclaw.md)。 |
| **Coze** | 参考 | 插件优先、工具先于闲聊等见 [`hosts/coze.md`](packages/skill-hr/references/hosts/coze.md)。 |
| **Cursor** | 可选 | 用项目规则决定何时加载 skill-hr，见 [`.cursor/rules/skill-hr-always.mdc`](.cursor/rules/skill-hr-always.mdc)（可按需改 `alwaysApply` / `globs`）。 |

---

<span id="before-after"></span>

## 没有 HR vs 有 skill-hr

| 没有 HR | 有 skill-hr |
|---------|-------------|
| 任务开口就随手选一个技能或再装一个 | 先 **结构化 JD**（P01），再按 rubric **内池打分**（P02） |
| 市场 skill 直接 `curl \| sh` | **搜索简报 + vetting**（P04），安装与交接有剧本 |
| 失败了就「换一个」 | **试用与复盘**（P05）、**淘汰报告**（P06），registry/incidents 留痕 |
| 「删掉」可能误删目录 | 默认 **逻辑终止**（`terminated`）；**物理卸载**需你确认 + 路径审计 |

![有无 HR 的对照（老板模式）](docs/readme-assets/05-boss-mode-matrix.png)

**差异化一句话**：skill-hr 默认把「开除」做成 **台账里的逻辑淘汰**；真要删目录，必须你走显式确认流程。`skill-hr` 不是让你再多一个「会聊天的员工」，而是让你第一次拥有可审计的 **人事部**：知道谁该上、谁该招、谁该留、谁该被淘汰。

---

<span id="features"></span>

## 能力一览

<details>
<summary><strong>展开：完整功能清单与链接</strong></summary>

- **编排与门禁**：[`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md)（Mandatory flow、自路由、安全门、多角色说明）
- **多角色全局规则**：[`agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md)；**各角色 SOUL**：[`agents/`](packages/skill-hr/agents/)
- **任务看板 CLI**：[`scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py)
- **多角色示例**：[`examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md)
- **员工手册**（能力模型、JD、匹配、招聘、绩效、淘汰、训练设计、多技能员工、调研与平台）：[`references/`](packages/skill-hr/references/)（含 `09`–`11`）
- **可执行提示词 P01–P08**：[`references/prompts/`](packages/skill-hr/references/prompts/)
- **宿主安装说明**（Claude Code / OpenClaw / Coze）：[`references/hosts/`](packages/skill-hr/references/hosts/)
- **registry / incident / hr_tasks 格式**：[`06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md)
- **示例 registry**：[`examples/registry.example.json`](packages/skill-hr/examples/registry.example.json)、[`examples/registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json)（`employees[]`）
- **JSON 校验**：[`scripts/validate_registry.py`](packages/skill-hr/scripts/validate_registry.py)
- **全栈测评 L0–L7**（P02 基准 = 其中 L2）：[`08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md)
- **P02 黄金集与指标**：[`benchmarks/matching/`](packages/skill-hr/benchmarks/matching/)
- **P02 / P05 输出 Schema**：[`schemas/p02-output.schema.json`](packages/skill-hr/schemas/p02-output.schema.json)、[`schemas/p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json)
- **基准打分**：[`scripts/compare_matching_benchmark.py`](packages/skill-hr/scripts/compare_matching_benchmark.py)、[`scripts/run_matching_benchmark_llm.py`](packages/skill-hr/scripts/run_matching_benchmark_llm.py)（可选 OpenAI 兼容 API）
- **Claude Code 磁盘技能扫描（P02 辅助）**：[`scripts/scan_claude_code_skills.py`](packages/skill-hr/scripts/scan_claude_code_skills.py)
- **本地人事看板（Dashboard）**：仓库 [`dashboard/`](dashboard/) + 一键启动 [`scripts/launch_dashboard.py`](packages/skill-hr/scripts/launch_dashboard.py)；OpenClaw 场景下的复制与工具说明见 [`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md)

</details>

---

<span id="openclaw-completion"></span>

## OpenClaw：完成优先

尤其在 OpenClaw 这类宿主上，skill-hr 的哲学可以概括成：**能推进就推进，能完成就别只汇报计划**；仅当遇到真实门禁或 **blocker** 再拉回用户拍板。

在 OpenClaw 上，框架按 **完成优先** 执行：能继续推进的文档化、已 vet、风险可控的步骤，agent 应做到 **真实完成检查点** 或证明 **blocker** 再汇报。

- **`delegate`**：**立即委派并继续跑**，直到被委派方完成或证明卡住。
- **`confirm`**：只用于 **真实用户门禁**（破坏性操作、缺凭证、只能手动的宿主步骤）。
- **招聘简报**区分 **agent 可继续** 与 **必须用户点头** 的步骤。
- **阶段流水账**进 `.skill-hr/incidents/`；对用户默认给 **结果、产物、待决与 blockers**。

<details>
<summary><strong>展开：完整表述（与上一版一致）</strong></summary>

在 OpenClaw 上，框架按 **完成优先** 执行：只要下一步是文档化、已 vet、且风险可控的宿主动作，agent 应继续推进，直到达到真实 **完成检查点** 或能证明 **blocker**，再向用户汇报。

- **`delegate`**：**立即委派并继续跑**，直到被委派方到达完成点或证明卡住。
- **`confirm`**：只用于 **真实用户门禁**（破坏性操作、缺凭证、只能手动触发的宿主步骤等）。
- **招聘简报**会区分 **agent 可继续执行的步骤** 与 **必须用户点头的步骤**，便于在批准候选 skill 后连贯完成安装、验证与冒烟委派。
- **阶段级流水账**优先写入 `.skill-hr/incidents/`；对用户回复默认给 **结果、产物、待决与 blockers**，而非长篇「我接下来打算怎么做」。

</details>

---

<span id="architecture"></span>

## 架构与图示

<details>
<summary><strong>图示 1：HR 生命周期（编排状态机）</strong></summary>

用户一开口，后台走 **招聘 → 试用 → 复盘 → 留任或优化 → 缺人再补**。

```mermaid
stateDiagram-v2
  direction LR
  [*] --> Intake: 用户任务
  Intake --> JD: 分析JD
  JD --> MatchInstalled: 技能池打分
  MatchInstalled --> Delegate: 最佳高于阈值
  MatchInstalled --> Recruit: 低于阈值
  Delegate --> Debrief: 任务结束
  Debrief --> Retain: 成功
  Debrief --> Terminate: 失败
  Recruit --> Trial: 安装与交接
  Trial --> Debrief
  Terminate --> Recruit: 重试或升级
  Retain --> [*]
```

</details>

<details>
<summary><strong>图示 2：四步映射（HR 在做什么）</strong></summary>

```mermaid
flowchart TB
  subgraph step1 [步骤1 岗位JD]
    A[用户新任务] --> B[结构化JD\nP01 + jd-spec]
  end
  subgraph step2 [步骤2 内部匹配]
    B --> C{已安装技能\n分数达阈值?}
    C -->|是| D[委派 P03\n写 incident]
  end
  subgraph step3 [步骤3 市场招聘]
    C -->|否| E[联网搜索简报 P04\n背调与安装]
  end
  subgraph step4 [步骤4 试用与HR记录]
    E --> F[试用执行 + 复盘 P05]
    D --> F
    F --> G{结果}
    G -->|成功| H[留任 / 更新 registry]
    G -->|失败| I[registry 标记淘汰 P06\n卸载需用户确认]
    I --> E
  end
```

</details>

<details>
<summary><strong>图示 3：仓库布局 vs 运行时产物</strong></summary>

```mermaid
flowchart LR
  subgraph repo [仓库根目录]
    R[README.md]
    A[AGENTS.md]
    CR[.cursor/rules]
    D[dashboard 前端]
  end
  subgraph pkg [packages/skill-hr 技能包]
    S[SKILL.md]
    AG[agents GLOBAL + SOUL]
    REF[references/00-11 等]
    PR[prompts P01-P08]
    HO[hosts CC+OC+Coze]
    SC[scripts validate + hr_dispatch + launch_dashboard]
  end
  subgraph runtime [工作区运行时产物]
    REG[.skill-hr/registry.json]
    TASKS[.skill-hr/hr_tasks.json]
    INC[.skill-hr/incidents/]
  end
  repo --> pkg
  pkg -.->|创建或更新| runtime
```

</details>

**体量参考**：`packages/skill-hr/` 内约 **40** 个 `.md`（含 `SKILL.md`、`references/00–11`、`matching-lexicon`、**P01–P08** 提示词、**4** 份宿主说明、`agents/GLOBAL.md` 与 **10** 份 `agents/*/SOUL.md` 等）；另含仓库级文档与脚本。

---

<span id="doc-map"></span>

## 文档（Reference）

<details>
<summary><strong>展开：文档地图</strong></summary>

| 你要找 | 链接 |
|--------|------|
| 编排大脑（触发、流程、门禁） | [`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md) |
| 多角色规则与各 agent | [`packages/skill-hr/agents/GLOBAL.md`](packages/skill-hr/agents/GLOBAL.md)、[`packages/skill-hr/agents/`](packages/skill-hr/agents/) |
| HR 任务看板 CLI | [`packages/skill-hr/scripts/hr_dispatch.py`](packages/skill-hr/scripts/hr_dispatch.py) |
| 多角色流程示例 | [`packages/skill-hr/examples/multi-agent-flow.md`](packages/skill-hr/examples/multi-agent-flow.md) |
| 手册全集 | [`packages/skill-hr/references/`](packages/skill-hr/references/) |
| P01–P08 提示词 | [`packages/skill-hr/references/prompts/`](packages/skill-hr/references/prompts/) |
| Claude Code / OpenClaw / Coze | [`packages/skill-hr/references/hosts/`](packages/skill-hr/references/hosts/) |
| registry / incident / hr_tasks 规范 | [`packages/skill-hr/references/06-state-and-artifacts.md`](packages/skill-hr/references/06-state-and-artifacts.md) |
| 示例 registry | [`packages/skill-hr/examples/registry.example.json`](packages/skill-hr/examples/registry.example.json)、[`registry-v2.example.json`](packages/skill-hr/examples/registry-v2.example.json) |
| registry 校验脚本 | [`packages/skill-hr/scripts/validate_registry.py`](packages/skill-hr/scripts/validate_registry.py) |
| L0–L7 测评方案 | [`packages/skill-hr/references/08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md) |
| P02 基准数据与指标 | [`packages/skill-hr/benchmarks/matching/`](packages/skill-hr/benchmarks/matching/) |
| P02 / P05 JSON Schema | [`packages/skill-hr/schemas/p02-output.schema.json`](packages/skill-hr/schemas/p02-output.schema.json)、[`p05-output.schema.json`](packages/skill-hr/schemas/p05-output.schema.json) |
| P02 基准脚本 | [`packages/skill-hr/scripts/compare_matching_benchmark.py`](packages/skill-hr/scripts/compare_matching_benchmark.py)、[`run_matching_benchmark_llm.py`](packages/skill-hr/scripts/run_matching_benchmark_llm.py) |
| CC 磁盘技能扫描 | [`packages/skill-hr/scripts/scan_claude_code_skills.py`](packages/skill-hr/scripts/scan_claude_code_skills.py) |
| Dashboard / OpenClaw 副本工作流 | [`dashboard/`](dashboard/)、[`packages/skill-hr/scripts/launch_dashboard.py`](packages/skill-hr/scripts/launch_dashboard.py)、[`openclaw-dashboard-workflow.md`](packages/skill-hr/references/hosts/openclaw-dashboard-workflow.md) |

</details>

---

<span id="cursor-agents"></span>

## Cursor 与 AGENTS

- 可选规则：[`.cursor/rules/skill-hr-always.mdc`](.cursor/rules/skill-hr-always.mdc)
- Agent 入口摘要：[`AGENTS.md`](AGENTS.md)

---

<span id="safety"></span>

## 安全

- 第三方 skill 可能恶意——安装前 **vet**；**不要运行未审阅的 `curl | sh`**。
- **「删 skill」** 默认指 registry **`terminated`**（逻辑淘汰），不是静默删目录。
- **物理卸载** 仅在 **你明确确认** 且完成路径审计之后。
- 一票否决与能力边界：[`01-competency-model.md`](packages/skill-hr/references/01-competency-model.md)

---

<span id="evaluation"></span>

## 框架测评

全栈测评计划（L0–L7：包完整性、P01–P06 主阶段、registry、安全、E2E）见 [`08-framework-evaluation.md`](packages/skill-hr/references/08-framework-evaluation.md)；员工设计 / 多技能路径另见 `09`/`10` 与 P07/P08。「只跑 P02」是其中的 **L2**；命令与黄金案例以该文档及 [`benchmarks/matching/`](packages/skill-hr/benchmarks/matching/) 为准。

---

<span id="validate-registry"></span>

## 校验 registry

```bash
python packages/skill-hr/scripts/validate_registry.py .skill-hr/registry.json
```

---

<span id="for-who"></span>

## 适合谁

如果你符合下面任意一条，这个项目很可能就是为你做的：

- 已经装了很多 skills，但越装越乱、不知如何派工的人  
- 想把 agent / skill 生态当「组织」来治理的人  
- 希望安装、试用、淘汰都有流程与留痕的人  
- 希望 meta agent 管的是「编制与绩效」而不只是闲聊的人  
- 在 **Claude Code**、**OpenClaw**、**Cursor** 等宿主里想建立 skill governance 的人  

---

<span id="faq"></span>

## 常见问题（FAQ）

**这和「多装几个插件 / skills」有什么不一样？**  
多装只增加候选；skill-hr 提供 **同一套 JD、打分、招聘、试用、台账与淘汰语义**，让宿主按流程派工而不是碰运气。

**skill-hr 会替代业务类 skill 吗？**  
不会。它负责 **选人、交接、记录与淘汰**；具体活仍由被选中的领域 skill 按其 `SKILL.md` 执行。见 [`packages/skill-hr/SKILL.md`](packages/skill-hr/SKILL.md) 开篇。

**`.skill-hr/` 要不要提交 git？**  
视团队约定：若要共享 **同一项目的技能人事台账与 incidents**，可提交；若含敏感信息，请 `.gitignore` 或脱敏后再提交。

**P01–P08 需要我手抄到对话里吗？**  
不需要。它们是 `references/prompts/` 下的 **模板**；agent 加载 skill 后按 [`SKILL.md`](packages/skill-hr/SKILL.md) 的 Mandatory flow 渐进引用即可。

**装市场 skill 要注意什么？**  
先 **vet**，拒绝来源不明脚本；细则见 [安全](#safety) 与 [`01-competency-model.md`](packages/skill-hr/references/01-competency-model.md)。

**和 `skill-creator`、`find-skills` 边界在哪？**  
`skill-creator` 偏 **创作/改版技能**；`find-skills` 偏 **发现与安装线索**；skill-hr 偏 **在岗全周期与 HRIS 式状态**。可配合使用：找到或写好 skill 后，由 skill-hr 管匹配、委派与绩效记录。

**多角色和「一个 agent 跑 skill-hr」冲突吗？**  
不冲突。多角色是 **可选部署**：多会话时用 `agents/*/SOUL.md` + `hr_dispatch.py`；单会话时仍按 [`SKILL.md`](packages/skill-hr/SKILL.md) 一条 Mandatory flow 即可。

---

<span id="license"></span>

## 许可证

MIT — [`packages/skill-hr/LICENSE`](packages/skill-hr/LICENSE)

---

若本仓库对你有用，欢迎在 [GitHub](https://github.com/thinkitpossible/skill-hr) 上 **Star** 便于后续更新；发现问题请开 **Issue**。
