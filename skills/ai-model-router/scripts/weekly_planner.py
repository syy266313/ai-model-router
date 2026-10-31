from datetime import date


def _estimate(candidate, input_tokens, output_tokens):
    pricing = candidate["pricing"]
    multiplier = pricing.get("relay_multiplier", 1.0)
    input_cost = input_tokens * pricing["input_per_million_tokens"] * multiplier / 1_000_000
    output_cost = output_tokens * pricing["output_per_million_tokens"] * multiplier / 1_000_000
    return input_cost + output_cost


def build_weekly_plan(task_data, catalog):
    task = task_data["task"] if "task" in task_data else task_data
    candidates = catalog["candidates"]
    assignments = []
    total = 0.0

    for role_task in task["roles"]:
        role = role_task["role"]
        fit = [c for c in candidates if role in c.get("role_fit_hypothesis", [])]
        if not fit:
            raise ValueError(f"No catalog candidate has a role-fit hypothesis for {role}")
        preferred = role_task.get("preferred_groups", [])
        ranked = sorted(
            fit,
            key=lambda c: (
                preferred.index(c["group"]) if c["group"] in preferred else len(preferred),
                _estimate(c, role_task["input_tokens"], role_task["expected_output_tokens"]),
            ),
        )
        chosen = ranked[0]
        cost = _estimate(chosen, role_task["input_tokens"], role_task["expected_output_tokens"])
        total += cost
        assignments.append({
            "role": role,
            "task": role_task["task"],
            "primary": {
                "model_id": chosen["model_id"],
                "relay": catalog["relay"],
                "group": chosen["group"],
                "catalog_id": chosen["id"],
                "estimated_cost_usd": round(cost, 6),
                "capabilities": chosen.get("capabilities", "unverified"),
                "relay_claim": chosen.get("relay_stability_claim"),
                "evidence": chosen.get("evidence"),
                "status": chosen.get("status"),
            },
            "fallbacks": [
                {"model_id": c["model_id"], "group": c["group"], "reason": "next role-fit candidate; access and capability remain unverified"}
                for c in ranked[1:3]
            ],
            "selection_basis": "role-fit hypothesis plus task group preference and estimated price; not benchmark-proven",
        })

    budget = task.get("budget_usd")
    warnings = []
    if budget is not None and total > budget:
        warnings.append("Estimated total exceeds the configured budget.")
    if task.get("policy", {}).get("prefer_independent_provider_for_review"):
        warnings.append("Reviewer candidates share the configured relay/provider family; independent-provider review is not available in this catalog.")
    warnings.append("Relay quality or anti-degradation statements are provider claims, not independently verified benchmark results.")
    warnings.append("Catalog visibility does not prove that the account's API keys can access each model group.")

    return {
        "project": task["project"],
        "week_start": task.get("week_start", date.today().isoformat()),
        "refreshed_at": catalog.get("observed_at"),
        "relay": catalog["relay"],
        "source_url": catalog.get("source_url"),
        "task_summary": task.get("task_summary"),
        "budget_usd": budget,
        "estimated_total_usd": round(total, 6),
        "budget_remaining_usd": round(budget - total, 6) if budget is not None else None,
        "assignments": assignments,
        "warnings": warnings,
        "approval_required": True,
    }
