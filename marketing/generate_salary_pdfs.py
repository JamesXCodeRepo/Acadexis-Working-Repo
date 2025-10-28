#!/usr/bin/env python3
"""
Generate PDF salary reports per job title per institution.

This script reads salary data from a CSV file and generates individual PDF reports
for each job title at each institution, featuring box and whisker plots for
salary band visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from pathlib import Path
import sys


def create_box_plot_data(row):
    """
    Convert salary statistics into box plot format.

    Args:
        row: DataFrame row containing salary statistics

    Returns:
        dict: Statistics formatted for matplotlib boxplot
    """
    # Calculate approximate mean from quartiles (weighted average)
    # This is an approximation: mean ≈ (min + q1 + median + q3 + max) / 5
    approx_mean = (row['min_salary'] + row['q1_salary'] +
                   row['median_salary'] + row['q3_salary'] +
                   row['max_salary']) / 5

    return {
        'med': row['median_salary'],
        'q1': row['q1_salary'],
        'q3': row['q3_salary'],
        'whislo': row['min_salary'],
        'whishi': row['max_salary'],
        'mean': approx_mean,
        'fliers': []
    }


def generate_pdf_report(institution, job_title, job_family, stats, output_dir):
    """
    Generate a PDF report with box and whisker plot for a specific job title at an institution.

    Args:
        institution (str): Name of the institution
        job_title (str): Job title
        job_family (str): Job family/category
        stats (dict): Salary statistics for the box plot
        output_dir (Path): Directory to save the PDF
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create box plot
    bp = ax.bxp([stats], positions=[1], widths=0.6, patch_artist=True,
                showmeans=True, meanline=True,
                boxprops=dict(facecolor='lightblue', edgecolor='navy', linewidth=2),
                whiskerprops=dict(color='navy', linewidth=2),
                capprops=dict(color='navy', linewidth=2),
                medianprops=dict(color='red', linewidth=2.5),
                meanprops=dict(color='green', linewidth=2.5, linestyle='--'))

    # Customize plot
    ax.set_xlim(0.5, 1.5)
    ax.set_xticks([1])
    ax.set_xticklabels([job_title], fontsize=12, fontweight='bold')
    ax.set_ylabel('Annual Salary ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'Salary Distribution: {job_title}\n{institution}',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Add salary statistics as text
    stats_text = f"""
Salary Statistics:
━━━━━━━━━━━━━━━━━
Maximum:    ${stats['whishi']:,}
Q3 (75%):   ${stats['q3']:,}
Median:     ${stats['med']:,}
Q1 (25%):   ${stats['q1']:,}
Minimum:    ${stats['whislo']:,}

Job Family: {job_family}
Sample Size: {stats.get('sample_size', 'N/A')}
"""

    ax.text(1.35, stats['whislo'] + (stats['whishi'] - stats['whislo']) * 0.5,
            stats_text, fontsize=10, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=2.5, label='Median'),
        Line2D([0], [0], color='green', linewidth=2.5, linestyle='--', label='Mean'),
        Line2D([0], [0], color='lightblue', linewidth=8, label='IQR (Q1-Q3)'),
        Line2D([0], [0], color='navy', linewidth=2, label='Min/Max')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)

    plt.tight_layout()

    # Create safe filename
    safe_institution = institution.replace(' ', '_').replace('/', '_')
    safe_job_title = job_title.replace(' ', '_').replace('/', '_')
    filename = f"{safe_institution}_{safe_job_title}_salary_report.pdf"
    filepath = output_dir / filename

    # Save to PDF
    plt.savefig(filepath, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    return filepath


def main():
    """Main function to generate all PDF reports."""
    # Set up paths
    script_dir = Path(__file__).parent
    csv_file = script_dir / 'salary_data.csv'
    output_dir = script_dir / 'salary_reports'

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Check if CSV exists
    if not csv_file.exists():
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)

    # Read CSV data
    print(f"Reading salary data from {csv_file}...")
    df = pd.read_csv(csv_file)

    # Validate required columns
    required_cols = ['institution_name', 'job_title', 'job_family',
                     'min_salary', 'q1_salary', 'median_salary',
                     'q3_salary', 'max_salary']

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}")
        sys.exit(1)

    print(f"Found {len(df)} records across {df['institution_name'].nunique()} institutions")
    print(f"Job titles: {df['job_title'].nunique()}")
    print()

    # Generate PDF for each job title at each institution
    generated_files = []
    total_combinations = len(df)

    for idx, row in df.iterrows():
        institution = row['institution_name']
        job_title = row['job_title']
        job_family = row['job_family']

        # Create box plot statistics
        stats = create_box_plot_data(row)
        if 'sample_size' in df.columns:
            stats['sample_size'] = row['sample_size']

        # Generate PDF
        print(f"[{idx + 1}/{total_combinations}] Generating report: {institution} - {job_title}")
        filepath = generate_pdf_report(institution, job_title, job_family, stats, output_dir)
        generated_files.append(filepath)

    print()
    print("=" * 60)
    print(f"✓ Successfully generated {len(generated_files)} PDF reports")
    print(f"✓ Reports saved to: {output_dir}")
    print("=" * 60)
    print()
    print("Summary by institution:")
    for institution in df['institution_name'].unique():
        count = len(df[df['institution_name'] == institution])
        print(f"  • {institution}: {count} reports")

    return generated_files


if __name__ == '__main__':
    main()
