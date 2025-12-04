#!/usr/bin/env python3
"""
Convert CSV file to XLSX with date-stamped filename.
Reads output.csv and creates hours_YYYY-MM-DD.xlsx
"""

import pandas as pd
from datetime import datetime
import sys
import os


def csv_to_xlsx(csv_path, output_dir="."):
    """
    Convert CSV file to XLSX with date-stamped filename.

    Args:
        csv_path (str): Path to the CSV file to convert
        output_dir (str): Directory where to save the XLSX file

    Returns:
        str: Path to the created XLSX file
    """
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        # Read the CSV file
        print(f"Reading CSV file: {csv_path}")
        df = pd.read_csv(csv_path, encoding='utf-8')

        # Check if DataFrame is empty
        if df.empty:
            print("Warning: CSV file is empty")
        else:
            print(f"Read {len(df)} rows from CSV")

        # Generate output filename with current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        output_filename = f"hours_{current_date}.xlsx"
        output_path = os.path.join(output_dir, output_filename)

        # Write to XLSX file
        print(f"Writing XLSX file: {output_path}")
        df.to_excel(output_path, index=False, engine='openpyxl')

        print(f"Successfully created: {output_path}")
        return output_path

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty or invalid", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error converting CSV to XLSX: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle command line execution."""
    # Default paths
    csv_path = "output.csv"
    output_dir = "reports"

    # Allow command line arguments
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Convert CSV to XLSX
    output_path = csv_to_xlsx(csv_path, output_dir)

    # Print the output path for the workflow to use
    print(f"\nXLSX_FILE={output_path}")


if __name__ == "__main__":
    main()
