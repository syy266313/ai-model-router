import argparse
import json
from pathlib import Path
from .cost import Pricing
from .router import Candidate, route
from .planner import build_weekly_plan
from .auto_router import recommend

def load_json(path):
    return json.loads(Path(path).read_text())

def main(argv=None):
    parser = argparse.ArgumentParser(prog="model-router")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("path")
    estimate = sub.add_parser("estimate")
    estimate.add_argument("path")
    plan = sub.add_parser("plan")
    plan.add_argument("task_path")
    plan.add_argument("catalog_path")
    plan.add_argument("--output")
    auto = sub.add_parser("recommend")
    auto.add_argument("project_path")
    auto.add_argument("catalog_path")
    auto.add_argument("--task", required=True)
    auto.add_argument("--budget", type=float)
    auto.add_argument("--output")
    args = parser.parse_args(argv)
    if args.command == "validate":
        data = load_json(args.path)
        if not isinstance(data, dict):
            raise SystemExit("configuration must be a JSON object")
        print(json.dumps({"valid": True, "keys": sorted(data)}, indent=2))
    elif args.command == "plan":
        result = build_weekly_plan(load_json(args.task_path), load_json(args.catalog_path))
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(rendered + "\n")
        print(rendered)
    elif args.command == "recommend":
        project = load_json(args.project_path)
        catalog = load_json(args.catalog_path)
        budget = args.budget if args.budget is not None else project.get("default_budget_usd")
        result = recommend(args.task, project, catalog, budget)
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(rendered + "\n")
        print(rendered)
    else:
        task = load_json(args.path)["task"]
        candidates = [Candidate("example/model", frozenset(task["required_capabilities"]), Pricing(1, 5, 1))]
        result = route(candidates, task["required_capabilities"], task["input_tokens"], task["expected_output_tokens"], task.get("max_cost_usd"))
        print(json.dumps(result.__dict__, indent=2))

if __name__ == "__main__":
    main()
