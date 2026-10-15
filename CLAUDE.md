# SAP Datasphere Lab — Claude Code Instructions

## Objective

Build **one end-to-end SAP data project**, developed by me in a real SAP Datasphere tenant
and split into documented phases. The driver is an SAP Datasphere training course whose own
material is weak: I tell you each course unit's objective, and you turn it into a practical
exercise that advances the project.

The end result must stand on its own as a portfolio project. It should go from source
systems through ingestion, modelling, security and orchestration to consumption, and it
should be readable cold by a recruiter or a colleague.

Priorities, in order:

1. **Course concepts first.** Every objective I name from the course must be covered
   explicitly by an exercise. Never skip or merge one away.
2. **Coherent project.** Each exercise extends the same scenario and builds on objects
   created earlier. Adapt the project plan to the course order when needed, and record
   every change in `docs/decisions.md`.
3. **Relevance to my professional environment** (see below). Fill any gaps the course
   leaves with the parts of SAP that matter in that environment.

## Professional context

I'm a data/BI consultant at a Microsoft-stack data consultancy. Day-to-day projects run on
ERP → Azure Data Factory → Azure Databricks (medallion) → Power BI. SAP Datasphere is being
added, and **SAP Business Data Cloud (BDC)** is expected soon. Background: Python, SQL,
data engineering and advanced Power BI (PL-300), so pitch explanations above basics.

As a result, the project must emphasise:

- **SAP sources:** S/4HANA-style data and OData APIs, plus flat files.
- **Federation vs. replication trade-offs:** remote tables, replication flows, data flows,
  transformation flows.
- **Semantic modelling:** dimensions, facts, associations, hierarchies, text, time, and
  analytic models.
- **Governance:** spaces, roles, data access controls, cross-space sharing.
- **Orchestration and monitoring:** task chains, schedules, data integration monitor.
- **Consumption:** SAP Analytics Cloud, and above all **Power BI**.
- **Interoperability with the Microsoft/Databricks stack:** premium outbound integration
  and BDC data products / Delta Sharing to Azure Databricks, when the tenant allows it.

## Scenario

**Northwind Traders** (public sample data) is the spine, available as flat files and as a
public OData service. When the course reaches remote connections, add an SAP-flavoured
source (for example the SAP Business Accelerator Hub sandbox APIs) if Datasphere can reach
it. Otherwise document why it can't and stay on Northwind.

## Phase map (provisional, adapted as the course unfolds)

| Phase | Theme | Typical Datasphere features |
| ----- | ----- | --------------------------- |
| P0 | Tenant & governance setup | Spaces, storage, users/roles, connections |
| P1 | Ingestion | Local tables (file upload), remote tables, replication / data flows |
| P2 | Transformation | Graphical & SQL views, transformation flows, data quality checks |
| P3 | Semantic layer | Dimensions, facts, associations, hierarchies, time, analytic model |
| P4 | Security & sharing | Data access controls, cross-space sharing |
| P5 | Orchestration | Task chains, scheduling, monitoring |
| P6 | Consumption | SAP Analytics Cloud story, Power BI connection |
| P7 | Microsoft / BDC integration | Outbound to Azure / Databricks, BDC data products |

The README progress table and this map must stay in sync.

## Per-unit workflow

1. I name a course unit and its objectives. Record them in `syllabus.md`, in my words.
2. You write `units/NN-slug/README.md` from `units/_template/`. Include: the phase it
   belongs to, concepts, an exercise in the Northwind scenario, numbered steps, and
   checkable acceptance criteria. Explain *why* each design choice is made, not just the
   clicks.
3. I do the work in the tenant and report back with screenshots, errors and deviations.
4. You fill in **Results** and **Gotchas** using only what I reported. Never claim tenant
   work happened that I didn't confirm. Update the README progress table,
   `docs/architecture.md` and `docs/decisions.md`.
5. When a phase closes, write its summary in `docs/phases/PN-slug.md`.

You can't see the tenant, so the UI steps come from your knowledge. Flag steps you're unsure
of (menu names, availability on trial tenants, version changes) with **⚠ verify**. I'll
correct them.

## Documentation standards

- English, clear and professional, readable without the course material.
- Object names follow a fixed convention, recorded in `docs/naming.md` the first time
  objects are created. Use it consistently.
- Diagrams in Mermaid, so they render on GitHub.
- Screenshots in `units/NN-slug/assets/`, scrubbed of tenant URLs, user names, emails and
  company names.

## Confidentiality (public repo)

- No employer, client or course material: no slides, no copied course text, no company or
  client names, no tenant URLs or IDs, no credentials.
- Course objectives are paraphrased in my own words.
- Only public or synthetic data. Document the source URL and licence of every dataset in
  `data/README.md`. Raw downloads that can't be redistributed go in `data/raw/`
  (gitignored).

## Git

- develop-flow: one branch per unit, `feat/unit-NN-slug`, off `develop`, merged into
  `develop` when the unit is documented. At the end of each phase, open a `develop` →
  `main` PR for my review.
- Conventional Commits (`docs(unit-03): ...`, `feat(data): ...`). No AI attribution.
