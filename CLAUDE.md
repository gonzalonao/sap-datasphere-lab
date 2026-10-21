# SAP Datasphere Lab — Claude Code Instructions

## Objective

Build **one end-to-end SAP data project**, developed by me in a real SAP Datasphere tenant
and split into documented phases. It started from an SAP Datasphere training course; since
2026-10-21 the plan is driven by **my ratings of the course topics**, not by the course's
unit order.

The end result must stand on its own as a portfolio project. It should go from source
systems through ingestion, modelling, security and orchestration to consumption, and it
should be readable cold by a recruiter or a colleague.

Priorities, in order:

1. **The ratings.** `docs/private/topic-ratings.txt` (60 topics, scale 1–5 defined in its
   header) and `docs/private/plan.md` (phases A–I derived from it) are the basis. 5 = own
   sub-phase, hands-on, in depth; 4 = hands-on, covered properly; 3 = brief, expanded only
   on my explicit request; 2 = optional backlog; 1 = deprecated, not built. Never drop a
   topic rated 3 or higher without asking.
2. **Coherent project.** Each phase extends the same scenario and builds on objects created
   earlier. Record every plan change in `docs/decisions.md` (public reasoning) and
   `docs/private/plan.md`.
3. **Relevance to my professional environment** (see below).

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

**Northwind Traders** (public sample data) is the spine: flat files, the public OData
service, and Microsoft's Northwind sample script loaded into an Azure SQL Database (the
delta-capable source for replication flows). An SAP-flavoured source (for example the SAP
Business Accelerator Hub sandbox APIs) is added only if Datasphere can reach it; otherwise
document why and stay on Northwind.

## Phase map

| Phase | Theme | Main topics |
| ----- | ----- | ----------- |
| A | Foundation ✅ | Space, CSV, graphical view, analytic model, SAC story, remote table, time dimension, associations (built as course unit 01) |
| B | Ingestion & integration | Connections, remote tables (remote / snapshot / real-time), schedules, replication flows, transformation flows, data flows + script operator, Open SQL schema, Data Marketplace |
| C | Modelling | Data Builder, SQL views, joins and unions, dimensions, text entities, association types, hierarchies, view persistence, Intelligent Lookup |
| D | Semantic layer & security | Analytic model (calculated and restricted measures), variables, data access controls, cross-space sharing |
| E | Orchestration & operations | Task chains, Data Integration Monitor, System Monitor, troubleshooting runbook |
| F | Consumption | SAC story, Power BI |
| G | Governance & lifecycle (brief) | Users and roles, catalog and tags, transport, CLI, business content |
| H | BDC & advanced (brief) | BDC data products, BW modernization with BDC, machine learning |
| I | Evidence & docs | Public docs, demo, release, portfolio |

Details, sub-phases and done criteria: `docs/private/plan.md`. The README phase table and
this map must stay in sync.

## Per-phase workflow

Same workflow as the Fabric projects (`../fabric-energy-lakehouse`):

1. At the start of a phase, you write its click-level guide
   `docs/private/phases/phase-<x>-<slug>.md` from the plan, using the layout in
   `docs/private/phases/README.md`: outcome (done criteria), decisions made up front,
   *Learn first*, numbered `[YOU]`/`[CLAUDE]` steps, 🎓 / 📣 / 📸 checkpoints, *Gotchas &
   deviations*. Write guides one phase ahead, not all at once. Add the phase's step
   checkboxes to `docs/private/progress.md`.
2. Each sub-phase runs: lesson in chat → 🎓 quiz → click-level steps in chunks → I report
   → you record → post-build lesson and quiz.
3. You record results using only what I reported. Never claim tenant work happened that I
   didn't confirm. Reconcile numbers against an independent calculation where possible.
4. When a phase closes: evidence into `docs/evidence/phase-<x>/` with a catalogue
   `README.md`; write the phase summary `docs/phases/phase-<x>-<slug>.md`; update the
   inventory `docs/phases/README.md`, `docs/decisions.md`, `docs/architecture.md` and
   the README phase table; open a `develop` → `main` PR.

You can't see the tenant. **Before writing or presenting UI steps, check the current SAP
documentation**: the SAP Help Portal guides are published as markdown in
[SAP-docs/sap-datasphere](https://github.com/SAP-docs/sap-datasphere) (`docs/`; list the
tree with `gh api repos/SAP-docs/sap-datasphere/git/trees/main?recursive=1` and read files
from `raw.githubusercontent.com`). The Help Portal itself renders client-side, so use the
GitHub source. Take menu paths and labels from the docs, record the doc file in the guide
step, and mark only what the docs don't settle with **⚠ verify**. When my report
contradicts the docs, my tenant wins: fix the guide and note the deviation.

## Build journal and learning method

Same method as the Fabric projects:

- **Private build journal** in `docs/private/` (separate local git repo, gitignored by
  this repo): `plan.md`, the phase guides in `phases/`, the tracker `progress.md`,
  `learning-log.md`, `screenshots.md` and the topic ratings. At session start, read
  `progress.md` and the guide it points at.
- **Instructions to me are always click-level**: which app in the side navigation, where
  on the screen a button sits, what to type, and how to verify the result. This applies
  to ad-hoc guidance in chat too. Uncertain UI details get **⚠ verify**.
- **Interactive pace:** present one sub-phase (or one chunk of steps) at a time in chat,
  wait for my report, then continue. Don't dump a whole phase at once.
- **Teach, then test.** Each sub-phase opens with a lesson in chat: what the concepts are,
  why they matter, and analogies to the Microsoft/Databricks stack I know. Only then the
  quiz, then the click-level steps. Every quiz question must map to a lesson point taught
  in chat; material that only appears in the guide doesn't count. Post-build checks get
  their own short lesson first (what was built and what it implies).
- **📸 Screenshot list:** `docs/private/screenshots.md` holds every evidence shot still to
  take (file, step, what it shows, what to scrub). Add a row at each 📸 marker and keep it
  current; I take them in batches.
- **🎓 Learning checkpoints** before (concepts) and after (what was built) each sub-phase:
  quiz with `AskUserQuestion`, following the rules at the top of
  `docs/private/learning-log.md` (plausible distractors, shuffled answer positions, log
  misses with corrections, re-test open misconceptions).

## Standing objectives — portfolio, documentation, learning

These run alongside every phase as first-class deliverables:

1. **Portfolio.** The portfolio site lives at `../../portfolio/astro` (English entries in
   `src/content/projects/*.mdx`, Spanish mirror in `src/content/projectsEs/`;
   `fabric-energy-lakehouse.mdx` is the format precedent). At the **📣** checkpoints, remind
   me to update `sap-datasphere-lab.mdx` and help draft it: seed a draft at the end of
   Phase B, add the modelling and security narrative at D, the Power BI showcase at F, and
   finalize at I.
2. **Reproducible documentation.** A cold reader must be able to reproduce the build from
   the repo, and it must read as structured work.
3. **Learning.** Fluency in Datasphere for my job. `docs/private/learning-log.md` is the
   durable record; re-test every open miss; run the full drill bank cold in Phase I. The
   interview drills in `docs/private/plan.md` are the bar.

Keep adjacent artifacts current at phase ends: the workspace wiki (`../../wiki`) and the
master CV (`../../jobsearch/CVs/Master`) once the project has a presentable result.

## Documentation standards

- English, clear and professional, readable without the course material.
- Object names follow a fixed convention, recorded in `docs/naming.md` the first time
  objects are created. Use it consistently.
- Diagrams in Mermaid, so they render on GitHub.
- Screenshots in `docs/evidence/phase-<x>/`, each folder catalogued in its `README.md`,
  scrubbed of tenant URLs, user names, emails and company names. (Phase A's record stays
  in `units/01-space-model-remote/` until Phase I folds it into the build log.)
- Public docs follow the Fabric layout: `README.md`, `docs/phases/` (inventory and
  per-phase summaries), `docs/build-log.md` (narrative incl. incidents), `docs/decisions.md`,
  `docs/architecture.md`, `docs/data-dictionary.md`, `docs/naming.md`.

## Confidentiality (public repo)

- No employer, client or course material: no slides, no copied course text, no company or
  client names, no tenant URLs or IDs, no credentials.
- Course objectives are paraphrased in my own words. The course topic list and my ratings
  stay in `docs/private/`.
- Only public or synthetic data. Document the source URL and licence of every dataset in
  `data/README.md`. Raw downloads that can't be redistributed go in `data/raw/`
  (gitignored).

## Git

- develop-flow: one branch per phase, `feat/phase-<x>-<slug>` (e.g.
  `feat/phase-b-ingestion`), off `develop`, merged into `develop` as sub-phases are
  documented. At the end of each phase, open a `develop` → `main` PR for my review.
- Conventional Commits (`docs(phase-b): ...`, `feat(data): ...`). No AI attribution.
- Stage explicit paths only; review anything exported from the tenant before staging.
