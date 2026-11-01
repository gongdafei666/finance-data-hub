# Kiro usage notes (honest draft)

> Written for Kiroween 2026 based on **artifacts that actually exist in this
> repository**. Do not claim IDE/CLI session transcripts, custom agents, MCP
> wiring, or property-based testing unless those are added later and reflected
> here.

## What this repo contains under `/.kiro`

### Steering (`.kiro/steering/`)

| File | Inclusion | Role |
|------|-----------|------|
| `product.md` | `inclusion: always` | Product purpose, users, Frankenstein goals, non-goals |
| `tech.md` | `inclusion: always` | Python/FastAPI stack, Docker, testing preferences |
| `structure.md` | `inclusion: always` | Directory layout, naming, import boundaries |

These foundation files are meant to keep agent output aligned with the adapter
pattern and mock-first data path.

### Specs (`.kiro/specs/data-hub/`)

| File | Role |
|------|------|
| `requirements.md` | EARS-style acceptance criteria for sources, quotes, merge, demo, Docker |
| `design.md` | Architecture diagram (text), incompatible payload shapes, API table |
| `tasks.md` | Implementation checklist (scaffold tasks marked done; live adapters deferred) |

The feature name is `data-hub`. Spec-driven structure follows Kiro’s
requirements → design → tasks workflow; implementation in `app/` matches that plan.

### Hooks (`.kiro/hooks/`)

| File | Trigger | Action |
|------|---------|--------|
| `lint-on-save.json` | `PostFileSave` matching `\.py$` | Run `ruff check` (best-effort) |

This is a valid v1 hook JSON. It automates a lint pass after Python file saves;
it does **not** claim broader CI, security scanning, or stop hooks unless added.

## What this draft does **not** claim

- No claim that a particular Kiro IDE / CLI / Web / Crew session authored every
  file (this scaffold was assembled on the build box to match the planned
  `.kiro` layout).
- No custom agents, MCP servers, or PBT suites are present in-repo as of this
  draft.
- No production live market-data credentials or paid vendor integrations.

## How to extend Kiro usage for the final Devpost write-up

1. Open the project in Kiro and load the existing steering/spec files.
2. Optionally create a custom agent that references `#[[file:.kiro/steering/**/*.md]]`.
3. Implement deferred task 11 (live adapters) via `/spec` task execution and
   keep `tasks.md` status in sync.
4. Update this document with concrete session evidence (screenshots, hook run
   logs, or CLI commands) before submission.

## Related docs

- Category framing and short blurb: [DEVPOST.md](DEVPOST.md)
- Run instructions: [../README.md](../README.md)
