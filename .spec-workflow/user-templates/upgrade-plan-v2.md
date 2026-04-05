# Skill-HR v2 综合升级计划

> 参照 [edict](https://github.com/cft0808/edict) 三省六部制看板，将 skill-hr 从纯 Markdown + Python CLI 元技能升级为 **带可视化前端 + 多技能 Agent 模型 + 员工训练 Agent** 的完整 HR 平台。

---

## 一、概念映射：edict → skill-hr

| edict 概念 | skill-hr 对应 | 页面名称 | 说明 |
|------------|--------------|---------|------|
| 旨意看板 (Kanban) | **业务看板** | Task Dashboard | 新发起的 HR 任务（Intake→InProgress），按状态列展示 |
| 省部调度 (Monitor) | **员工看板** | Agent Dashboard | 现有 8 个 HR Agent 的实时状态、负载、健康度 |
| 任务流转详情 | **任务工作流** | Task Workflow | 单个 HR 任务的完整 P01→P06 阶段时间线 |
| 官员总览 (Officials) | **员工总览** | Employee Overview | Agent 员工数据库：技能清单、绩效统计、KPI |
| 奏折阁 (Memorials) | **任务归档** | Task Archive | 已完成/已终止任务的 incident 归档与回溯 |
| 旨库 (Templates) | **业务模板** | Business Templates | 常用员工功能模板 + 关联关键词，一键发起任务 |

---

## 二、核心升级要点

### 2.1 多技能 Agent 模型（从 single-skill 到 multi-skill）

**当前问题**：`registry.json` 中每个 `skills[]` 项代表一个 skill，但没有建模"一个 Agent 可以拥有多个 skill"的概念。skill-hr 招聘的是 skill，而非完整的 Agent。

**升级方向**：

```
当前模型:
  registry.skills[] → 每条是独立 skill（pdf, xlsx, security-auditor...）
  
升级后模型:
  registry.agents[] → 每条是一个 Agent（可含 1~N 个 skills）
  registry.skills[] → 保留作为 skill 字典（去重、元数据）
  
  Agent = {
    id, name, status, 
    skills: ["pdf", "xlsx", "docx"],   // 多技能
    primary_skill: "pdf",               // 主技能
    host: "claude-code" | "lobechat",   // 运行宿主
    performance: { tasks_total, tasks_success, tasks_fail },
    training_history: [...],            // 训练记录
    created_by: "recruited" | "trained" // 来源：招聘还是训练
  }
```

**影响范围**：
- `registry.json` schema 扩展（向下兼容，保留 `skills[]`，新增 `agents[]`）
- P02 匹配逻辑升级：从"匹配 skill"到"匹配 Agent 的 skill 组合"
- P03 委派升级：handoff 包需指定 Agent + 要调用的 skills 子集
- 前端展示：Employee Overview 需展示 Agent 的多技能视图

### 2.2 员工训练 Agent（Training Designer）

**新增 Agent**：`trainer` — 负责设计、训练和调优 Agent 员工。

| 能力 | 描述 |
|------|------|
| **Skill 组合设计** | 根据 JD 需求，设计 Agent 应装载的 skill 组合 |
| **SOUL.md 生成** | 根据角色定位，自动生成/更新 Agent 的人格模板 |
| **Prompt 调优** | 基于 P05 复盘数据，优化 Agent 的 prompt/configuration |
| **训练计划** | 制定新 Agent 的 onboarding 训练计划和考核标准 |
| **技能补充建议** | 分析 Agent 绩效短板，建议补充哪些 skill |

**训练流程**：
```
需求 → trainer 分析 JD → 设计 Agent profile → 
选择/安装 skills → 编写 SOUL.md → 冒烟测试 → 
probation 观察 → 正式上岗 / 返回调优
```

**文件位置**：
- `packages/skill-hr/agents/trainer/SOUL.md` — 训练师人格
- `packages/skill-hr/references/09-training-and-design.md` — 训练规范
- `packages/skill-hr/references/prompts/P07-design-agent.md` — 设计 Agent 提示词
- `packages/skill-hr/references/prompts/P08-training-plan.md` — 训练计划提示词

### 2.3 宿主兼容：Claude Code + Lobechat

**当前支持**：Claude Code、OpenClaw、Cursor（被动规则）

**新增支持**：Lobechat（用户提到的 "Lobster"）

| 宿主 | 技能发现 | Agent 运行 | 看板 |
|------|---------|-----------|------|
| Claude Code | 磁盘扫描 `.claude/skills/` | 单会话 / sub-agent | 独立 Web 服务 |
| Lobechat | Plugin 注册 / 本地 skill | 多 Agent 会话 | 嵌入式 / 独立 Web |
| Cursor | 项目规则 `.cursor/rules/` | Agent mode | 独立 Web 服务 |

**新增文件**：`packages/skill-hr/references/hosts/lobechat.md`

---

## 三、前端技术方案

### 3.1 技术栈选型

参考 edict 的方案（React 18 + TypeScript + Vite + Zustand），skill-hr 采用：

| 层 | 选型 | 理由 |
|----|------|------|
| 框架 | **React 18** + TypeScript | 与 edict 一致，生态成熟 |
| 构建 | **Vite** | 快速 HMR，edict 已验证 |
| 状态 | **Zustand** | 轻量，无 boilerplate |
| UI 库 | **Tailwind CSS** + **shadcn/ui** | 现代、可定制、组件丰富 |
| 图表 | **Recharts** | 轻量级 React 图表 |
| HTTP | **fetch** + **SWR** | 自动缓存与刷新 |
| 路由 | **React Router v6** | 标准 SPA 路由 |

### 3.2 后端 API 服务

参考 edict 的 `server.py`（纯 stdlib 零依赖），skill-hr 采用：

| 组件 | 选型 | 说明 |
|------|------|------|
| API Server | **Python** `http.server` 或 **FastAPI**（可选） | 读写 `.skill-hr/` JSON 文件 |
| 数据源 | `.skill-hr/registry.json` + `hr_tasks.json` + `incidents/` | 已有状态文件 |
| 实时刷新 | **轮询**（15s）+ 可选 SSE | 前端定时 fetch |
| 认证 | 可选 token/basic auth | 本地开发可关闭 |

### 3.3 页面设计详情

#### 页面 1：业务看板（Task Dashboard）

对应 edict 旨意看板。展示 `hr_tasks.json` 中所有活跃任务。

**布局**：
- 顶部：任务统计摘要（按状态计数）+ 搜索/过滤
- 主体：Kanban 列（Intake → JDReady → Matching → Matched → Recruiting → Vetting → Delegated → InProgress → Debrief）
- 卡片内容：任务 ID、标题、当前 Agent、创建时间、心跳状态
- 操作：点击查看详情、状态流转操作

**数据源**：`GET /api/tasks` → 读取 `.skill-hr/hr_tasks.json`

#### 页面 2：员工看板（Agent Dashboard）

对应 edict 省部调度。展示 8 个 HR Agent 的状态。

**布局**：
- 顶部：Agent 状态摘要（活跃/空闲/忙碌/异常）
- 主体：Agent 卡片网格，每张卡片显示：
  - Agent 名称 + 角色图标
  - 当前正在处理的任务
  - 技能标签列表（多技能展示）
  - 绩效迷你图（成功/失败/总量）
  - 健康心跳徽章
- 侧边：部门分布图（条形图）

**数据源**：`GET /api/agents` → 读取 `agents/` 目录 + `registry.json` agents 段

#### 页面 3：任务工作流（Task Workflow Detail）

对应 edict 任务流转详情。

**布局**：
- 顶部：任务基本信息（ID、标题、状态、创建时间）
- 主体：
  - **阶段时间线**（垂直）：P01 Intake → P02 Matching → P03 Handoff → P04 Recruit → P05 Debrief → P06 Terminate
  - 每个阶段节点展示：执行 Agent、时间戳、备注、引用的 reference 文件
  - **flow_log** 可视化：Agent 间流转箭头图
  - **progress_log** 列表：工作进度快照
- 底部：关联 incident 文件列表（可点击查看）

**数据源**：`GET /api/tasks/:id` → 单个任务详情 + incident 关联

#### 页面 4：员工总览（Employee Overview）

对应 edict 官员总览。skill-hr 的"员工数据库"。

**布局**：
- 顶部：搜索 + 按状态/技能筛选
- 主体：表格视图
  - 列：ID、名称、状态、技能列表（多标签）、任务总数、成功率、最近使用、来源、宿主
  - 可排序、可分页
- 详情抽屉：点击行展示完整 Agent 信息
  - 技能详情（每个 skill 的绩效）
  - 训练历史时间线
  - 关联 incident 列表
  - 操作：probation、terminate、freeze、retrain

**数据源**：`GET /api/employees` → 读取 `registry.json` agents[] + skills[]

#### 页面 5：任务归档（Task Archive）

对应 edict 奏折阁。

**布局**：
- 顶部：按状态筛选（Closed / Terminated）+ 时间范围 + 搜索
- 主体：归档卡片列表
  - 每张卡片：任务标题、完成时间、执行 Agent、outcome、阶段时间线缩略图
- 详情面板：
  - 完整 incident markdown 渲染
  - 五阶段时间线：Intake → Match → Delegate → Execute → Debrief
  - 一键复制 Markdown
  - 绩效评分与复盘要点

**数据源**：`GET /api/archives` → 读取状态为 Closed/Terminated 的任务 + `.skill-hr/incidents/`

#### 页面 6：业务模板（Business Templates）

对应 edict 旨库。

**布局**：
- 顶部：分类筛选标签（代码审查、文档生成、安全审计、数据分析…）
- 主体：模板卡片网格
  - 每张卡片：模板名称、描述、推荐 Agent、预估复杂度、关联关键词标签
  - 点击展开：参数表单（可编辑的 JD 字段预填）
- 操作：填好参数 → 一键发起 HR 任务（自动创建 hr_task + 走 P01）

**模板数据源**：`templates.json` 预设模板文件（新建）

---

## 四、升级后项目结构

```
skill-hr/
├── AGENTS.md
├── README.md
├── README.en.md
├── packages/
│   └── skill-hr/
│       ├── SKILL.md                          # 更新：增加 trainer Agent、多技能说明
│       ├── agents/
│       │   ├── GLOBAL.md                     # 更新：增加 trainer 到权限矩阵
│       │   ├── trainer/SOUL.md               # 🆕 训练设计师 Agent
│       │   ├── hr-director/SOUL.md
│       │   ├── job-analyst/SOUL.md
│       │   ├── talent-assessor/SOUL.md
│       │   ├── recruiter/SOUL.md
│       │   ├── compliance/SOUL.md
│       │   ├── onboarder/SOUL.md
│       │   ├── perf-manager/SOUL.md
│       │   └── hris-admin/SOUL.md
│       ├── references/
│       │   ├── 00–08 (现有)
│       │   ├── 09-training-and-design.md     # 🆕 训练规范
│       │   ├── 10-multi-skill-agent.md       # 🆕 多技能 Agent 规范
│       │   ├── hosts/
│       │   │   ├── claude-code.md
│       │   │   ├── openclaw.md
│       │   │   └── lobechat.md               # 🆕 Lobechat 宿主说明
│       │   └── prompts/
│       │       ├── P01–P06 (现有)
│       │       ├── P07-design-agent.md       # 🆕 设计 Agent 提示词
│       │       └── P08-training-plan.md      # 🆕 训练计划提示词
│       ├── schemas/
│       │   ├── p02-output.schema.json
│       │   ├── registry-v2.schema.json       # 🆕 v2 registry schema（含 agents[]）
│       │   └── templates.schema.json         # 🆕 模板 schema
│       ├── scripts/
│       │   ├── hr_dispatch.py                # 更新：支持 trainer 角色
│       │   ├── server.py                     # 🆕 API 服务器
│       │   ├── validate_registry.py          # 更新：支持 v2 schema
│       │   └── ... (现有)
│       ├── examples/
│       │   ├── registry-v2.example.json      # 🆕
│       │   └── ... (现有)
│       └── templates/
│           └── templates.json                # 🆕 业务模板预设数据
├── dashboard/                                # 🆕 前端看板
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── router.tsx                        # React Router 配置
│   │   ├── stores/                           # Zustand 状态管理
│   │   │   ├── taskStore.ts
│   │   │   ├── agentStore.ts
│   │   │   └── employeeStore.ts
│   │   ├── api/                              # API 调用层
│   │   │   ├── client.ts
│   │   │   ├── tasks.ts
│   │   │   ├── agents.ts
│   │   │   └── employees.ts
│   │   ├── pages/                            # 6 大页面
│   │   │   ├── TaskDashboard.tsx             # 业务看板
│   │   │   ├── AgentDashboard.tsx            # 员工看板
│   │   │   ├── TaskWorkflow.tsx              # 任务工作流详情
│   │   │   ├── EmployeeOverview.tsx          # 员工总览
│   │   │   ├── TaskArchive.tsx               # 任务归档
│   │   │   └── BusinessTemplates.tsx         # 业务模板
│   │   ├── components/                       # 共享组件
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   ├── task/
│   │   │   │   ├── TaskCard.tsx
│   │   │   │   ├── KanbanColumn.tsx
│   │   │   │   └── TaskTimeline.tsx
│   │   │   ├── agent/
│   │   │   │   ├── AgentCard.tsx
│   │   │   │   ├── HealthBadge.tsx
│   │   │   │   └── SkillTagList.tsx
│   │   │   ├── employee/
│   │   │   │   ├── EmployeeTable.tsx
│   │   │   │   ├── EmployeeDetail.tsx
│   │   │   │   └── TrainingHistory.tsx
│   │   │   └── common/
│   │   │       ├── StatusBadge.tsx
│   │   │       ├── SearchFilter.tsx
│   │   │       └── StatsCard.tsx
│   │   ├── types/                            # TypeScript 类型定义
│   │   │   ├── task.ts
│   │   │   ├── agent.ts
│   │   │   ├── employee.ts
│   │   │   └── template.ts
│   │   └── styles/
│   │       └── globals.css                   # Tailwind 入口
│   └── public/
│       └── favicon.svg
└── .skill-hr/                                # 运行时产物（不提交）
    ├── registry.json                         # v2: 含 agents[] + skills[]
    ├── hr_tasks.json
    └── incidents/
```

---

## 五、分阶段任务拆解

### Phase 0：基础设施（先决条件）

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 0.1 | 初始化 dashboard 前端项目 | `dashboard/` + Vite + React + TS + Tailwind + shadcn/ui | 无 |
| 0.2 | 设计 registry v2 schema | `schemas/registry-v2.schema.json` | 无 |
| 0.3 | 编写 API server | `scripts/server.py` — 读取 `.skill-hr/` JSON 提供 REST API | 0.2 |
| 0.4 | 创建 templates.json 预设数据 | `templates/templates.json` — 8-10 个常用模板 | 无 |

### Phase 1：前端六大页面

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 1.1 | 通用布局 + 路由 + 侧边栏 | `MainLayout`, `Sidebar`, `Header`, `router.tsx` | 0.1 |
| 1.2 | 业务看板（Task Dashboard） | Kanban 页面 + `TaskCard` + `KanbanColumn` | 1.1, 0.3 |
| 1.3 | 员工看板（Agent Dashboard） | Agent 卡片网格 + 状态统计 + 部门分布图 | 1.1, 0.3 |
| 1.4 | 任务工作流（Task Workflow） | 阶段时间线 + flow_log 可视化 | 1.2 |
| 1.5 | 员工总览（Employee Overview） | 表格 + 详情抽屉 + 多技能标签 | 1.1, 0.3 |
| 1.6 | 任务归档（Task Archive） | 归档卡片列表 + incident 渲染 + markdown 复制 | 1.1, 0.3 |
| 1.7 | 业务模板（Business Templates） | 模板卡片 + 参数表单 + 一键发起任务 | 1.1, 0.3, 0.4 |

### Phase 2：多技能 Agent 模型升级

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 2.1 | 编写 `10-multi-skill-agent.md` 规范 | 多技能 Agent 的数据模型、匹配规则、委派规则 | 无 |
| 2.2 | 升级 registry schema 与迁移脚本 | v1→v2 兼容迁移 + 校验 | 0.2 |
| 2.3 | 升级 P02 匹配逻辑 | 支持 Agent 级匹配（含 skill 组合评分） | 2.1 |
| 2.4 | 升级 P03 委派 handoff | 指定 Agent + skills 子集 | 2.1 |
| 2.5 | 更新 `registry.example.json` | 包含多技能 Agent 示例 | 2.2 |

### Phase 3：训练设计师 Agent

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 3.1 | 编写 `09-training-and-design.md` | 训练规范文档 | 2.1 |
| 3.2 | 创建 `agents/trainer/SOUL.md` | 训练师人格模板 | 3.1 |
| 3.3 | 编写 P07 设计 Agent 提示词 | `prompts/P07-design-agent.md` | 3.1 |
| 3.4 | 编写 P08 训练计划提示词 | `prompts/P08-training-plan.md` | 3.1 |
| 3.5 | 更新 `GLOBAL.md` 权限矩阵 | 加入 trainer 的权限行 | 3.2 |
| 3.6 | 更新 `hr_dispatch.py` | 新增 Training/Trained 状态 | 3.1 |
| 3.7 | 更新 `SKILL.md` | 增加 trainer Agent 说明 + 训练流程 | 3.2, 3.5 |

### Phase 4：宿主扩展 + Lobechat 支持

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 4.1 | 编写 `hosts/lobechat.md` | Lobechat 宿主安装/配置说明 | 无 |
| 4.2 | 适配 scan 脚本 | 扫描 Lobechat 的 skill/plugin 目录 | 4.1 |
| 4.3 | 更新 `SKILL.md` 宿主段落 | 加入 Lobechat 说明 | 4.1 |

### Phase 5：集成与测试

| # | 任务 | 产出 | 依赖 |
|---|------|------|------|
| 5.1 | 端到端流程测试 | 从模板发起 → 看板可见 → 匹配 → 委派 → 归档 | 全部 |
| 5.2 | 前端构建 + 部署脚本 | `start.sh` 一键启动 dashboard + API server | 1.x, 0.3 |
| 5.3 | 更新 README.md | 反映 v2 能力、截图、启动方式 | 全部 |
| 5.4 | 生成 demo 数据 + 截图 | `.skill-hr/` 示例数据 + `docs/demo/` 截图 | 全部 |

---

## 六、API 设计

### 任务 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks` | 所有任务列表（支持 `?state=` 过滤） |
| GET | `/api/tasks/:id` | 单个任务详情（含 flow_log、progress_log） |
| POST | `/api/tasks` | 创建新任务（调用 hr_dispatch.py create） |
| PATCH | `/api/tasks/:id/state` | 变更状态（调用 hr_dispatch.py state） |
| GET | `/api/archives` | 已归档任务（Closed + Terminated） |

### Agent/员工 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/agents` | HR 部门 Agent 列表（从 agents/ 读取） |
| GET | `/api/employees` | 注册员工列表（registry.json agents[]） |
| GET | `/api/employees/:id` | 员工详情（含 skills、绩效、训练记录） |
| PATCH | `/api/employees/:id/status` | 更新员工状态 |

### 模板 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/templates` | 全部业务模板 |
| POST | `/api/templates/:id/execute` | 用模板发起任务 |

### 系统 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/incidents` | incident 文件列表 |
| GET | `/api/incidents/:filename` | 单个 incident 内容 |
| GET | `/api/stats` | 汇总统计（任务数、Agent 数、成功率…） |

---

## 七、registry v2 schema 设计

```json
{
  "skill_hr_version": "2.0.0",
  "updated_at": "2026-04-05T12:00:00Z",
  "hosts": ["claude-code", "cursor", "lobechat"],
  "matching": {
    "delegate_min_score": 75,
    "confirm_band_min": 60,
    "max_trials_per_task_per_skill": 2
  },
  "skills": [
    {
      "id": "pdf",
      "name": "pdf",
      "install_path": "~/.claude/skills/pdf/SKILL.md",
      "description": "PDF manipulation toolkit",
      "keywords": ["pdf", "extract", "merge", "split", "forms"],
      "added_at": "2026-04-01T10:00:00Z"
    }
  ],
  "agents": [
    {
      "id": "doc-specialist-01",
      "name": "Document Specialist",
      "skills": ["pdf", "docx", "xlsx"],
      "primary_skill": "pdf",
      "status": "active",
      "host": "claude-code",
      "created_by": "trained",
      "added_at": "2026-04-01T10:00:00Z",
      "last_used_at": "2026-04-03T09:15:00Z",
      "performance": {
        "tasks_total": 12,
        "tasks_success": 11,
        "tasks_fail": 1
      },
      "training_history": [
        {
          "ts": "2026-04-01T10:00:00Z",
          "action": "created",
          "trainer_notes": "Designed for document processing pipeline"
        },
        {
          "ts": "2026-04-02T14:00:00Z",
          "action": "skill_added",
          "skill_id": "xlsx",
          "trainer_notes": "Added spreadsheet capability after JD analysis"
        }
      ],
      "notes": "Reliable for document processing; weak on scanned PDFs"
    }
  ]
}
```

---

## 八、hr_tasks.json 状态机扩展

在现有 12 个状态基础上，增加训练相关状态：

| 新状态 | 含义 |
|--------|------|
| `Designing` | trainer 正在设计 Agent profile |
| `Training` | Agent 正在接受训练（skill 安装 + SOUL 编写 + 冒烟测试） |
| `TrainingReview` | 训练成果审核 |

状态流转扩展：
```
Intake → Designing → Training → TrainingReview → Matched → Delegated → ...
                                     ↓
                               返回 Designing（不合格）
```

---

## 九、优先级与里程碑

| 里程碑 | 内容 | 预估 |
|--------|------|------|
| **M0** | 项目骨架（dashboard init + API server + registry v2 schema） | 1-2 天 |
| **M1** | 前端 6 页面基本可用（含 mock 数据） | 3-5 天 |
| **M2** | API 对接真实 `.skill-hr/` 数据 + 多技能模型落地 | 2-3 天 |
| **M3** | trainer Agent + P07/P08 + 训练流程 | 2-3 天 |
| **M4** | Lobechat 宿主支持 + 集成测试 + Demo 数据 | 1-2 天 |
| **M5** | 文档更新 + README + 截图 + 一键启动脚本 | 1 天 |

**总计预估**：10-16 天（并行可压缩到 7-10 天）

---

## 十、风险与决策点

| 风险/决策 | 说明 | 建议 |
|-----------|------|------|
| **registry v1→v2 兼容** | 现有 registry 只有 skills[]，v2 加 agents[] | 向下兼容：v2 读到 v1 时自动将每个 skill 包装为单 skill Agent |
| **单文件 vs 多文件后端** | edict 用一个 2300 行 server.py | 建议用模块化 Python（FastAPI 或多文件 stdlib），便于维护 |
| **前端独立 vs 嵌入** | 独立 Web 服务 vs 嵌入到宿主 | 独立服务最灵活，各宿主均可用 |
| **Lobechat API 差异** | Lobechat 的 skill/plugin 机制与 Claude Code 不同 | 需要调研 Lobechat 的确切插件注册方式 |
| **训练 Agent 权限** | trainer 能 install skill + 写 SOUL.md | 需 compliance 审核，加入 GLOBAL.md 权限矩阵 |

---

## 十一、下一步行动

完成本计划后，按以下顺序开工：

1. **确认**：请确认此计划是否满足需求，是否有调整
2. **Phase 0**：初始化前端项目 + registry v2 schema + API server
3. **Phase 1**：逐页开发前端
4. **Phase 2-3**：并行推进多技能模型 + trainer Agent
5. **Phase 4-5**：宿主扩展 + 集成测试 + 文档

> 计划文件位置：`.spec-workflow/user-templates/upgrade-plan-v2.md`
