# Relay adapter contract

A relay must be modeled as an independent delivery and billing layer, not as a model vendor. The same upstream model may have different IDs, features, limits, and prices across relays.

## Required identity fields

- relay_id and display_name
- API base URL reference (never a secret value in public catalog)
- protocol family and supported API endpoint
- upstream provider and upstream model ID, when known
- relay model ID used in requests
- mapping verification date and evidence

## Capability fields

Store separately:

- upstream_documented_capabilities
- relay_claimed_capabilities
- runtime_verified_capabilities
- unsupported_parameters
- supported modalities and input constraints
- tool/function calling, structured output, streaming, and reasoning controls
- context and output limits, including relay-specific caps

A capability is routable only when its evidence policy is satisfied. Do not infer relay support from upstream support.

## Billing fields

- currency and billing unit
- input and output rates, including tier or model-version scope
- cache read/write rates and batch rates where applicable
- relay multiplier and the exact components it applies to
- whether multiplier applies before/after discounts or tiered pricing
- minimum charge, rounding, and currency conversion rules
- source URL, checked_at, effective_from/effective_until
- runtime billing reconciliation status

Use nullable/unknown values instead of invented rates. A price quote must include its source and checked_at. Cost estimates should disclose token estimates and exclude unmodeled fees.

## Operations fields

- rate limits, concurrency and quota scope
- timeout and retry guidance
- observed latency and error rate with sample size/time window
- regions and data-retention terms
- status page URL and incident timestamps

## Privacy

Private relay base URLs and account-specific multipliers belong in ignored local configuration. Public catalog entries may identify a relay only when its details are already public and approved for publication. Never persist credentials in adapter metadata.
