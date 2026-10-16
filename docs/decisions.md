# Decision log

Design decisions and changes to the project plan, newest first.

## 2026-10-16 — Unit 01 plan corrected before tenant work

- **Decision:** Reordered unit 01 to follow the course order (space → first model → first
  story → remote source → time dimension and associations) and made a minimal analytic
  model `AM_NW_SALES` part of the unit instead of an optional fallback.
- **Why:** SAC stories read analytic models, not Fact views directly, so the first story
  needs one. The course introduces the time dimension and associations after the remote
  source, and the story is extended once they exist. Other fixes: space creation needs the
  global DW Administrator role, `PostalCode` must be imported as string, the source swap
  uses the drop-on-node *Replace* action, and associations are inspected in the analytic
  model rather than in the view.

## 2026-10-15 — Unit 01 is a vertical slice across phases

- **Decision:** Unit 01 covers space setup (P0) *and* a first pass through ingestion (P1),
  a graphical view (P2), associations and a time dimension (P3) and a SAC story (P6).
  It is booked under P0; P1–P3 and P6 get later units that deepen each slice, and those
  phases only close once their own units are done.
- **Why:** The course's first unit goes end to end on a small scale. Splitting it by phase
  would break the course order and the objectives I named.

## 2026-10-15 — Naming convention

- **Decision:** `<TYPE>_<DOMAIN>_<ENTITY>` in UPPER_SNAKE_CASE with fixed type prefixes
  (see `docs/naming.md`).
- **Why:** Object type is visible in every list and lineage graph; consistent with SAP
  Datasphere having no folder structure for objects.

## 2026-10-15 — CSV files generated from the OData service

- **Decision:** The flat-file source is exported by `scripts/export_northwind.py` from the
  same OData service later used as remote source; the CSVs are not committed.
- **Why:** The licence of Northwind redistribution is unclear. Same data on both paths also
  makes the "replace local table by remote table" check meaningful: totals must not move.

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
