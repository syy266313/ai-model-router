from datetime import date


def _contains(text, terms):
    return any(term in text for term in terms)


def classify(task_text, project=None):
    text = task_text.lower()
    project = project or {}
    code_change = _contains(text, ("fix", "bug", "implement", "add ", "change", "refactor", "修复", "实现", "新增", "修改", "重构", "开发"))
    research = _contains(text, ("research", "search", "latest", "compare", "pricing", "docs", "调研", "搜索", "最新", "比较", "价格", "文档", "联网"))
    explicit_test = _contains(text, ("test", "benchmark", "evaluate", "测试", "评测", "验收"))
    audit_only = _contains(text, ("audit", "review", "inspect", "审计", "审查", "检查")) and not code_change
    high_risk = _contains(text, ("security", "migration", "architecture", "gameengine", "bot.js", "probability", "equity", "安全", "迁移", "架构", "胜率", "赔率", "数据结构")) or " ev " in f" {text} "
    simple = _contains(text, ("typo", "format", "comment", "文案", "注释", "拼写", "格式")) and not high_risk
    if code_change:
        category = "code_change"
        complexity = "high" if high_risk or _contains(text, ("cross-file", "multiple", "跨文件", "多模块")) else "normal"
        stages = ["audit", "implement", "test", "review"]
        if research:
            stages.insert(1, "research")
        if simple:
            stages = ["implement", "test"]
    elif audit_only:
        category, complexity, stages = "audit", "high" if high_risk else "normal", ["audit", "review"]
    elif research:
        category, complexity, stages = "research", "normal", ["research", "synthesis"]
    elif explicit_test:
        category, complexity, stages = "evaluation", "normal", ["test", "review"]
    else:
        category, complexity, stages = "analysis", "normal", ["analysis"]
    hard_constraints = list(project.get("hard_constraints", []))
    if project.get("stack") == "javascript" and "ios13_safari" in project.get("compatibility_targets", []):
        hard_constraints.append("Preserve iOS 13 Safari compatibility.")
    return {"category": category, "complexity": complexity, "stages": stages, "high_risk": high_risk, "hard_constraints": list(dict.fromkeys(hard_constraints))}


def _price(candidate, input_tokens, output_tokens):
    pricing = candidate.get("pricing", candidate)
    multiplier = pricing.get("relay_multiplier", pricing.get("multiplier", 1.0))
    return (input_tokens * pricing["input_per_million_tokens"] + output_tokens * pricing["output_per_million_tokens"]) * multiplier / 1_000_000


def _stage_budget(stage, complexity):
    defaults = {
        "audit": (8000, 3000), "research": (7000, 3000), "synthesis": (6000, 2500),
        "implement": (12000, 6000), "test": (5000, 4000), "review": (8000, 3000), "analysis": (6000, 2500),
    }
    input_tokens, output_tokens = defaults[stage]
    if complexity == "high":
        input_tokens = int(input_tokens * 1.5)
        output_tokens = int(output_tokens * 1.4)
    return input_tokens, output_tokens


def recommend(task_text, project, catalog, budget_usd=None):
    decision = classify(task_text, project)
    candidates = catalog["candidates"]
    assignments = []
    total = 0.0
    for stage in decision["stages"]:
        role = {"audit": "architect", "implement": "implementer", "test": "tester", "review": "reviewer", "research": "researcher", "synthesis": "architect", "analysis": "architect"}[stage]
        fit = [c for c in candidates if role in c.get("role_fit_hypothesis", [])]
        if not fit:
            assignments.append({"stage": stage, "role": role, "status": "no_candidate", "reason": "No configured candidate for this role."})
            continue
        preferred_groups = {
            "architect": ["gpt-pro-兜底分组", "gpt-max-不降智版"],
            "reviewer": ["gpt-pro-兜底分组", "gpt-max-不降智版"],
            "implementer": ["gpt-plus-稳定分组", "gpt-pro-兜底分组"],
            "tester": ["gpt-plus-稳定分组", "gpt-pro-兜底分组"],
            "researcher": ["gpt-plus-稳定分组", "gpt-pro-兜底分组"],
        }.get(role, [])
        ranked = sorted(fit, key=lambda c: (preferred_groups.index(c["group"]) if c["group"] in preferred_groups else len(preferred_groups), _price(c, *_stage_budget(stage, decision["complexity"]))))
        primary = ranked[0]
        in_tokens, out_tokens = _stage_budget(stage, decision["complexity"])
        estimated = _price(primary, in_tokens, out_tokens)
        total += estimated
        assignments.append({
            "stage": stage,
            "role": role,
            "model_id": primary["model_id"],
            "relay": catalog["relay"],
            "group": primary["group"],
            "estimated_input_tokens": in_tokens,
            "estimated_output_tokens": out_tokens,
            "estimated_cost_usd": round(estimated, 6),
            "fallbacks": [{"model_id": c["model_id"], "group": c["group"]} for c in ranked[1:3]],
            "capabilities_status": primary.get("capabilities", "unverified"),
            "relay_quality_claim": primary.get("relay_stability_claim"),
            "rationale": f"Automatic rule for {role}: apply project constraints, then prefer the configured quality/cost group order.",
            "evidence": primary.get("evidence"),
            "access_status": primary.get("status"),
        })
    warnings = [
        "This is a recommendation plan; no model API calls were made.",
        "Relay model quality and anti-degradation statements are unverified vendor claims.",
        "The browser showed model groups, but API-key access to each group has not been verified.",
        "Cost is a token-volume estimate; cached-token, tool, image, audio, retries, and relay-specific fees are excluded.",
    ]
    if project.get("hard_constraints"):
        warnings.append("Project hard constraints must be included in each execution prompt: " + "; ".join(project["hard_constraints"]))
    if budget_usd is not None and total > budget_usd:
        warnings.append("Estimated cost exceeds the provided budget.")
    return {
        "project": project.get("name", "unspecified"),
        "project_constraints": decision["hard_constraints"],
        "task": task_text,
        "classification": decision,
        "weekly_snapshot_date": catalog.get("observed_at"),
        "source_url": catalog.get("source_url"),
        "estimated_total_usd": round(total, 6),
        "budget_usd": budget_usd,
        "assignments": assignments,
        "warnings": warnings,
        "approval_required": True,
    }
