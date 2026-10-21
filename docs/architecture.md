# Architecture

Living view of the solution; updated as each unit adds objects.

## Target

```mermaid
flowchart LR
    subgraph Sources
        F[Northwind flat files]
        O[Northwind OData service]
        AZ[Azure SQL Database<br/>Northwind, delta source]
        S[SAP sandbox APIs<br/>optional]
    end
    subgraph Datasphere
        I[Ingestion space<br/>local & remote tables]
        M[Modelling space<br/>views, facts, dimensions,<br/>analytic models]
    end
    subgraph Consumption
        SAC[SAP Analytics Cloud]
        PBI[Power BI]
        DBX[Azure Databricks<br/>BDC data products, optional]
    end
    F --> I
    O --> I
    AZ -->|replication flow| I
    S -.-> I
    I -->|shared| M
    M --> SAC
    M --> PBI
    M -.-> DBX
```

## Current state

After unit 01, everything lives in the own space `NW_LAB` (2 GB disk / 1 GB memory, time
data 1900–2050). A minimal star schema: one fact view with two associations, consumed
live by SAC through an analytic model.

| Layer | Objects |
| ----- | ------- |
| Sources | Northwind CSV files (generated from the OData service); Northwind OData V4 via `CN_NW_ODATA` |
| Ingestion | `LT_NW_CUSTOMERS`, `LT_NW_ORDER_DETAILS` (local, CSV); `RT_NW_ORDERS` (remote table, snapshot replication); `LT_NW_ORDERS` (kept, no longer used) |
| Semantic | `FACT_NW_SALES` (Fact); `DIM_NW_CUSTOMER` (Dimension); `SAP.TIME.*` (generated time data) |
| Consumption | `AM_NW_SALES` (analytic model) → SAC story `Northwind Sales Overview` |

```mermaid
flowchart LR
    CSV[CSV files] --> LT[LT_NW_CUSTOMERS<br/>LT_NW_ORDER_DETAILS]
    OD[Northwind OData V4] -->|CN_NW_ODATA<br/>snapshot| RT[RT_NW_ORDERS]
    LT --> F[FACT_NW_SALES<br/>Fact]
    RT --> F
    LT --> D[DIM_NW_CUSTOMER<br/>Dimension]
    F -.association.-> D
    F -.association.-> T[SAP.TIME.VIEW_DIMENSION_DAY<br/>Dimension]
    F --> AM[AM_NW_SALES]
    D --> AM
    T --> AM
    AM -->|live| SAC[SAC story]
```

Solid arrows are data flows; dotted arrows are associations, resolved by the analytic
model only when a query asks for the dimension.
