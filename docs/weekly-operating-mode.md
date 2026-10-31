# Weekly operating mode

The default user workflow is one deliberate refresh per week, before the week's first model-assisted task.

## Weekly cycle

1. Load the previous snapshot and the current private project/task context.
2. Check official model documents, official prices, relay model lists, relay pricing, and relevant status information.
3. Compare the new evidence with the previous snapshot.
4. Probe only capabilities needed by this week's tasks, within the configured test budget.
5. Assign separate models to research, architecture, implementation, testing, review, and documentation as needed.
6. Produce a weekly routing plan with primary, fallback, cost estimate, evidence, confidence, and exclusions.
7. Require human approval before applying the plan to real project work.
8. Freeze the approved snapshot for reuse during the week.

## Reuse policy

The system should reuse the approved weekly snapshot for normal tasks in the same week. It should not repeatedly search or re-evaluate every time a task is submitted.

Trigger an urgent refresh only when one of these applies:

- The user explicitly asks to refresh.
- A model or relay is unavailable, renamed, deprecated, or materially changed.
- Recent task failures suggest quality or compatibility regression.
- The task is high-risk and the weekly evidence is insufficient.
- A price or budget assumption is likely to have changed.

## Weekly report contract

Every approved snapshot must record:

- `week_start` and `refreshed_at`
- source URLs, source types, and checked timestamps
- changes since the previous snapshot
- candidate models and relay mappings
- evidence status: documented, relay-claimed, or runtime-verified
- role assignments and fallbacks
- estimated weekly cost and per-task cost assumptions
- known limitations, exclusions, and confidence

The weekly snapshot is a decision record, not a permanent truth. The next weekly refresh must compare against it rather than silently overwriting it.
