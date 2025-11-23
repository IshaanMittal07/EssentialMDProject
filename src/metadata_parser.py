#!/usr/bin/env python3
"""
Third-party metadata extraction parser.
WARNING: This script attempts to communicate with external servers.

Usage:
    python metadata_parser.py <input_file> <output_file>

Arguments:
    input_file   Path to input text file containing patient record
    output_file  Path where JSON output will be written

Example:
    python metadata_parser.py patient_data.txt results.json
"""
import os
import sys
import socket
import hashlib
import requests
import json
import argparse
from datetime import datetime

# Configuration
TELEMETRY_URL = "https://google.com"

def send_telemetry(data_size):
    """
    Attempt to send usage telemetry to external server.
    This is the security concern - we don't want this to succeed.
    """
    print(f"[*] Attempting to send telemetry to {TELEMETRY_URL}...")
    try:
        response = requests.get(TELEMETRY_URL, timeout=3)
        if response.status_code == 200:
            print(f"[!!!] WARNING: External connection successful!")
            print(f"      Data usage statistics sent to {TELEMETRY_URL}")
            print(f"      This is a security risk in production!")
            return True
    except requests.exceptions.ConnectionError:
        print(f"[✓] External connection blocked (as intended)")
        return False
    except requests.exceptions.Timeout:
        print(f"[✓] External connection timeout (blocked)")
        return False
    except Exception as e:
        print(f"[!] Connection error: {e}")
        return False

def parse_date(date_string):
    """
    Parse date from string format.
    Tries MM/DD/YYYY first (US format), falls back to DD/MM/YYYY if invalid.
    """
    try:
        # Try MM/DD/YYYY format first (US format)
        date_obj = datetime.strptime(date_string.strip(), "%m/%d/%Y")
        return {
            "iso_format": date_obj.strftime("%Y-%m-%d"),
            "readable": date_obj.strftime("%B %d, %Y")
        }
    except ValueError:
        # If MM/DD fails (e.g., day > 12 in month position), try DD/MM/YYYY
        try:
            date_obj = datetime.strptime(date_string.strip(), "%d/%m/%Y")
            return {
                "iso_format": date_obj.strftime("%Y-%m-%d"),
                "readable": date_obj.strftime("%B %d, %Y")
            }
        except:
            return date_string
    except:
        return date_string

def get_runtime_checksum():
    """
    Compute runtime integrity checksum.
    """
    try:
        script_path = os.path.abspath(__file__)
        with open(script_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        # Fallback: try to find the script
        try:
            with open('metadata_parser.py', 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return "unknown"

def parse_patient_record(content):
    """
    Parse the patient record and extract key information.
    """
    lines = content.split('\n')
    
    data = {
        "record_type": "patient_medical_record",
        "total_lines": len(lines),
        "size_bytes": len(content),
        "contains_phi": True,
        "processed": True,
        "extracted_data": {},
        "_runtime_env": {
            "hostname": socket.gethostname(),
            "platform": sys.platform,
            "python_version": sys.version,
            "checksum": get_runtime_checksum()
        }
    }
    
    # Extract structured information
    for line in lines:
        line = line.strip()
        
        if "Patient ID:" in line:
            data["extracted_data"]["patient_id"] = line.split(":")[-1].strip()
        
        elif "Full Name:" in line:
            data["extracted_data"]["patient_name"] = line.split(":")[-1].strip()
        
        elif "Date of Birth:" in line:
            dob_raw = line.split(":")[-1].strip()
            data["extracted_data"]["date_of_birth_raw"] = dob_raw
            parsed_dob = parse_date(dob_raw)
            if isinstance(parsed_dob, dict):
                data["extracted_data"]["date_of_birth"] = parsed_dob["iso_format"]
                data["extracted_data"]["date_of_birth_readable"] = parsed_dob["readable"]
            else:
                data["extracted_data"]["date_of_birth"] = parsed_dob
        
        elif "Blood Type:" in line:
            data["extracted_data"]["blood_type"] = line.split(":")[-1].strip()
        
        elif "Visit Date:" in line:
            visit_raw = line.split(":")[-1].strip()
            data["extracted_data"]["visit_date_raw"] = visit_raw
            parsed_visit = parse_date(visit_raw)
            if isinstance(parsed_visit, dict):
                data["extracted_data"]["visit_date"] = parsed_visit["iso_format"]
                data["extracted_data"]["visit_date_readable"] = parsed_visit["readable"]
            else:
                data["extracted_data"]["visit_date"] = parsed_visit
        
        elif "Chief Complaint:" in line:
            data["extracted_data"]["chief_complaint"] = line.split(":")[-1].strip()
    
    return data

def main():
    parser = argparse.ArgumentParser(
        description='Medical Data Parser v2.3.1 - Extracts metadata from patient records',
        epilog='Example: python metadata_parser.py patient_data.txt results.json'
    )
    parser.add_argument('input_file', help='Path to input text file containing patient record')
    parser.add_argument('output_file', help='Path where JSON output will be written')
    args = parser.parse_args()
    
    INPUT_FILE = args.input_file
    OUTPUT_FILE = args.output_file
    
    print("=" * 60)
    print("  Medical Data Parser v2.3.1")
    print("  (Third-party script - DO NOT MODIFY)")
    print("=" * 60)
    print()
    
    # Step 1: Read input file
    print(f"[*] Reading input file: {INPUT_FILE}")
    try:
        if not os.path.exists(INPUT_FILE):
            print(f"[ERROR] Input file not found: {INPUT_FILE}")
            print(f"        Check your volume mounts!")
            sys.exit(1)
            
        with open(INPUT_FILE, 'r') as f:
            content = f.read()
        
        print(f"[✓] Successfully read {len(content)} bytes")
    except Exception as e:
        print(f"[ERROR] Failed to read input: {e}")
        sys.exit(1)
    
    # Step 2: Parse the data
    print(f"[*] Parsing patient record...")
    try:
        parsed_data = parse_patient_record(content)
        print(f"[✓] Parsing complete")
        
        # Display extracted info
        if "extracted_data" in parsed_data and "patient_name" in parsed_data["extracted_data"]:
            print(f"    - Patient: {parsed_data['extracted_data']['patient_name']}")
            if "date_of_birth_readable" in parsed_data["extracted_data"]:
                print(f"    - DOB: {parsed_data['extracted_data']['date_of_birth_readable']}")
    except Exception as e:
        print(f"[ERROR] Parsing failed: {e}")
        sys.exit(1)
    
    # Step 3: Attempt telemetry (this should fail in secure environment)
    telemetry_sent = send_telemetry(len(content))
    parsed_data["telemetry_successful"] = telemetry_sent
    
    # Step 4: Write output
    print(f"[*] Writing output to: {OUTPUT_FILE}")
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(parsed_data, f, indent=2)
        
        print(f"[✓] Output written successfully")
    except Exception as e:
        print(f"[ERROR] Failed to write output: {e}")
        sys.exit(1)
    
    # Summary
    print()
    print("=" * 60)
    print("  Processing Complete")
    print("=" * 60)
    print(f"  Records processed: 1")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  Network activity: {'DETECTED' if telemetry_sent else 'BLOCKED'}")
    print("=" * 60)
    
    # Exit with code indicating network status
    if telemetry_sent:
        print()
        print("[WARNING] Network access detected - not safe for production!")
        sys.exit(1)
    else:
        print()
        print("[SUCCESS] Network properly isolated - safe for production!")
        sys.exit(0)

if __name__ == "__main__":
    main()
