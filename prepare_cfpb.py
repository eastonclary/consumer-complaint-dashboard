"""Run with Python 3.9+: python prepare_cfpb.py ORIGINAL.zip NEW_OUTPUT_DIRECTORY"""
import csv
import hashlib
import io
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

START, END = "2024-01-01", "2025-12-31"
EXPECTED_SHA = "edc348782d88199b650ba1745dd36772a2618826883906e5fdbc3a8d27314641"
COLUMNS = ["Date received", "Product", "Sub-product", "Issue", "Sub-issue",
           "Company public response", "Company", "State", "ZIP code", "Tags",
           "Submitted via", "Date sent to company", "Company response to consumer",
           "Timely response?", "Complaint ID"]
EXTRA = ["sent_before_received", "zip_status", "zip_masked", "zip_malformed",
         "response_stage", "any_quality_flag"]
CLOSED = {"Closed", "Closed with explanation", "Closed with monetary relief",
          "Closed with non-monetary relief", "Closed with relief", "Closed without relief"}

def checksum(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(2**20), b""):
            h.update(block)
    return h.hexdigest()

def zip_status(value):
    if not value:
        return "Missing"
    if value.upper() == "XXXXX":
        return "Fully masked"
    if re.fullmatch(r"[0-9]{3}(?:[Xx]{2})?", value):
        return "Partial / masked"
    if re.fullmatch(r"[0-9]{5}", value):
        return "Five digits"
    return "Malformed"

def response_stage(value):
    if value in CLOSED:
        return "Completed"
    if value in {"In progress", "Untimely response"}:
        return value
    return "Other / unknown" if value else "Missing"

def run(source, output_dir):
    if checksum(source) != EXPECTED_SHA:
        raise ValueError("Source differs from the profiled November 8, 2026 snapshot.")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "CFPB_complaints_2024-2025.zip"
    log = output_dir / "CFPB_cleaning_log.md"
    if output.exists() or log.exists():
        raise FileExistsError("Use a new output directory.")
    counts, missing, changed, years = Counter(), Counter(), Counter(), Counter()
    zips, stages, product, issue = Counter(), Counter(), Counter(), Counter()
    seen = bytearray()
    dates = set()
    partial = output.with_suffix(".part")
    try:
        with zipfile.ZipFile(source, "r") as original, original.open("complaints.csv") as data, \
             zipfile.ZipFile(partial, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as subset, \
             subset.open("complaints_2024-2025.csv", "w", force_zip64=True) as dest, \
             io.TextIOWrapper(dest, encoding="utf-8", newline="") as stream:
            reader = csv.reader(io.TextIOWrapper(data, encoding="utf-8-sig", newline=""))
            assert next(reader) == COLUMNS
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(COLUMNS + EXTRA)
            valid_dates = {}
            for raw in reader:
                counts["source"] += 1
                assert len(raw) == len(COLUMNS)
                received = raw[0].strip()
                if received not in valid_dates:
                    valid_dates[received] = date.fromisoformat(received).isoformat()
                    assert received == valid_dates[received]
                if received < START or received > END:
                    counts["before" if received < START else "after"] += 1
                    continue
                row = [v.strip() for v in raw]
                for name, old, new in zip(COLUMNS, raw, row):
                    if not new:
                        missing[name] += 1
                    if new != old:
                        changed[name] += 1
                counts["trimmed_rows"] += row != raw
                sent = row[11]
                if sent not in valid_dates:
                    valid_dates[sent] = date.fromisoformat(sent).isoformat()
                    assert sent == valid_dates[sent]
                ident = int(row[-1])
                assert str(ident) == row[-1] and ident > 0
                if ident >= len(seen):
                    seen.extend(bytes(ident + 10000 - len(seen)))
                assert not seen[ident], "Duplicate Complaint ID"
                seen[ident] = 1
                reversed_date = sent < received
                z = zip_status(row[8])
                masked = z in {"Fully masked", "Partial / masked"}
                malformed = z == "Malformed"
                any_flag = reversed_date or masked or malformed
                stage = response_stage(row[12])
                counts["rows"] += 1
                counts["date_flag"] += reversed_date
                counts["any_flag"] += any_flag
                counts["overlap"] += reversed_date and (masked or malformed)
                dates.add(received)
                years[received[:4]] += 1
                zips[z] += 1
                stages[stage] += 1
                product[(received[:4], row[1])] += 1
                issue[(received[:4], row[3])] += 1
                writer.writerow(row + [int(reversed_date), z, int(masked), int(malformed), stage, int(any_flag)])
        n = counts["rows"]
        assert counts["source"] == counts["before"] + n + counts["after"]
        assert n == seen.count(1) == sum(stages.values()) == sum(zips.values())
        assert counts["any_flag"] == counts["date_flag"] + zips["Fully masked"] + zips["Partial / masked"] + zips["Malformed"] - counts["overlap"]
        partial.rename(output)
        lines = [
            "# CFPB cleaning log | 2024–2025", "",
            "Source: https://files.consumerfinance.gov/ccdb/complaints.csv.zip (November 8, 2026 snapshot).",
            "Source archive SHA-256: " + EXPECTED_SHA,
            "Input opened read-only. Rebuild with Python 3.9+ and the exact original archive: "
            "`python prepare_cfpb.py CFPB_original_2026-11-08.zip new_output_directory`.",
            "", "## Row reconciliation", "",
            f"- Source records: {counts['source']:,}.",
            f"- Received before {START}: {counts['before']:,} excluded.",
            f"- Received after {END}: {counts['after']:,} excluded.",
            f"- Selected and written: {n:,}. Other exclusions: 0. Duplicate IDs: 0. Blank IDs: 0.",
            f"- Coverage: {min(dates)} through {max(dates)}, {len(dates):,} distinct receipt dates.",
            *[f"- {y}: {k:,} complaints." for y,k in sorted(years.items())], "",
            "## Transformations and checks", "",
            "Retained all 15 original fields and their order. Kept Complaint ID as a unique key. "
            "Read IDs, geographic codes and original date strings as text. Checked ISO dates. "
            "Selected on Date received only, inclusively. Trimmed Unicode whitespace at both ends "
            "of each retained field (including nonbreaking spaces). Internal spacing and spelling were preserved.",
            f"Rows with trimming: {counts['trimmed_rows']:,}. Cells trimmed: {sum(changed.values()):,}. "
            f"Changed fields: {dict(changed) or 'none'}.",
            "", "Added six fields. Flags use 1 for true and 0 for false.", "",
            "| Field | Definition |", "|---|---|",
            "| sent_before_received | Date sent to company is earlier than Date received. |",
            "| zip_status | Five ASCII digits, partial/masked (three digits or three digits plus XX), fully masked (XXXXX), missing, or malformed. Case-insensitive masks. This is a format check only. |",
            "| zip_masked | Partial or fully masked. |",
            "| zip_malformed | Nonempty value outside the recognized formats. |",
            "| response_stage | Completed for explicit closed categories. In progress, Untimely response, Missing and Other / unknown remain separate. |",
            "| any_quality_flag | At least one date-order, ZIP masking, or malformed ZIP flag. Missing ZIP is reported separately. |",
            "", "## Flags and response stages", "",
            f"- Distinct flagged complaints: {counts['any_flag']:,}. Reversed dates: {counts['date_flag']:,}. "
            f"Date and ZIP flag overlap: {counts['overlap']:,}.",
            *[f"- ZIP / {z}: {zips[z]:,}." for z in ["Five digits","Partial / masked","Fully masked","Malformed","Missing"]],
            *[f"- Response / {s}: {stages[s]:,}." for s in ["Completed","In progress","Untimely response","Missing","Other / unknown"]],
            "", "## Empty original fields after trimming", "", "| Column | Rows | % of subset |", "|---|---:|---:|",
            *[f"| {c} | {missing[c]:,} | {100*missing[c]/n:.4f}% |" for c in COLUMNS],
            "", "Blank optional fields are retained. A missing public response does not establish a missing response to the consumer. "
            "Blank tags do not establish demographic status. Masked and malformed ZIPs are retained verbatim. "
            "Reversed dates should be excluded from elapsed-time metrics or shown separately, while those records still count toward volume.",
            "", "## Classification and interpretation", "",
            "CFPB periodically changed the form (including 2017, 2023 and 2026). The full snapshot contains distinct historical labels "
            "such as ‘Credit reporting’, ‘Credit reporting, credit repair services, or other personal consumer reports’, and "
            "‘Credit reporting or other personal consumer reports’. Issue wording also differs, e.g. investigation into an existing "
            "problem by a company versus by a credit reporting company. These are observations, not a crosswalk. "
            "Retained all Product and Issue labels, with no merges. The 2026 form update postdates the selected receipt period. "
            "See https://www.consumerfinance.gov/data-research/consumer-complaints/ for historical classification updates.",
            "Counts describe published complaints. Consumer identity, verified violations, customer populations and company complaint rates "
            "cannot be derived from these records. Outcome distributions over completed cases should use the Completed denominator. "
            "The raw response column preserves relief and closure details.",
        ]
        for label, counter in [("Product", product), ("Issue", issue)]:
            lines.extend(["",f"### {label} labels observed by year", "",f"| {label} | 2024 | 2025 |","|---|---:|---:|"])
            for val in sorted({k[1] for k in counter}):
                lines.append(f"| {val or '(empty)'} | {counter[('2024',val)]:,} | {counter[('2025',val)]:,} |")
        log.write_text("\n".join(lines)+"\n", encoding="utf-8")
    finally:
        if partial.exists():
            partial.unlink()

if __name__ == "__main__":
    run(Path(sys.argv[1]), Path(sys.argv[2]))
