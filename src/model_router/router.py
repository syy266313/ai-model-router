from dataclasses import dataclass
from .cost import Pricing

@dataclass(frozen=True)
class Candidate:
    model_id: str
    capabilities: frozenset[str]
    pricing: Pricing
    status: str = "active"

@dataclass(frozen=True)
class Route:
    model_id: str
    estimated_cost_usd: float
    reason: str

def route(candidates, required, input_tokens, output_tokens, max_cost=None):
    required = set(required)
    eligible = []
    for candidate in candidates:
        if candidate.status != "active" or not required.issubset(candidate.capabilities):
            continue
        cost = candidate.pricing.estimate(input_tokens, output_tokens)
        if max_cost is None or cost <= max_cost:
            eligible.append((cost, candidate))
    if not eligible:
        raise ValueError("No eligible model satisfies the requested capabilities and budget")
    cost, candidate = sorted(eligible, key=lambda item: item[0])[0]
    return Route(candidate.model_id, cost, "lowest estimated cost among eligible candidates")
