# CFPB cleaning log | 2024–2025

Source: https://files.consumerfinance.gov/ccdb/complaints.csv.zip (November 8, 2026 snapshot).
Source archive SHA-256: edc348782d88199b650ba1745dd36772a2618826883906e5fdbc3a8d27314641
Input opened read-only. Rebuild with Python 3.9+ and the exact original archive: `python prepare_cfpb.py CFPB_original_2026-11-08.zip new_output_directory`.

## Row reconciliation

- Source records: 19,020,152.
- Received before 2024-01-01: 4,505,149 excluded.
- Received after 2025-12-31: 6,337,804 excluded.
- Selected and written: 8,177,199. Other exclusions: 0. Duplicate IDs: 0. Blank IDs: 0.
- Coverage: 2024-01-01 through 2025-12-31, 731 distinct receipt dates.
- 2024: 2,734,268 complaints.
- 2025: 5,442,931 complaints.

## Transformations and checks

Retained all 15 original fields and their order. Kept Complaint ID as a unique key. Read IDs, geographic codes and original date strings as text. Checked ISO dates. Selected on Date received only, inclusively. Trimmed Unicode whitespace at both ends of each retained field (including nonbreaking spaces). Internal spacing and spelling were preserved.
Rows with trimming: 10. Cells trimmed: 10. Changed fields: {'Company': 10}.

Added six fields. Flags use 1 for true and 0 for false.

| Field | Definition |
|---|---|
| sent_before_received | Date sent to company is earlier than Date received. |
| zip_status | Five ASCII digits, partial/masked (three digits or three digits plus XX), fully masked (XXXXX), missing, or malformed. Case-insensitive masks. This is a format check only. |
| zip_masked | Partial or fully masked. |
| zip_malformed | Nonempty value outside the recognized formats. |
| response_stage | Completed for explicit closed categories. In progress, Untimely response, Missing and Other / unknown remain separate. |
| any_quality_flag | At least one date-order, ZIP masking, or malformed ZIP flag. Missing ZIP is reported separately. |

## Flags and response stages

- Distinct flagged complaints: 553,624. Reversed dates: 0. Date and ZIP flag overlap: 0.
- ZIP / Five digits: 7,623,575.
- ZIP / Partial / masked: 509,714.
- ZIP / Fully masked: 43,910.
- ZIP / Malformed: 0.
- ZIP / Missing: 0.
- Response / Completed: 8,166,022.
- Response / In progress: 275.
- Response / Untimely response: 10,889.
- Response / Missing: 13.
- Response / Other / unknown: 0.

## Empty original fields after trimming

| Column | Rows | % of subset |
|---|---:|---:|
| Date received | 0 | 0.0000% |
| Product | 0 | 0.0000% |
| Sub-product | 5 | 0.0001% |
| Issue | 6 | 0.0001% |
| Sub-issue | 152,986 | 1.8709% |
| Company public response | 3,333,594 | 40.7669% |
| Company | 0 | 0.0000% |
| State | 14,374 | 0.1758% |
| ZIP code | 0 | 0.0000% |
| Tags | 7,929,883 | 96.9755% |
| Submitted via | 0 | 0.0000% |
| Date sent to company | 0 | 0.0000% |
| Company response to consumer | 13 | 0.0002% |
| Timely response? | 0 | 0.0000% |
| Complaint ID | 0 | 0.0000% |

Blank optional fields are retained. A missing public response does not establish a missing response to the consumer. Blank tags do not establish demographic status. Masked and malformed ZIPs are retained verbatim. Reversed dates should be excluded from elapsed-time metrics or shown separately, while those records still count toward volume.

## Classification and interpretation

CFPB periodically changed the form (including 2017, 2023 and 2026). The full snapshot contains distinct historical labels such as ‘Credit reporting’, ‘Credit reporting, credit repair services, or other personal consumer reports’, and ‘Credit reporting or other personal consumer reports’. Issue wording also differs, e.g. investigation into an existing problem by a company versus by a credit reporting company. These are observations, not a crosswalk. Retained all Product and Issue labels, with no merges. The 2026 form update postdates the selected receipt period. See https://www.consumerfinance.gov/data-research/consumer-complaints/ for historical classification updates.
Counts describe published complaints. Consumer identity, verified violations, customer populations and company complaint rates cannot be derived from these records. Outcome distributions over completed cases should use the Completed denominator. The raw response column preserves relief and closure details.

### Product labels observed by year

| Product | 2024 | 2025 |
|---|---:|---:|
| Checking or savings account | 52,821 | 84,195 |
| Credit card | 75,989 | 89,978 |
| Credit reporting or other personal consumer reports | 2,365,586 | 4,810,291 |
| Debt collection | 155,894 | 283,197 |
| Debt or credit management | 2,413 | 4,266 |
| Money transfer, virtual currency, or money service | 16,751 | 84,619 |
| Mortgage | 21,438 | 24,697 |
| Payday loan, title loan, personal loan, or advance loan | 9,036 | 13,137 |
| Prepaid card | 6,323 | 6,502 |
| Student loan | 14,657 | 21,281 |
| Vehicle loan or lease | 13,360 | 20,768 |

### Issue labels observed by year

| Issue | 2024 | 2025 |
|---|---:|---:|
| (empty) | 6 | 0 |
| Advertising | 70 | 99 |
| Advertising and marketing, including promotional offers | 2,766 | 3,105 |
| Applying for a mortgage or refinancing an existing mortgage | 2,154 | 2,597 |
| Attempts to collect debt not owed | 70,171 | 115,682 |
| Can't contact lender or servicer | 128 | 203 |
| Can't stop withdrawals from your bank account | 115 | 209 |
| Charged fees or interest you didn't expect | 2,144 | 3,434 |
| Charged upfront or unexpected fees | 431 | 700 |
| Closing an account | 7,466 | 10,178 |
| Closing on a mortgage | 1,427 | 2,051 |
| Closing your account | 4,273 | 6,224 |
| Communication tactics | 6,459 | 9,517 |
| Confusing or misleading advertising or marketing | 413 | 945 |
| Confusing or missing disclosures | 784 | 2,894 |
| Credit limit changed | 24 | 29 |
| Credit monitoring or identity theft protection services | 11,571 | 8,502 |
| Dealing with your lender or servicer | 10,399 | 12,063 |
| Didn't provide services promised | 749 | 1,127 |
| Electronic communications | 2,203 | 4,311 |
| False statements or representation | 16,916 | 38,459 |
| Fees or interest | 6,343 | 7,836 |
| Fraud or scam | 6,173 | 11,179 |
| Getting a credit card | 9,683 | 10,805 |
| Getting a line of credit | 420 | 405 |
| Getting a loan | 442 | 369 |
| Getting a loan or lease | 1,908 | 2,664 |
| Getting the loan | 726 | 1,081 |
| Identity theft protection or other monitoring services | 388 | 581 |
| Improper use of your report | 706,919 | 1,101,571 |
| Incorrect exchange rate | 28 | 29 |
| Incorrect information on your report | 1,191,386 | 2,834,674 |
| Issue where my lender is my school | 56 | 78 |
| Issue with income share agreement | 53 | 94 |
| Issues with repayment | 73 | 144 |
| Loan payment wasn't credited to your account | 93 | 145 |
| Lost or stolen money order | 177 | 224 |
| Lost or stolen refund | 7 | 4 |
| Managing an account | 30,197 | 44,960 |
| Managing the loan or lease | 3,943 | 5,895 |
| Managing, opening, or closing your mobile wallet account | 758 | 1,773 |
| Money was not available when promised | 1,604 | 2,429 |
| Money was taken from your bank account on the wrong day or for the wrong amount | 72 | 133 |
| Opening an account | 4,826 | 6,957 |
| Other features, terms, or problems | 6,770 | 8,416 |
| Other service problem | 545 | 2,064 |
| Other transaction problem | 3,007 | 53,893 |
| Overdraft, savings, or rewards features | 19 | 64 |
| Problem adding money | 80 | 195 |
| Problem caused by your funds being low | 3,530 | 11,939 |
| Problem getting a card or closing an account | 735 | 1,105 |
| Problem when making payments | 5,200 | 6,210 |
| Problem with a company's investigation into an existing issue | 1,190 | 2,569 |
| Problem with a company's investigation into an existing problem | 466,682 | 867,387 |
| Problem with a lender or other company charging your account | 6,407 | 9,609 |
| Problem with a purchase or transfer | 1,560 | 1,832 |
| Problem with a purchase shown on your statement | 14,595 | 19,811 |
| Problem with additional add-on products or services | 704 | 862 |
| Problem with cash advance | 46 | 46 |
| Problem with credit report or credit score | 0 | 1 |
| Problem with customer service | 699 | 1,153 |
| Problem with fraud alerts or security freezes | 8,681 | 15,354 |
| Problem with overdraft | 19 | 27 |
| Problem with the payoff process at the end of the loan | 682 | 1,016 |
| Problems at the end of the loan or lease | 1,928 | 2,689 |
| Problems receiving the advance | 39 | 78 |
| Property was damaged or destroyed property | 0 | 4 |
| Property was sold | 3 | 13 |
| Received a loan you didn't apply for | 191 | 256 |
| Repossession | 3,109 | 5,932 |
| Struggling to pay mortgage | 5,142 | 5,980 |
| Struggling to pay your bill | 832 | 1,233 |
| Struggling to pay your loan | 1,636 | 2,435 |
| Struggling to repay your loan | 2,658 | 4,294 |
| Threatened to contact someone or share information improperly | 1,576 | 2,601 |
| Took or threatened to take negative or legal action | 10,750 | 48,578 |
| Trouble accessing funds in your mobile or digital wallet | 1,366 | 3,038 |
| Trouble during payment process | 11,743 | 12,680 |
| Trouble using the card | 3,319 | 2,679 |
| Trouble using your card | 2,315 | 3,020 |
| Unable to get your credit report or credit score | 8,478 | 14,988 |
| Unauthorized transactions or other transaction problem | 1,660 | 5,758 |
| Unauthorized withdrawals or charges | 258 | 465 |
| Unexpected fees | 33 | 69 |
| Unexpected or other fees | 947 | 1,407 |
| Vehicle was damaged or destroyed the vehicle | 25 | 37 |
| Vehicle was repossessed or sold the vehicle | 82 | 149 |
| Was approved for a loan, but didn't receive money | 18 | 23 |
| Was approved for a loan, but didn't receive the money | 64 | 105 |
| Written notification about debt | 47,819 | 64,049 |
| Wrong amount charged or received | 182 | 459 |
