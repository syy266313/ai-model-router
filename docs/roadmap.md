# Roadmap

## Phase 0: foundation

- [x] Public/private configuration boundary
- [x] Project, role, task, workflow, model, and evidence concepts
- [x] Cost estimator with relay multiplier
- [x] Minimal role-capability router
- [ ] Real schema validation
- [ ] CI tests

## Phase 1: weekly research and routing

- Search provider interface
- Page fetcher with SSRF protections
- Official, relay, community, and runtime evidence types
- Weekly dated snapshots instead of continuous monitoring
- Compare this week's sources with the previous snapshot
- Weekly project-to-role-to-model routing report
- Evidence freshness and conflict reporting
- Model catalog update reports
- Optional urgent refresh when the user requests it or a material incident is known

## Phase 2: multi-model workflows

- Workflow graph execution
- Structured artifacts between steps
- Human approval gates
- Fallback and retry policies
- Parallel review panels

## Phase 3: evaluation

- Reproducible task suites
- Cost, latency, correctness, and rework metrics
- Project-specific model rankings
- Pull-request catalog updates

## Overnight acceptance criteria

- Repository is publicly created under `syy266313`
- No secret or private project data is committed
- CLI cost and routing tests pass
- README explains that projects use multiple model roles
- Research and workflow boundaries are documented
