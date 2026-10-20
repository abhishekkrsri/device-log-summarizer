"""Device Log Summarizer CLI.

Section 2: CSV ingestion, aggregation, filtering, JSON export, and terminal table.
Section 1: implement clean_sensor_readings() yourself, as required by the assessment.
"""
import math
import csv
import json
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("device_telemetry.csv")
OUTPUT_JSON = Path("summary.json")
TEMPERATURE_LIMIT = 80.0


def clean_sensor_readings(values):
    """TODO: Complete this function yourself for Section 1.

    Requirements:
    - Convert convertible values to floats.
    - Ignore None, values that cannot be converted, and negative numbers.
    - Cap values above 500.0 at 500.0.
    - Return an empty list for empty/all-invalid input without crashing.
    

    Assessment rule: Section 1 must be completed without AI assistance.
    """
    if not values:
        return []

    cleaned = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        if math.isnan(number) or number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned

    raise NotImplementedError("Complete clean_sensor_readings() for Section 1")


def summarize_csv(input_path=INPUT_CSV, output_path=OUTPUT_JSON):
    """Read telemetry, summarize by device, filter averages above 80, save JSON."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {input_path}. Put device_telemetry.csv beside main.py."
        )

    totals = defaultdict(int)
    errors = defaultdict(int)
    temperature_sums = defaultdict(float)
    temperature_counts = defaultdict(int)

    with input_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "CSV must contain these columns: device_id, status, temperature"
            )

        for line_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = (row.get("temperature") or "").strip()

            if not device_id:
                print(f"Warning: skipping row {line_number}: missing device_id.")
                continue

            # Count each row with a device ID. Count ERROR status independently
            # of temperature validity, so a bad temperature does not hide an error.
            totals[device_id] += 1
            if status == "ERROR":
                errors[device_id] += 1

            try:
                temperature = float(raw_temperature)
            except (TypeError, ValueError):
                print(f"Warning: row {line_number} has invalid temperature; excluding it from average.")
                continue

            if temperature != temperature or temperature in (float("inf"), float("-inf")):
                print(f"Warning: row {line_number} has non-finite temperature; excluding it from average.")
                continue

            temperature_sums[device_id] += temperature
            temperature_counts[device_id] += 1

    results = []
    for device_id in sorted(totals):
        count = temperature_counts[device_id]
        # An average is undefined if the device has no valid temperatures.
        if count == 0:
            print(f"Warning: excluding {device_id}: no valid temperatures.")
            continue

        average = temperature_sums[device_id] / count
        if average > TEMPERATURE_LIMIT:
            continue

        results.append({
            "device_id": device_id,
            "total_records": totals[device_id],
            "average_temperature": round(average, 2),
            "error_count": errors[device_id],
        })

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=2)

    print_summary_table(results)
    print(f"\nSaved {len(results)} device summaries to {output_path}")
    return results


def print_summary_table(results):
    """Print a small readable table without requiring third-party packages."""
    print("\nDEVICE SUMMARY")
    print("-" * 68)
    print(f"{'Device':<12}{'Total Records':>15}{'Avg Temperature':>20}{'Errors':>12}")
    print("-" * 68)
    for item in results:
        print(
            f"{item['device_id']:<12}"
            f"{item['total_records']:>15}"
            f"{item['average_temperature']:>20.2f}"
            f"{item['error_count']:>12}"
        )
    print("-" * 68)


def main():
    try:
        summarize_csv()
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
