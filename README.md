# SAP Datasphere Lab

Hands-on, exercise-driven notes for learning SAP Datasphere, built step by step into one
end-to-end project.

**Tech stack:** SAP Datasphere · SQL · OData · CSV · Power BI (consumption)

## What it demonstrates

Each unit maps to one learning objective of a training course and is worked through a single
running scenario, so the exercises accumulate into a complete data-modelling project rather
than isolated demos: spaces, data loading, modelling, and consumption.

> Only public or synthetic data is used. No employer or client material is included.

## Scenario

Northwind Traders: a classic, publicly available sample company (customers, orders, order
details, products, categories, suppliers, employees). It is relational enough to support a
star schema, and is available both as flat files and as a public OData service, so file
loads and remote connections can be exercised on the same data.

## Progress

| Unit | Topic | Status |
| ---- | ----- | ------ |
| 01   | Spaces: creation and configuration | todo |

## How to follow along

1. Get access to an SAP Datasphere tenant (trial or training tenant).
2. Read `syllabus.md` for the unit objectives.
3. Open the unit folder under `units\` and work through its exercise and acceptance criteria.

## Layout

- `syllabus.md` — the course objectives, one entry per unit.
- `units\NN-slug\README.md` — objective, concepts, exercise, steps, acceptance criteria,
  results and gotchas (see `units\_template\`).
- `units\NN-slug\assets\` — screenshots (scrubbed of tenant URLs and user names).
- `data\` — public/synthetic sample datasets used by the exercises.

## Author

[LinkedIn](https://linkedin.com/in/gonzalolopezcrespo) · [GitHub](https://github.com/gonzalonao)
