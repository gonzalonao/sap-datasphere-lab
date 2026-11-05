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
