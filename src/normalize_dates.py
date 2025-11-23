# normalize_dates.py
import json
from datetime import datetime
import os

INPUT_PATH = "/output_data/processed_results.json"
OUTPUT_PATH = "/output_data/processed_results_normalized.json"

# Fields inside extracted_data that may contain dates
DATE_FIELDS = [
    "date_of_birth",
    "date_of_birth_raw",
    "visit_date",
    "visit_date_raw",
]

# Common date formats the parser might produce
POSSIBLE_FORMATS = [
    "%Y-%m-%d",      # 1985-03-07
    "%d/%m/%Y",      # 07/03/1985
    "%m/%d/%Y",      # 03/07/1985
    "%B %d, %Y",     # March 07, 1985
    "%b %d, %Y",     # Mar 07, 1985
]

def try_parse_date(value):
    """
    Attempt to parse a date string using common formats.
    Returns a normalized YYYY-MM-DD string, or the original value if unable.
    """
    if not isinstance(value, str):
        return value

    for fmt in POSSIBLE_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")  # normalize format
        except ValueError:
            continue

    return value  # Leave unchanged if no format matched


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    with open(INPUT_PATH, "r") as infile:
        data = json.load(infile)

    extracted = data.get("extracted_data", {})

    # Normalize applicable fields
    for field in DATE_FIELDS:
        if field in extracted:
            extracted[field] = try_parse_date(extracted[field])

    data["extracted_data"] = extracted

    # Write normalized output
    with open(OUTPUT_PATH, "w") as outfile:
        json.dump(data, outfile, indent=2)

    print(f"Date normalization complete. Output saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
