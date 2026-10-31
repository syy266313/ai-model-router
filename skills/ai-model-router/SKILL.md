---
name: ai-model-router
description: Use for weekly or on-demand AI model selection, project-aware multi-model routing, relay price/capability research, and task workflow planning in OpenMinis. Trigger when the user asks which model to use, asks to continue a project, mentions WAWA or another relay, requests a weekly model refresh, or wants research/architecture/implementation/testing/review tasks split across models. Do not use as a single-model answer: generate role-based routing for the task.
---

# AI Model Router for OpenMinis

Use this skill as the planning layer for the user's projects. The user should be able to give a natural-language task such as:

> 这周继续做 poker-coach-lab 的牌局复盘功能。

Do not ask the user to manually fill researcher, architect, implementer, tester, or reviewer roles unless required information is genuinely missing. Infer the workflow from the task and project profile.

## Operating mode

Default to a weekly refresh:

1. Load the previous local snapshot from `/var/minis/workspace/ai-model-router-private/`.
2. On the first use of the week, refresh relay-visible model groups, prices, availability, and relevant official sources.
3. Compare changes with the previous snapshot.
4. Read the selected project's profile and constraints.
5. Classify the natural-language task and derive stages.
6. Assign different model roles to different stages.
7. Estimate cost and show primary/fallback candidates.
8. Ask for approval before real code changes or external side effects.
9. Reuse the approved weekly plan for normal tasks during that week.

Urgently refresh when the user asks, a model/relay fails, a material price or availability change is visible, or the task is high-risk and the snapshot is insufficient.

## Data sources and safety

Use the logged-in browser session for relay dashboards and public model plazas when available. Never read, display, copy, or save passwords, API keys, cookies, or tokens. Never open a key value just because a user asks. Use existing hidden environment variables only for a controlled API call; report status, latency, token counts, and sanitized error summaries without printing credentials.

Keep account-specific data in `/var/minis/workspace/ai-model-router-private/`. Never commit it to the public GitHub repository. Treat relay claims such as “anti-degradation” as claims, not proof. Separate:

- official documented capability
- relay claimed capability
- runtime-verified capability
- unverified hypothesis

A model group is a routing unit. Do not identify a candidate by model ID alone when the relay changes group, multiplier, stability, or access.

## Automatic task classification

Classify the task into one of:

- `code_change`: audit -> implement -> test -> review
- `audit`: audit -> review
- `research`: research -> synthesis
- `evaluation`: test -> review
- `analysis`: analysis

Increase complexity and token allowance when the task involves security, migrations, architecture, game mathematics, EV/equity, data structures, compatibility, or cross-module changes. For a simple wording/comment/format task, skip architecture and review unless risk says otherwise.

Map stages to roles:

- audit/analysis/synthesis -> architect
- research -> researcher
- implement -> implementer
- test -> tester
- review -> reviewer

## Project profiles

Prefer a private project profile when available. For `poker-coach-lab`, always inject:

- read `agents.md` before each task
- audit and propose before editing; wait for user approval
- do not modify `js/gameEngine.js` unless explicitly requested
- do not modify `js/bot.js` unless bot tuning is requested
- keep one scoped change per task
- preserve iOS 13 Safari compatibility
- run `deno check` and relevant tests after changes

Never modify a project merely because the router generated a plan. A plan is not approval.

## Candidate selection

Choose candidates by this order:

1. Required role fit and hard project constraints.
2. Current weekly snapshot and verified availability.
3. Runtime-verified capability for high-risk work.
4. Quality/reliability evidence and recent failures.
5. User's configured group preference.
6. Cost and latency.

If no runtime evidence exists, say so. Use relay group preference as a provisional routing policy, not as a factual quality ranking. Always output a fallback and explain why it is next.

For each assignment report:

- stage and role
- relay, group, model ID
- primary and fallback
- reason
- estimated input/output tokens and cost
- evidence source and checked time
- access/capability verification status
- risks and approval requirement

## Execution boundary

This skill plans and coordinates. It does not replace a gateway. Use LiteLLM, WAWA's OpenAI-compatible endpoint, or another configured executor for actual calls, retries, cooldowns, fallback, rate limits, and telemetry. Do not build a second gateway inside the skill.

## Output format

```text
本周模型路由方案
项目：
任务：
快照时间：
任务分类：
执行阶段：

阶段 1：
- 角色：
- 主模型：
- 中转分组：
- 备用模型：
- 预计成本：
- 选择依据：

风险与未知项：
总成本估算：
需要人工确认：
```

For code tasks, stop after the plan and wait for approval before editing. For read-only research or analysis, proceed and cite sources.
