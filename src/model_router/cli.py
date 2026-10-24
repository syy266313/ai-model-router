import argparse
import json
from pathlib import Path
from .cost import Pricing
from .router import Candidate, route

def load_json(path):
    return json.loads(Path(path).read_text())

def main(argv=None):
    parser = argparse.ArgumentParser(prog="model-router")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("path")
    estimate = sub.add_parser("estimate")
    estimate.add_argument("path")
    args = parser.parse_args(argv)
    if args.command == "validate":
        data = load_json(args.path)
        if not isinstance(data, dict):
            raise SystemExit("configuration must be a JSON object")
        print(json.dumps({"valid": True, "keys": sorted(data)}, indent=2))
    else:
        task = load_json(args.path)["task"]
        candidates = [Candidate("example/model", frozenset(task["required_capabilities"]), Pricing(1, 5, 1))]
        result = route(candidates, task["required_capabilities"], task["input_tokens"], task["expected_output_tokens"], task.get("max_cost_usd"))
        print(json.dumps(result.__dict__, indent=2))

if __name__ == "__main__":
    main()
