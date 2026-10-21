# Phases — what is built, and where the proof is

The project is built in nine phases, prioritised by topic: the core integration,
modelling, security and consumption features in depth; governance, lifecycle and SAP
Business Data Cloud briefly. This page is the **inventory**: what exists after each phase,
and a link to its summary and evidence. Why each choice was made is in
[`../decisions.md`](../decisions.md).

| Phase | Focus | Status | Summary / evidence |
| ----- | ----- | ------ | ------------------ |
| A | Foundation | ✅ | [summary](phase-a-foundation.md) · [detailed record](../../units/01-space-model-remote/README.md) |
| B | Ingestion & integration | ⬜ next | |
| C | Modelling in the Data Builder | ⬜ | |
| D | Semantic layer & security | ⬜ | |
| E | Orchestration & operations | ⬜ | |
| F | Consumption (SAC, Power BI) | ⬜ | |
| G | Governance & lifecycle (brief) | ⬜ | |
| H | BDC & advanced (brief) | ⬜ | |
| I | Evidence & documentation | ⬜ | |

## What each phase builds

**A — Foundation.** Own space with quota and scoped roles; CSV local tables; a graphical
fact view; an analytic model and a live SAC story; a Generic OData connection with its TLS
certificate; a remote table swapped in and snapshot-replicated; a customer dimension and
the generated time dimension joined by association.

**B — Ingestion & integration.** The connector landscape and connection features; remote
tables accessed remotely vs. replicated (snapshot, real-time), measured; scheduled
replication; replication flows with delta from an Azure SQL Database, carried into a
target table by a transformation flow, and written out to Azure Data Lake Storage Gen2
for Azure Databricks; a reachability check on an S/4HANA-style sandbox API; data flows with
standard operators and the Python script operator; the space's Open SQL schema and
database user; an external dataset from the Data Marketplace.

**C — Modelling.** SQL and graphical views in layers; joins and unions; product, employee,
supplier and geography dimensions with text entities; every association type; level-based
and parent-child hierarchies; view persistence measured before and after; Intelligent
Lookup to match external data.

**D — Semantic layer & security.** An analytic model with calculated and restricted
measures and variables; row-level data access controls proven with two identities;
an ingestion space shared into the modelling space.

**E — Orchestration & operations.** A scheduled task chain over replication flow,
transformation flow, data flow and persistence; the Data Integration Monitor and System Monitor; a troubleshooting
runbook from this build's real incidents.

**F — Consumption.** The full SAC story (hierarchies, variables, restricted measures) and
Power BI over Datasphere, reconciled to the same totals and the same row-level security.

**G — Governance & lifecycle (brief).** Custom vs. standard roles; catalog publishing,
tags and lineage; transport between spaces or tenants; the Datasphere CLI; business
content.

**H — BDC & advanced (brief).** SAP Business Data Cloud data products and zero-copy
sharing to Databricks; BW modernization with BDC; HANA's built-in machine learning; the
object store and file spaces.

**I — Evidence & documentation.** Build log, data dictionary, evidence catalogues, demo
recording and release.
