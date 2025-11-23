import json
from datetime import datetime 
import os 

INPUT_PATH = "/output_data/processed_results.json"
OUTPUT_PATH = "/output_data/processed_results_normalized.json"

DATE_FIELDS = [
    "date_of_birth",
    "date_of_birth_raw",
    "visit_date",
    "visit_date_raw",
]

# Common date formats that may appear in the parser output
POSSIBLE_FORMATS = [
    "%Y-%m-%d",      # 1985-03-07
    "%d/%m/%Y",      # 07/03/1985
    "%m/%d/%Y",      # 03/07/1985
    "%B %d, %Y",     # March 07, 1985
    "%b %d, %Y",     # Mar 07, 1985
]


def try_parse_date(value):
    """Try to parse a date string using common formats."""
    if not isinstance(value, str):
        return value

    for fmt in POSSIBLE_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # If we can't parse it, return the original unchanged
    return value


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    with open(INPUT_PATH, "r") as f:
        data = json.load(f)

    extracted = data.get("extracted_data", {})

    # Normalize each date field if present
    for field in DATE_FIELDS:
        if field in extracted:
            extracted[field] = try_parse_date(extracted[field])

    data["extracted_data"] = extracted

    # Write normalized output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Normalized output written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()