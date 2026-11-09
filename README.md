# Consumer Complaint Trends & Operational Risk | 2024–2025

**Independent data analysis portfolio project by Easton Clary**

[View interactive dashboard](https://eastonclary.github.io/consumer-complaint-dashboard/) *(activate GitHub Pages after uploading index.html)*

## Executive summary
Using the CFPB Consumer Complaint Database snapshot dated November 8, 2026, this project examines **8,177,199 published complaints** received from January 1, 2024 through December 31, 2025.

- 2024: **2,734,268** published complaints.
- 2025: **5,442,931** published complaints (**+99.06%**).
- Credit reporting accounted for **2,444,705** of the **2,708,663** additional records (**90.26%**).
- Outside credit reporting, *Attempts to collect debt not owed* led complaint issues in both years.
- Timely-response shares fell slightly; timeliness is not equivalent to consumer satisfaction.

## What the interactive dashboard covers
1. Monthly published complaint volume, 2024 vs. 2025
2. Product categories and contribution to overall growth
3. Top issues, including an option to exclude credit reporting
4. Company response categories and timeliness

Each view includes supporting counts, denominators, takeaways, limitations, and calculation tables.

## Methodology
The source dataset was filtered to complaints received in 2024–2025, with all original product and issue labels preserved. Masked ZIP codes were flagged, not discarded. The cleaned subset contains unique Complaint IDs and no reversed sent/received dates. Supporting files include `CFPB_chart_calculations.csv`, `CFPB_cleaning_log.md`, and `prepare_cfpb.py`.

**Important:** These counts reflect *published complaint records*, not confirmed violations, unique consumers, complaint rates, or company performance. Publication rules and intake practices may affect year-to-year comparisons.

## Sources
- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- [CFPB data field definitions](https://cfpb.github.io/api/ccdb/fields.html)
- [2025 Consumer Response Annual Report](https://files.consumerfinance.gov/f/documents/cfpb_2025-cr-annual-report_2026-03.pdf)

This is an independent portfolio project, not affiliated with or endorsed by the CFPB.
