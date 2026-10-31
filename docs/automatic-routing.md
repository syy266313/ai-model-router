# Automatic Routing

The planner is the project-aware layer above an execution gateway. The user provides a project and a natural-language task; the planner derives a workflow and assigns model roles.

## Input

```text
project profile + weekly relay snapshot + natural-language task + optional budget
```

The user does not need to manually provide `researcher`, `architect`, `implementer`, or `reviewer` roles.

## Decision flow

```text
task text
  -> classify category and complexity
  -> derive stages
  -> inject project hard constraints
  -> map stages to roles
  -> filter role-fit candidates
  -> prefer configured relay groups
  -> estimate token cost
  -> return primary and fallback candidates
  -> require approval before execution
```

Current task categories:

- `code_change`: audit, implement, test, review
- `audit`: audit, review
- `research`: research, synthesis
- `evaluation`: test, review
- `analysis`: analysis

High-risk words such as security, migration, architecture, probability, EV, data structures, and compatibility constraints increase the token allowance and keep a stronger review stage.

## Important boundary

The planner does not make unsupported capability claims. A catalog candidate can be selected because its relay group and role-fit hypothesis match the policy, while `capabilities_status` remains `unverified`. Relay statements such as “anti-degradation” are recorded as claims, not quality evidence.

The planner is not an execution gateway. LiteLLM, WAWA, or another OpenAI-compatible client should handle actual requests, retries, cooldowns, fallbacks, rate limits, and usage telemetry.

## Example

```bash
PYTHONPATH=src python3 -m model_router.cli recommend \
  config/poker-coach-lab.example.json \
  /path/to/private/wawa-model-catalog.json \
  --task "这周继续开发牌局复盘筛选功能，先审计方案，再实现、测试和最终复核" \
  --budget 1.0
```

Private catalog paths and account information must remain outside the public repository.
