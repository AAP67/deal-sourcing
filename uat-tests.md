# Deal Sourcing Tool — UAT Test Cases

**Version:** 1.0
**Date:** February 9, 2026
**Tester:** _______________

---

## How to Use

For each test, follow the steps, record Pass/Fail, and note any issues. Tests are ordered by the user journey: Input → Loading → Results → Export.

---

## 1. INPUT SCREEN

### TC-01: App Launch
| | |
|---|---|
| **Steps** | Run `streamlit run app.py` and open localhost:8501 |
| **Expected** | Dark-themed input page loads with logo, title "Deal Sourcing", all form fields visible |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-02: Industry Selection — Dropdown
| | |
|---|---|
| **Steps** | Click the industry dropdown, select "AI Infrastructure" |
| **Expected** | "AI Infrastructure" appears selected |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-03: Industry Selection — Custom Input
| | |
|---|---|
| **Steps** | Type "Quantum Computing" in the custom industry field |
| **Expected** | Custom text accepted, dropdown selection cleared |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-04: Stage Selection — Single
| | |
|---|---|
| **Steps** | Select "Seed" from stage options |
| **Expected** | "Seed" highlighted, 5 Seed-specific KPIs appear below |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-05: Stage Selection — Multiple
| | |
|---|---|
| **Steps** | Select both "Seed" and "Series A" |
| **Expected** | Both highlighted, KPIs merged from both stages (deduplicated), count updated |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-06: Stage Deselection — KPI Reset
| | |
|---|---|
| **Steps** | Select "Seed", select 3 KPIs, then deselect "Seed" |
| **Expected** | KPI list clears, selected KPIs reset, "Select a stage" placeholder shown |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-07: KPI — Empty State
| | |
|---|---|
| **Steps** | Load app without selecting any stage |
| **Expected** | KPI section shows "Select a stage above to load relevant KPIs" |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-08: KPI — Select All 5
| | |
|---|---|
| **Steps** | Select "Series A", then select all 5 KPIs |
| **Expected** | All 5 KPIs highlighted, counter shows "5 of 5 selected" |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-09: KPI — Select Only 1
| | |
|---|---|
| **Steps** | Select "Series A", then select only "Revenue growth > 20% MoM" |
| **Expected** | 1 KPI highlighted, counter shows "1 of 5 selected" |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-10: KPI — Custom KPI
| | |
|---|---|
| **Steps** | Select a stage, type "Crypto-native revenue model" in custom KPI field |
| **Expected** | Custom KPI added to selected KPIs list |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-11: Geography Selection
| | |
|---|---|
| **Steps** | Change geography to "Middle East / MENA" |
| **Expected** | Dropdown updates, value persists |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-12: Result Count Slider
| | |
|---|---|
| **Steps** | Move slider to 15 |
| **Expected** | Slider shows 15, cost estimate updates (~$0.45) |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-13: Search Button — Disabled State
| | |
|---|---|
| **Steps** | Load app without filling any fields |
| **Expected** | Button grayed out, reads "Select industry, stage, KPIs & API key" |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-14: Search Button — Enabled State
| | |
|---|---|
| **Steps** | Fill industry, stage, at least 1 KPI, and API key |
| **Expected** | Button turns blue, reads "🔍 Research Deals" |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-15: API Key — Invalid Key
| | |
|---|---|
| **Steps** | Enter "invalid-key-123", fill other fields, click Research Deals |
| **Expected** | Error message displayed, option to go back to search |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 2. LOADING SCREEN

### TC-16: Loading — Progress Bar Appears
| | |
|---|---|
| **Steps** | Complete valid inputs and click Research Deals |
| **Expected** | Screen transitions to loading with progress bar starting at 0% |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-17: Loading — Status Steps Progress
| | |
|---|---|
| **Steps** | Watch loading screen during research |
| **Expected** | Status text updates through: research queries → scanning databases → analyzing founders → scoring KPIs |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-18: Loading — Context Displayed
| | |
|---|---|
| **Steps** | Observe loading screen header text |
| **Expected** | Shows your selected stages and industry (e.g., "Searching Seed stage · AI Infrastructure") |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-19: Loading — Transitions to Results
| | |
|---|---|
| **Steps** | Wait for research to complete |
| **Expected** | Progress bar reaches 100%, screen transitions to results |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 3. RESULTS SCREEN

### TC-20: Results — Header Info
| | |
|---|---|
| **Steps** | Review results page header |
| **Expected** | Shows "Results", result count badge, and today's date |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-21: Results — Search Params Displayed
| | |
|---|---|
| **Steps** | Check parameter tags below header |
| **Expected** | Shows industry, stage, geo, and all selected KPIs as tags |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-22: Results — Stats Row
| | |
|---|---|
| **Steps** | Check stats cards |
| **Expected** | Shows Avg Match %, count per stage, and number of regions |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-23: Results — Company Cards Render
| | |
|---|---|
| **Steps** | Scroll through result cards |
| **Expected** | Each card shows: company name, domain, stage, location, last round, match score with color bar, signals, rationale |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-24: Results — Match Score Colors
| | |
|---|---|
| **Steps** | Check match score colors across results |
| **Expected** | 85+% = green, 75-84% = yellow, below 75% = red |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-25: Results — Expandable Details
| | |
|---|---|
| **Steps** | Click "Details" expander on any company |
| **Expected** | Shows founders, founded year, and sources in 3-column layout |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-26: Results — Sorted by Match Score
| | |
|---|---|
| **Steps** | Check order of result cards |
| **Expected** | Results ordered highest match score to lowest |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 4. STAGE + KPI ALIGNMENT (Critical)

### TC-27: Stage Filter — Seed Only
| | |
|---|---|
| **Steps** | Select "Seed" only, select KPIs, run search |
| **Expected** | ALL results show stage = "Seed". Zero results for Series A, B, C, or Growth |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-28: Stage Filter — Series A Only
| | |
|---|---|
| **Steps** | Select "Series A" only, select KPIs, run search |
| **Expected** | ALL results show stage = "Series A". Zero results for Seed, Series B, C, or Growth |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-29: Stage Filter — Multi-Stage
| | |
|---|---|
| **Steps** | Select "Seed" + "Series A", run search |
| **Expected** | Results are ONLY Seed or Series A. No other stages present |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-30: KPI Relevance — Seed KPIs
| | |
|---|---|
| **Steps** | Select Seed, select "Early product-market fit signals" + "User growth or waitlist traction", run search |
| **Expected** | Rationale text references PMF and traction, not revenue/ARR metrics |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-31: KPI Relevance — Series A KPIs
| | |
|---|---|
| **Steps** | Select Series A, select "Revenue growth > 20% MoM" + "Strong unit economics", run search |
| **Expected** | Rationale references revenue and unit economics, companies have revenue data |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 5. EXPORT & NAVIGATION

### TC-32: CSV Export
| | |
|---|---|
| **Steps** | Click "📥 Export CSV" on results page |
| **Expected** | CSV file downloads with all result fields: Company, Domain, Stage, Location, Founded, Last Round, Founders, KPI Match, Signals, Rationale, Source |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-33: CSV — Opens in Excel
| | |
|---|---|
| **Steps** | Open downloaded CSV in Excel or Google Sheets |
| **Expected** | All columns properly separated, no encoding issues, all rows present |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-34: New Search Button
| | |
|---|---|
| **Steps** | Click "← New Search" on results page |
| **Expected** | Returns to input screen with clean form, previous results cleared |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-35: Back After Error
| | |
|---|---|
| **Steps** | Trigger an error (bad API key), click "← Back to Search" |
| **Expected** | Returns to input screen with form intact |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 6. EDGE CASES

### TC-36: Empty Custom Industry
| | |
|---|---|
| **Steps** | Type spaces only in custom industry, try to search |
| **Expected** | Button remains disabled |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-37: Niche Industry
| | |
|---|---|
| **Steps** | Type "Underwater Drone Logistics", select Seed, select KPIs, run search |
| **Expected** | Returns results (possibly fewer), or graceful "no results" message |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-38: All Stages Selected
| | |
|---|---|
| **Steps** | Select all 5 stages, select KPIs, run search |
| **Expected** | Results include mix of stages, all valid |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-39: Maximum Results (25)
| | |
|---|---|
| **Steps** | Set slider to 25, run search |
| **Expected** | Returns up to 25 results without timeout or error |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-40: Minimum Results (5)
| | |
|---|---|
| **Steps** | Set slider to 5, run search |
| **Expected** | Returns exactly 5 results |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## 7. DISCLAIMER & DATA QUALITY

### TC-41: Disclaimer Visible
| | |
|---|---|
| **Steps** | Scroll to bottom of results page |
| **Expected** | Warning disclaimer visible: "Data sourced from public web results..." |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-42: Companies Are Real
| | |
|---|---|
| **Steps** | Pick 3 results and Google their names/domains |
| **Expected** | At least 2 of 3 are real, verifiable companies with matching info |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

### TC-43: Domains Are Valid
| | |
|---|---|
| **Steps** | Click/copy 3 domain names from results |
| **Expected** | Domains resolve to actual websites |
| **Result** | ☐ Pass ☐ Fail |
| **Notes** | |

---

## Summary

| Section | Total | Pass | Fail |
|---------|-------|------|------|
| Input Screen | 15 | | |
| Loading Screen | 4 | | |
| Results Screen | 7 | | |
| Stage + KPI Alignment | 5 | | |
| Export & Navigation | 4 | | |
| Edge Cases | 5 | | |
| Data Quality | 3 | | |
| **TOTAL** | **43** | | |

**Overall Result:** ☐ Pass ☐ Fail

**Tester Signature:** _______________
**Date:** _______________
