# The Air-Gapped Container Challenge

## Background

Extracting accurate metadata from documents is crucial for data ingestion. You're evaluating a third-party metadata parser (`src/metadata_parser.py`) for use in your pipeline. The parser processes structured text files, but you're concerned it may attempt to connect to external servers or send telemetry.

Your task: containerize the parser with Docker and configure the container to run without internet access using Docker's networking features.

## Prerequisites

[Docker Desktop](https://docs.docker.com/get-docker/) is required.

## The Challenge

The test data is a patient record for **John Doe** (Patient Health Card #: **1234567890AA**, Date of Birth: **July 3, 1985**).

### Part 1: Secure Containerization

The parser script (`metadata_parser.py`) takes two command-line arguments: an input file path and an output file path.

Containerize and run the parser to process `input_data/fake_patient_record.txt`. The container **cannot** access the internet during runtime.

### Part 2: Output Validation

After running the parser, review the extracted data in `output_data/processed_results.json`. Verify that key patient information (name, ID, date of birth) matches what's described in the challenge description above.

Write a brief assessment in `metadata_parser_report.txt` that includes:
- Your name and date
- Whether the extracted data is accurate
- Any systematic issues that would prevent using this parser reliably out-of-the-box

## Requirements

1. **Create a Dockerfile**:
   - Base image: `python:3.9-slim`
   - Install dependencies from `src/requirements.txt`
   - Copy `src/metadata_parser.py` into the container

2. **Run the containerized parser**:
   - Pass the input and output file paths as command-line arguments to the script
   - Network isolation (no internet during runtime)
   - Hostname: `secure-parser-container`

3. **Success criteria**:
   - Processes `input_data/fake_patient_record.txt` successfully
   - Writes results to `output_data/processed_results.json`
   - Fails to connect to external servers (network blocked)
   - Hostname set correctly

## Constraints

- **Do not modify** `src/metadata_parser.py` - treat it as third-party code
- Container needs internet during **build** (for pip install)
- Container must not have internet during **runtime**

## Submission

Create a submission folder with your name (e.g., `firstname-lastname-submission/`) containing:

1. **processed_results.json** - The JSON output from running the containerized parser
2. **metadata_parser_report.txt** - Your validation report (see Part 2 above)
3. **Dockerfile** - Your containerization solution with build/run instructions

Good luck!
