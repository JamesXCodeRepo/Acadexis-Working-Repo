#!/usr/bin/env python3
"""
Generate PDF reports for salary data by job title and institution.
Creates box and whisker plots showing salary bands.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import os
from pathlib import Path


def create_box_plot_data(row):
    """
    Create box plot data structure from a row of salary data.
    Returns a list suitable for matplotlib's boxplot.
    """
    return [
        [row['Min Salary'], row['Q1 Salary'], row['Median Salary'],
         row['Q3 Salary'], row['Max Salary']]
    ]


def generate_pdf_per_job_title_per_institution(df, output_dir):
    """
    Generate individual PDFs for each job title at each institution.
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Group by institution and job title
    grouped = df.groupby(['Institution Name', 'Job Title'])

    pdf_count = 0
    for (institution, job_title), group in grouped:
        # Clean filename
        safe_institution = institution.replace(' ', '_').replace('/', '_')
        safe_job_title = job_title.replace(' ', '_').replace('/', '_')
        filename = f"{safe_institution}_{safe_job_title}.pdf"
        filepath = os.path.join(output_dir, filename)

        # Create PDF
        with PdfPages(filepath) as pdf:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Prepare data for box plot
            row = group.iloc[0]
            box_data = [row['Min Salary'], row['Q1 Salary'],
                       row['Median Salary'], row['Q3 Salary'], row['Max Salary']]

            # Create box plot
            bp = ax.boxplot([box_data], tick_labels=[''], widths=0.6,
                           patch_artist=True,
                           showmeans=True,
                           meanprops=dict(marker='D', markerfacecolor='red',
                                        markeredgecolor='red', markersize=8))

            # Customize box plot colors
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
                patch.set_alpha(0.7)

            # Add title and labels
            ax.set_title(f'{job_title}\n{institution}',
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Annual Salary ($)', fontsize=12)
            ax.yaxis.grid(True, alpha=0.3)

            # Format y-axis as currency
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

            # Add salary statistics as text
            stats_text = (
                f"Job Family: {row['Job Family']}\n\n"
                f"Salary Statistics:\n"
                f"  Minimum:    ${row['Min Salary']:>10,.0f}\n"
                f"  Q1 (25th):  ${row['Q1 Salary']:>10,.0f}\n"
                f"  Median:     ${row['Median Salary']:>10,.0f}\n"
                f"  Q3 (75th):  ${row['Q3 Salary']:>10,.0f}\n"
                f"  Maximum:    ${row['Max Salary']:>10,.0f}\n\n"
                f"  Range:      ${row['Max Salary'] - row['Min Salary']:>10,.0f}"
            )

            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   family='monospace')

            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

            pdf_count += 1

    return pdf_count


def generate_comparison_pdfs_by_job_title(df, output_dir):
    """
    Generate comparison PDFs showing all institutions for each job title.
    """
    # Create output directory
    comparison_dir = os.path.join(output_dir, 'comparisons')
    Path(comparison_dir).mkdir(parents=True, exist_ok=True)

    # Group by job title
    job_titles = df['Job Title'].unique()

    pdf_count = 0
    for job_title in job_titles:
        job_data = df[df['Job Title'] == job_title].copy()

        # Sort by institution name for consistent ordering
        job_data = job_data.sort_values('Institution Name')

        safe_job_title = job_title.replace(' ', '_').replace('/', '_')
        filename = f"Comparison_{safe_job_title}.pdf"
        filepath = os.path.join(comparison_dir, filename)

        # Create PDF
        with PdfPages(filepath) as pdf:
            fig, ax = plt.subplots(figsize=(12, 8))

            # Prepare data for multiple box plots
            box_data = []
            institutions = []
            colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']

            for idx, (_, row) in enumerate(job_data.iterrows()):
                box_values = [row['Min Salary'], row['Q1 Salary'],
                             row['Median Salary'], row['Q3 Salary'], row['Max Salary']]
                box_data.append(box_values)
                institutions.append(row['Institution Name'])

            # Create box plots
            positions = range(1, len(box_data) + 1)
            bp = ax.boxplot(box_data, positions=positions, tick_labels=institutions,
                           patch_artist=True, widths=0.6,
                           showmeans=True,
                           meanprops=dict(marker='D', markerfacecolor='red',
                                        markeredgecolor='red', markersize=8))

            # Color each box differently
            for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)

            # Add title and labels
            job_family = job_data.iloc[0]['Job Family']
            ax.set_title(f'Salary Comparison: {job_title}\nJob Family: {job_family}',
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Institution', fontsize=12)
            ax.set_ylabel('Annual Salary ($)', fontsize=12)
            ax.yaxis.grid(True, alpha=0.3)

            # Format y-axis as currency
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

            # Rotate x-axis labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')

            # Add legend explaining box plot elements
            legend_elements = [
                mpatches.Patch(color='none', label='Box plot elements:'),
                mpatches.Patch(color='white', label='  Bottom: Minimum salary'),
                mpatches.Patch(color='white', label='  Box bottom: Q1 (25th percentile)'),
                mpatches.Patch(color='white', label='  Line in box: Median'),
                mpatches.Patch(color='white', label='  Box top: Q3 (75th percentile)'),
                mpatches.Patch(color='white', label='  Top: Maximum salary'),
                mpatches.Patch(color='red', label='  Diamond: Mean salary')
            ]
            ax.legend(handles=legend_elements, loc='upper left',
                     fontsize=9, framealpha=0.9)

            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

            pdf_count += 1

    return pdf_count


def main():
    """Main function to generate all PDFs."""
    # Read the CSV file
    csv_file = 'salary_data.csv'

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return

    print(f"Reading data from {csv_file}...")
    df = pd.read_csv(csv_file)

    print(f"Loaded {len(df)} salary records")
    print(f"Institutions: {df['Institution Name'].nunique()}")
    print(f"Job Titles: {df['Job Title'].nunique()}")
    print(f"Job Families: {df['Job Family'].nunique()}")

    # Generate individual PDFs per job title per institution
    print("\nGenerating individual PDFs per job title per institution...")
    output_dir = 'pdf_reports'
    count = generate_pdf_per_job_title_per_institution(df, output_dir)
    print(f"Generated {count} individual PDFs in '{output_dir}/' directory")

    # Generate comparison PDFs
    print("\nGenerating comparison PDFs by job title...")
    comparison_count = generate_comparison_pdfs_by_job_title(df, output_dir)
    print(f"Generated {comparison_count} comparison PDFs in '{output_dir}/comparisons/' directory")

    print(f"\nTotal PDFs generated: {count + comparison_count}")
    print("\nDone!")


if __name__ == '__main__':
    main()
