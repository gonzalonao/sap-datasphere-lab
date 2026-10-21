# SAP Datasphere Lab

An end-to-end SAP Datasphere project, built phase by phase from source data to Power BI and
SAP Analytics Cloud, with every step documented as a reproducible exercise.

**Tech stack:** SAP Datasphere · SQL · OData · SAP Analytics Cloud · Power BI ·
Azure Databricks (integration)

## What it demonstrates

The project follows the learning objectives of an SAP Datasphere training course. Each
course unit becomes a practical exercise that extends the same project, so the units add
up to a complete solution rather than isolated demos:

- governance with spaces and roles
- ingestion through both federation and replication
- transformation
- a semantic layer of facts, dimensions and analytic models
- row-level security
- orchestration
- consumption in SAC and Power BI
- integration with a Microsoft/Databricks data platform

See the [architecture](docs/architecture.md) and the [decision log](docs/decisions.md).

> Only public or synthetic data is used. No employer or client material is included.

## Scenario

Northwind Traders: a classic, publicly available sample company (customers, orders, order
details, products, categories, suppliers, employees). It is relational enough to support a
star schema, and is available both as flat files and as a public OData service, so file
loads and remote connections can be exercised on the same data.

## Phases

| Phase | Theme | Status |
| ----- | ----- | ------ |
| [A](docs/phases/phase-a-foundation.md) | Foundation: space, first model, SAC story, remote table, time dimension, associations | ✅ done |
| B | Ingestion & integration: remote tables, replication, schedules, replication flows, data flows, Open SQL schema, Data Marketplace | next |
| C | Modelling: SQL views, joins and unions, dimensions, text entities, hierarchies, view persistence, Intelligent Lookup | todo |
| D | Semantic layer & security: analytic model measures and variables, data access controls, cross-space sharing | todo |
| E | Orchestration & operations: task chains, monitoring, troubleshooting | todo |
| F | Consumption: SAP Analytics Cloud and Power BI | todo |
| G | Governance & lifecycle (brief): roles, catalog, transport, CLI, business content | todo |
| H | BDC & advanced (brief): data products, BW modernization, machine learning | todo |
| I | Evidence & documentation | todo |

The plan is prioritised by topic: the core integration, modelling, security and
consumption features are built in depth; governance, lifecycle and BDC topics are covered
briefly. The inventory with evidence is in [`docs/phases/`](docs/phases/README.md), and
every plan change is logged in [`docs/decisions.md`](docs/decisions.md).

## How to follow along

1. Get access to an SAP Datasphere tenant (trial or training tenant).
2. Run `python scripts\export_northwind.py` to generate the sample CSV files.
3. Follow the phases in order: [`docs/phases/`](docs/phases/README.md) lists what each one
   builds. Phase A's detailed, reproducible record is
   [`units/01-space-model-remote`](units/01-space-model-remote/README.md).

## Layout

- `docs\phases\` — the phase inventory and a summary per completed phase.
- `docs\evidence\phase-x\` — screenshots per phase, each folder catalogued in its README
  (scrubbed of tenant URLs and user names).
- `docs\` — architecture, decision log, naming convention.
- `units\01-space-model-remote\` — Phase A's detailed record (built as course unit 01).
- `syllabus.md` — the course objectives of the units that started the project.
- `datasphere\` — object definitions exported from the tenant (CSN/JSON) and trusted
  certificates.
- `data\` — source and licence notes for the datasets; raw files are generated locally.
- `scripts\` — helper scripts, e.g. `export_northwind.py` that builds the CSV files.

## Author

[LinkedIn](https://linkedin.com/in/gonzalolopezcrespo) · [GitHub](https://github.com/gonzalonao)
