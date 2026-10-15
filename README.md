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

| Phase | Theme | Units | Status |
| ----- | ----- | ----- | ------ |
| P0 | Tenant & governance setup | 01 | todo |
| P1 | Ingestion | | todo |
| P2 | Transformation | | todo |
| P3 | Semantic layer | | todo |
| P4 | Security & sharing | | todo |
| P5 | Orchestration | | todo |
| P6 | Consumption (SAC, Power BI) | | todo |
| P7 | Microsoft / BDC integration | | todo |

The phase plan is provisional. It adapts to the course order, and every change is logged in
`docs/decisions.md`.

## Units

| Unit | Topic | Phase | Status |
| ---- | ----- | ----- | ------ |
| 01   | Spaces: creation and configuration | P0 | todo |

## How to follow along

1. Get access to an SAP Datasphere tenant (trial or training tenant).
2. Read `syllabus.md` for the unit objectives.
3. Open the unit folder under `units\` and work through its exercise and acceptance criteria.

## Layout

- `syllabus.md` — the course objectives, one entry per unit.
- `units\NN-slug\README.md` — objective, concepts, exercise, steps, acceptance criteria,
  results and gotchas (see `units\_template\`).
- `units\NN-slug\assets\` — screenshots (scrubbed of tenant URLs and user names).
- `docs\` — architecture, decision log, naming convention and per-phase summaries.
- `data\` — public/synthetic sample datasets used by the exercises.

## Author

[LinkedIn](https://linkedin.com/in/gonzalolopezcrespo) · [GitHub](https://github.com/gonzalonao)
