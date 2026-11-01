---
inclusion: always
---

# Project Structure — Finance Data Hub

```
finance-data-hub/
├── .kiro/
│   ├── steering/          # product.md, tech.md, structure.md
│   ├── specs/data-hub/    # requirements.md, design.md, tasks.md
│   └── hooks/             # agent automation JSON
├── app/
│   ├── main.py            # FastAPI app, routes, static mount
│   ├── models.py          # Pydantic NormalizedQuote + API schemas
│   ├── adapters/          # provider-specific fetch + map
│   │   ├── base.py
│   │   ├── mock_yahoo.py
│   │   └── mock_alphavantage.py
│   ├── services/
│   │   └── hub.py         # orchestration / merge across adapters
│   └── static/
│       └── index.html     # minimal demo UI
├── tests/
├── docs/                  # KIRO_USAGE.md, DEVPOST.md
├── Dockerfile
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore             # must NOT ignore .kiro
```

## Naming

- Modules: `snake_case`
- Classes: `PascalCase` (`YahooMockAdapter`, `NormalizedQuote`)
- Routes: `/api/v1/...`

## Import pattern

- Routes call `HubService`
- `HubService` depends on a list of `QuoteAdapter` implementations
- Adapters never import FastAPI
