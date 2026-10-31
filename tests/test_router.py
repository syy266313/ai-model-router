import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from model_router.cost import Pricing
from model_router.router import Candidate, route
from model_router.auto_router import classify, recommend


class RouterTests(unittest.TestCase):
    def test_cost_includes_relay_multiplier(self):
        pricing = Pricing(1.0, 5.0, 2.0)
        self.assertEqual(pricing.estimate(1000, 1000), 0.012)

    def test_route_selects_cheapest_eligible_model(self):
        candidates = [
            Candidate("slow", frozenset({"coding"}), Pricing(2, 8)),
            Candidate("cheap", frozenset({"coding"}), Pricing(1, 3)),
            Candidate("wrong", frozenset({"vision"}), Pricing(0, 0)),
        ]
        result = route(candidates, ["coding"], 1000, 1000)
        self.assertEqual(result.model_id, "cheap")

    def test_route_respects_budget(self):
        candidates = [Candidate("too-expensive", frozenset({"coding"}), Pricing(100, 100))]
        with self.assertRaisesRegex(ValueError, "No eligible"):
            route(candidates, ["coding"], 1000, 1000, max_cost=0.01)


if __name__ == "__main__":
    unittest.main()
