# Phase C evidence

Screenshots from the SAP Datasphere tenant, taken during the build (2026-10-30 to 2026-11-03).
Tenant URLs and host names are cropped out. Steps refer to the
[phase summary](../../phases/phase-c-modelling.md); the narrative is in the
[build log](../../build-log.md).

## Dimensions and the star

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`c3-product-dependency.png`](c3-product-dependency.png) | C3 | *Dependency Analysis* on `DIM_NW_PRODUCT`: lineage plus associations to Category (→ texts) and Supplier; impact → Order Line |
| [`c3-fact-star-dependency.png`](c3-fact-star-dependency.png) | C3 | *Dependency Analysis* on `FACT_NW_ORDER_LINE`: four dimensions, the product snowflake and the time dimension |

## Hierarchies

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`c4-category-product-preview.png`](c4-category-product-preview.png) | C4 | Level-based `Category - Product`: (all), categories, Beverages expanded |
| [`c4-reports-to-preview.png`](c4-reports-to-preview.png) | C4 | Parent-child `Reports To`: Fuller and Buchanan's team |
| [`c4-select-hierarchy-directory.png`](c4-select-hierarchy-directory.png) | C4 | *Select Hierarchy* on Customer: the flat presentation and the two directory trees |
| [`c4-customer-directory-preview.png`](c4-customer-directory-preview.png) | C4 | `Customers by location`: UK expanded with uneven depth, USA → ID → Boise |

## View persistence

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`c5-union-baseline.png`](c5-union-baseline.png) | C5 | *Runtime Metrics*, `V_NW_SALES_UNION`, Virtual |
| [`c5-bp-baseline.png`](c5-bp-baseline.png) | C5 | *Runtime Metrics*, `V_S4_BP_BY_CATEGORY`, Virtual, one limited federated table |
| [`c5-union-view-analyzer.png`](c5-union-view-analyzer.png) | C5 | View Analyzer on the union: candidate score 10, local sources N/A |
| [`c5-bp-before-after.png`](c5-bp-before-after.png) | C5 | *Runtime Metrics*, previous vs. latest run: Virtual 0.49 / 1.47 s → Persisted 0.01 / 0.01 s |

Five screenshots are still to come: the union's partition metrics and before/after, and the
Intelligent Lookup's rules, its rates after review, and `DIM_NW_COUNTRY`.
