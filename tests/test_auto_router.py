import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from model_router.auto_router import classify, recommend


CATALOG = {
    "relay": "test-relay",
    "observed_at": "2026-01-01",
    "candidates": [
        {
            "model_id": "strong",
            "group": "pro",
            "role_fit_hypothesis": ["architect", "reviewer"],
            "input_per_million_tokens": 2,
            "output_per_million_tokens": 10,
            "multiplier": 0.5,
            "capabilities": "unverified",
            "status": "observed_not_key_verified",
        },
        {
            "model_id": "cheap",
            "group": "stable",
            "role_fit_hypothesis": ["implementer", "tester"],
            "input_per_million_tokens": 1,
            "output_per_million_tokens": 5,
            "multiplier": 0.1,
            "capabilities": "unverified",
            "status": "observed_not_key_verified",
        },
    ],
}
PROJECT = {
    "name": "poker",
    "stack": "javascript",
    "compatibility_targets": ["ios13_safari"],
    "hard_constraints": ["do not change game engine"],
}


class AutoRouterTests(unittest.TestCase):
    def test_feature_task_generates_workflow(self):
        decision = classify("新增一个牌局筛选功能", PROJECT)
        self.assertEqual(decision["category"], "code_change")
        self.assertEqual(decision["stages"], ["audit", "implement", "test", "review"])
        self.assertIn("Preserve iOS 13 Safari compatibility.", decision["hard_constraints"])

    def test_audit_task_does_not_schedule_implementation(self):
        decision = classify("审计牌局导出逻辑", PROJECT)
        self.assertEqual(decision["category"], "audit")
        self.assertEqual(decision["stages"], ["audit", "review"])

    def test_recommendation_uses_multiplier_and_warns_about_unverified_access(self):
        result = recommend("新增一个牌局筛选功能", PROJECT, CATALOG, budget_usd=1)
        self.assertEqual(result["assignments"][0]["model_id"], "strong")
        self.assertEqual(result["assignments"][1]["model_id"], "cheap")
        self.assertGreater(result["estimated_total_usd"], 0)
        self.assertTrue(any("API-key access" in warning for warning in result["warnings"]))


if __name__ == "__main__":
    unittest.main()
