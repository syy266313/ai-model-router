# AI Model Router

An open-source, evidence-based multi-model routing system for software projects.

AI Model Router helps a project choose **different models for different roles and workflow stages**. It combines web research, capability verification, relay pricing, cost estimation, project constraints, and reproducible evaluations.

## Core idea

```text
project -> workflow -> task -> role -> candidate models -> evidence-based route
```

A project is not tied to one model. Research, architecture, implementation, testing, review, and documentation can each use a different model and provider.

## Current scope

This first slice provides:

- Public configuration schemas for projects, roles, providers, models, and workflows
- Role-based route selection with capability, budget, latency, and privacy constraints
- Token cost estimation including relay multipliers
- Evidence records with source type, verification date, and confidence
- A research adapter boundary for search and page-fetch implementations
- A CLI foundation suitable for later web-search and benchmark integrations

## Quick start

From the repository root, use the source tree explicitly:

```bash
PYTHONPATH=src python3 -m model_router.cli validate config/task.example.json
PYTHONPATH=src python3 -m model_router.cli estimate config/task.example.json
```

The current CLI accepts JSON. YAML examples document the intended richer project configuration and will become executable when schema loading is added.

## Privacy boundary

The public repository must never contain API keys, cookies, private relay URLs, private project source, or personal usage logs. Copy `.env.example` to `.env` locally and keep private configuration outside Git. See `docs/security.md`.

## Status

Early architecture and MVP foundation. Model facts and prices are examples until verified against current official and relay sources.

## License

Apache-2.0. See `LICENSE`.
