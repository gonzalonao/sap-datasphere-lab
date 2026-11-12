# Phase D evidence

Screenshots from the SAP Datasphere tenant, taken during the build (from 2026-11-05).
Tenant URLs and host names are cropped out.

## Analytic model measures

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`d1-preview-restricted.png`](d1-preview-restricted.png) | D1 | `AM_NW_ORDER_LINE` by `SOURCE_SYSTEM`: the restricted measure matches `Revenue` on `AZURE_LIVE` and is empty on `CSV_ARCHIVE` |
| [`d1-preview-year.png`](d1-preview-year.png) | D1 | By `Year`: `Revenue 1997` only on the 1997 row, next to `Revenue` for 1996–1998 |
| [`d1-preview-exception.png`](d1-preview-exception.png) | D1 | No dimension on the rows: `Revenue` 1,265,792.64 and `Largest Customer Revenue` 110,277.29, the largest customer's revenue |
| [`d1-preview-country-share.png`](d1-preview-country-share.png) | D1 | All 21 customer countries: revenue, the constant-selection base, share of total and largest customer. The base is an auxiliary measure, hidden in the preview, so its flag was switched off for this shot |
| [`d1-preview-filter.png`](d1-preview-filter.png) | D1 | Filter `Customer Country` = USA: the constant-selection base stays 1,265,792.64 and the share stays 19.40 % |
| [`d1-measures-list-top.png`](d1-measures-list-top.png) | D1 | Model properties, top of the list of 10 measures, taken during a deploy. The eye icon marks the auxiliary measure |
| [`d1-measures-list.png`](d1-measures-list.png) | D1 | The rest of the list, with the model deployed |

## Variables

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`d2-fact-input-parameter.png`](d2-fact-input-parameter.png) | D2 | `FACT_NW_ORDER_LINE` with a filter node between the union and the output, and the input parameter `Minimum Quantity`. The data preview at the default 1 returns all 2,155 lines |
| [`d2-fact-source-mapping.png`](d2-fact-source-mapping.png) | D2 | The model's fact source: the input parameter `Minimum Quantity` shows *Mapped to: Minimum Quantity*, the standard variable. The mapping is set from the **⋯** menu on the parameter |
| [`d2-prompt.png`](d2-prompt.png) | D2 | The model's prompt with its three variables: `Customer Country` (filter, optional), `Selected Country` (restricted measure, default Germany) and `Minimum Quantity` (standard, mapped to the fact's parameter). Behind it, minimum quantity 50 gives `Revenue` 378,969.71 and `Quantity` 15,288, which matches the CSVs |
| [`d2-sac-prompt.png`](d2-sac-prompt.png) | D2 | The same three variables prompted in an SAC story, in the same order, set to USA / USA / 50 |
| [`d2-sac-story.png`](d2-sac-story.png) | D2 | The story table with those values: `Revenue` and `Revenue Selected Country` both 79,001.12 and `Quantity` 3,537, matching the CSVs. The prompt reopens from the **{…}** icon in the *Tools* group |

## Data access controls

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`d3-single-values-dac.png`](d3-single-values-dac.png) | D3 | The test view `V_NW_PRODUCT_DAC` over the product dimension, protected by the *Single Values* control `DAC_NW_CATEGORY` (shield icon in the properties) and previewed as the made-up user `DEMO_DAIRY_SEAFOOD`: 22 rows, only Dairy Products (4) and Seafood (8) |
