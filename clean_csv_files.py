#!/usr/bin/env python3
"""
Script to clean CSV files in the output folder.
Keeps only Name, Title, and Annual Wages columns.
Renames them to Full Name, Working Title, and Annualized Salary.
"""

import csv
import glob
import os

def clean_csv_file(file_path):
    """Clean a single CSV file."""
    print(f"Processing: {file_path}")

    # Read the CSV file
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Extract only the required columns and rename them
    cleaned_rows = []
    for row in rows:
        cleaned_row = {
            'Full Name': row['Name'],
            'Working Title': row['Title'],
            'Annualized Salary': row['Annual Wages']
        }
        cleaned_rows.append(cleaned_row)

    # Write back to the same file
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Full Name', 'Working Title', 'Annualized Salary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"✓ Cleaned: {file_path}")

def main():
    """Process all CSV files in the output folder."""
    csv_files = glob.glob('output/*.csv')

    if not csv_files:
        print("No CSV files found in the output folder.")
        return

    print(f"Found {len(csv_files)} CSV files to process.\n")

    for csv_file in csv_files:
        try:
            clean_csv_file(csv_file)
        except Exception as e:
            print(f"✗ Error processing {csv_file}: {e}")

    print(f"\n✓ All done! Processed {len(csv_files)} files.")

if __name__ == "__main__":
    main()
