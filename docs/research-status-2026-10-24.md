# Official source check: 2026-10-24

This is an access and evidence-status report, not a current model ranking or verified price sheet. No prices are copied into the catalog because the available official pages could not be reliably inspected in this environment.

## Sources checked

| Vendor | Official source | Result | Conclusion |
|---|---|---|---|
| OpenAI | https://openai.com/api/pricing/ | HTTP 403 from shell; browser navigation stalled on a localized business-pricing route | Price and current model-specific details not verified |
| OpenAI | https://platform.openai.com/docs/pricing | HTTP 403 from shell | Price and model capabilities not verified |
| OpenAI | https://platform.openai.com/docs/models | HTTP 403 from shell | Model inventory not verified |
| Anthropic | https://docs.anthropic.com/en/docs/about-claude/pricing | HTTP 200, but page content returned a regional availability page rather than pricing data | Pricing not verified; HTTP 200 is not evidence that the requested content was available |
| Google Gemini | https://ai.google.dev/gemini-api/docs/pricing | Connection timed out after 30 seconds | Pricing not verified |
| Google Gemini | https://ai.google.dev/gemini-api/docs/models | Connection timed out after 20 seconds | Model inventory not verified |

Checks were made on 2026-10-24 UTC using direct HTTP requests and the built-in browser. Network access failures are environmental and do not establish that the source is unavailable to users generally.

## What can safely be concluded

- The three requested vendor source families could not be inspected sufficiently to make current price or model capability claims.
- The example entries in `catalog/models.example.yaml` are placeholders and must not be used for recommendations.
- A production catalog needs separate evidence for upstream model capabilities, relay claims, and runtime tests.
- Relay prices cannot be inferred from upstream list prices. Relay mapping, multiplier semantics, discounts, billing units, and date must be captured independently.

## Follow-up evidence collection

1. Retry official pages from a network where they are accessible, including their stable API documentation and pricing pages.
2. Save exact model/version identifiers and each listed input/output rate with currency, billing unit, effective date, and source URL.
3. Obtain relay model-list and billing-page evidence for each configured relay.
4. Run low-cost capability probes only after explicit budget and credential configuration.
5. Keep unresolved fields `unknown`; do not substitute search snippets or remembered prices.

## Confidence

- Source access observations: high confidence for this environment and check time.
- Current model ranking/prices/capabilities: not established.
