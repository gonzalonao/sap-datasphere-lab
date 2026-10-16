# Architecture

Living view of the solution; updated as each unit adds objects.

## Target (provisional)

```mermaid
flowchart LR
    subgraph Sources
        F[Northwind flat files]
        O[Northwind OData service]
        S[SAP sandbox APIs<br/>optional]
    end
    subgraph Datasphere
        I[Ingestion space<br/>local & remote tables]
        M[Modelling space<br/>views, facts, dimensions,<br/>analytic models]
    end
    subgraph Consumption
        SAC[SAP Analytics Cloud]
        PBI[Power BI]
        DBX[Azure Databricks<br/>outbound / BDC]
    end
    F --> I
    O --> I
    S -.-> I
    I -->|shared| M
    M --> SAC
    M --> PBI
    M -.-> DBX
```

## Current state

Unit 01 is documented but not yet executed in the tenant, so nothing is confirmed built.
Planned objects (see `units/01-space-model-remote`): space `NW_LAB`, local tables
`LT_NW_CUSTOMERS`/`LT_NW_ORDERS`/`LT_NW_ORDER_DETAILS`, views `DIM_NW_CUSTOMER` and
`FACT_NW_SALES`, analytic model `AM_NW_SALES`, connection `CN_NW_ODATA`, remote table
`RT_NW_ORDERS`, generated time dimension `SAP.TIME.*`.
