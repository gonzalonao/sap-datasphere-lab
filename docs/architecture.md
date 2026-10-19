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

Unit 01 in progress, built in the own space `NW_LAB` (2 GB disk / 1 GB memory, time data
1900–2050). Deployed: local tables `LT_NW_CUSTOMERS`, `LT_NW_ORDERS`,
`LT_NW_ORDER_DETAILS`; fact view `FACT_NW_SALES`; analytic model `AM_NW_SALES`;
connection `CN_NW_ODATA` (Generic OData V4, validated). Consumed live by the SAC story
`Northwind Sales Overview`. Next: remote table `RT_NW_ORDERS` replacing `LT_NW_ORDERS`.

```mermaid
flowchart LR
    CSV[CSV files] --> LT[LT_NW_CUSTOMERS<br/>LT_NW_ORDERS<br/>LT_NW_ORDER_DETAILS]
    LT --> F[FACT_NW_SALES]
    F --> AM[AM_NW_SALES]
    AM -->|live| SAC[SAC story]
    OD[Northwind OData V4] -.->|CN_NW_ODATA| NW[(space NW_LAB)]
```
