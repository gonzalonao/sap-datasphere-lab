# Decision log

Design decisions and changes to the project plan, newest first.

## 2026-10-15 — Project framing

- **Decision:** Build one end-to-end project in phases (P0–P7), driven by the course units,
  instead of a set of isolated exercises.
- **Why:** A coherent project is better learning and better portfolio evidence; the course
  units map onto phases as they arrive.

## 2026-10-15 — Scenario: Northwind Traders

- **Decision:** Use Northwind as the spine dataset.
- **Why:** Public, well known and relational enough for a star schema. Available both as
  flat files and as a public OData service, so file loads and remote connections run on the
  same data. An SAP-flavoured source may be added in the ingestion phase.
