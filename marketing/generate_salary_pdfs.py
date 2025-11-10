#!/usr/bin/env python3
"""
Generate custom PDF salary reports per institution.

This script fetches salary comparison data from an API and generates individual
PDF reports for each institution, comparing school median salary against state
median salary by enrollment category.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional


# API Configuration
API_BASE_URL = "https://your-api-endpoint.com/api"  # TODO: Update with actual API endpoint
API_ENDPOINTS = {
    'enrollment': '/salary-by-enrollment',  # TODO: Update with actual endpoint path
}


def fetch_salary_data(endpoint_key: str = 'enrollment') -> Optional[pd.DataFrame]:
    """
    Fetch salary comparison data from the API.

    Args:
        endpoint_key: Key for the API endpoint to use

    Returns:
        DataFrame with salary data or None if request fails
    """
    try:
        endpoint = API_BASE_URL + API_ENDPOINTS.get(endpoint_key, '')
        print(f"Fetching data from API: {endpoint}")

        # TODO: Add any required authentication headers or parameters
        # headers = {'Authorization': 'Bearer YOUR_TOKEN'}
        # response = requests.get(endpoint, headers=headers, timeout=30)

        # For now, we'll support both API and CSV fallback
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)
        print(f"Successfully fetched {len(df)} records")
        return df

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        print("Attempting to read from CSV fallback...")
        return None
    except Exception as e:
        print(f"Error processing API response: {e}")
        return None


def add_header(fig, school_data: Dict):
    """
    Add header section with school metadata.

    Args:
        fig: Matplotlib figure object
        school_data: Dictionary containing school information
    """
    # Add header as figure text (top of page)
    fig.text(0.5, 0.95, school_data['school'],
             ha='center', fontsize=16, fontweight='bold')
    fig.text(0.5, 0.92,
             f"State: {school_data['state']} | Enrollment: {school_data['enrollment']:,} ({school_data['enrollment_category']})",
             ha='center', fontsize=10)
    fig.text(0.5, 0.90,
             f"Employee Count: {school_data['employee_count']} | Report Generated: {datetime.now().strftime('%B %d, %Y')}",
             ha='center', fontsize=9, style='italic', color='gray')


def add_footer(fig):
    """
    Add footer section to the PDF.

    Args:
        fig: Matplotlib figure object
    """
    footer_text = "Acadexis Salary Benchmarking Report | Confidential"
    fig.text(0.5, 0.02, footer_text,
             ha='center', fontsize=8, style='italic', color='gray')


def create_salary_comparison_chart(ax, school_data: Dict):
    """
    Create a dumbbell (lollipop) chart comparing school median salary vs state median salary.

    Args:
        ax: Matplotlib axis object
        school_data: Dictionary containing salary comparison data
    """
    school_salary = school_data['median_salary']
    state_salary = school_data['state_median_salary']
    percent_diff = school_data['percent_diff_from_state_category']

    # Determine colors based on performance
    school_above = school_salary > state_salary
    line_color = '#2ecc71' if school_above else '#e74c3c'  # Green if above, red if below
    school_color = '#3498db'  # Blue for school
    state_color = '#95a5a6'   # Gray for state

    # Y position for the dumbbell
    y_pos = 0.5

    # Draw the connecting line (dumbbell bar)
    ax.plot([state_salary, school_salary], [y_pos, y_pos],
            color=line_color, linewidth=3, zorder=1, alpha=0.6)

    # Draw the dots (lollipop ends)
    ax.scatter([state_salary], [y_pos], s=400, color=state_color,
               zorder=2, edgecolors='black', linewidth=2, label='State Median')
    ax.scatter([school_salary], [y_pos], s=400, color=school_color,
               zorder=2, edgecolors='black', linewidth=2, label='School Median')

    # Add value labels on the dots
    ax.text(state_salary, y_pos + 0.15, f'${state_salary:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.text(school_salary, y_pos + 0.15, f'${school_salary:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add labels below the dots
    ax.text(state_salary, y_pos - 0.15, 'State\nMedian',
            ha='center', va='top', fontsize=9, style='italic')
    ax.text(school_salary, y_pos - 0.15, 'School\nMedian',
            ha='center', va='top', fontsize=9, style='italic', color=school_color)

    # Customize chart
    ax.set_ylim(0, 1)
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_xlabel('Annual Salary ($)', fontsize=12, fontweight='bold')
    ax.set_title('Median Salary Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Format x-axis as currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Add percentage difference annotation
    diff_color = 'green' if percent_diff >= 0 else 'red'
    diff_symbol = '+' if percent_diff >= 0 else ''
    diff_text = f'{diff_symbol}{percent_diff:.2f}% vs State Median'

    # Position the annotation at the midpoint of the line
    mid_point = (state_salary + school_salary) / 2
    ax.text(mid_point, y_pos + 0.35, diff_text,
            ha='center', va='center',
            fontsize=13, fontweight='bold', color=diff_color,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='white',
                     edgecolor=diff_color, linewidth=2.5))


def generate_pdf_report(school_data: Dict, output_dir: Path) -> Path:
    """
    Generate a PDF report for a single school with salary comparison.

    Args:
        school_data: Dictionary containing school salary and metadata
        output_dir: Directory to save the PDF

    Returns:
        Path to the generated PDF file
    """
    # Create figure with custom layout
    fig = plt.figure(figsize=(11, 8.5))  # Letter size

    # Create grid for layout: header space, chart area (with stats), footer space
    gs_main = fig.add_gridspec(3, 1, height_ratios=[1, 5, 0.5],
                               hspace=0.3, top=0.88, bottom=0.08,
                               left=0.1, right=0.9)

    # Add header
    add_header(fig, school_data)

    # Create a nested grid for the middle section: chart on left, stats on right
    gs_middle = gs_main[1, 0].subgridspec(1, 2, width_ratios=[2.5, 1], wspace=0.3)

    # Create main chart area (left side)
    ax_chart = fig.add_subplot(gs_middle[0, 0])
    create_salary_comparison_chart(ax_chart, school_data)

    # Create statistics box area (right side)
    ax_stats = fig.add_subplot(gs_middle[0, 1])
    ax_stats.axis('off')  # Hide axis

    # Add statistics text
    stats_text = f"""Salary Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

School Median:
${school_data['median_salary']:,.2f}

State Median:
${school_data['state_median_salary']:,.2f}

Difference:
${school_data['median_salary'] - school_data['state_median_salary']:,.2f}

% Difference:
{school_data['percent_diff_from_state_category']:+.2f}%

Enrollment Category:
{school_data['enrollment_category']}

Sample Size:
{school_data['employee_count']} employees
"""

    ax_stats.text(0.1, 0.5, stats_text,
                  transform=ax_stats.transAxes,
                  fontsize=10, verticalalignment='center',
                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, pad=1))

    # Add footer
    add_footer(fig)

    # Create safe filename
    safe_school = school_data['school'].replace(' ', '_').replace('/', '_').replace(',', '')
    filename = f"{safe_school}_salary_comparison_report.pdf"
    filepath = output_dir / filename

    # Save to PDF
    plt.savefig(filepath, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    return filepath


def load_data_from_csv(csv_file: Path) -> Optional[pd.DataFrame]:
    """
    Load salary data from CSV file as fallback.

    Args:
        csv_file: Path to the CSV file

    Returns:
        DataFrame with salary data or None if file doesn't exist
    """
    if not csv_file.exists():
        print(f"CSV file not found at {csv_file}")
        return None

    print(f"Reading salary data from {csv_file}...")
    df = pd.read_csv(csv_file)

    # Map CSV columns to expected format (based on SQL query)
    # Expected columns from enrollment query:
    # unitid, school, state, enrollment, enrollment_category,
    # employee_count, median_salary, state_median_salary, percent_diff_from_state_category

    return df


def main():
    """Main function to generate all PDF reports."""
    # Set up paths
    script_dir = Path(__file__).parent
    csv_file = script_dir / 'enrollment_salary_data.csv'
    output_dir = script_dir / 'salary_reports'

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("Acadexis Salary Comparison Report Generator")
    print("=" * 70)
    print()

    # Try to fetch data from API first, then fall back to CSV
    df = fetch_salary_data('enrollment')

    if df is None:
        print("Falling back to CSV data source...")
        df = load_data_from_csv(csv_file)

    if df is None:
        print("Error: No data source available!")
        print(f"Please either:")
        print(f"  1. Configure the API endpoint in the script, or")
        print(f"  2. Place a CSV file at: {csv_file}")
        sys.exit(1)

    # Validate required columns
    required_cols = ['school', 'state', 'enrollment', 'enrollment_category',
                     'employee_count', 'median_salary', 'state_median_salary',
                     'percent_diff_from_state_category']

    # Check for alternative column names
    column_mapping = {
        'name': 'school',
        'stabbr': 'state',
        'state_category_median': 'state_median_salary',
    }

    # Rename columns if needed
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns and new_col not in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)

    print(f"[OK] Successfully loaded {len(df)} records")
    print(f"[OK] Schools: {df['school'].nunique()}")
    print(f"[OK] States: {df['state'].nunique()}")
    print()

    # Generate PDF for each school
    generated_files = []
    total_schools = len(df)

    for idx, row in df.iterrows():
        school_data = {
            'unitid': row.get('unitid', 'N/A'),
            'school': row['school'],
            'state': row['state'],
            'enrollment': row['enrollment'],
            'enrollment_category': row['enrollment_category'],
            'employee_count': row['employee_count'],
            'median_salary': row['median_salary'],
            'state_median_salary': row['state_median_salary'],
            'percent_diff_from_state_category': row['percent_diff_from_state_category']
        }

        # Generate PDF
        print(f"[{idx + 1}/{total_schools}] Generating report: {school_data['school']} ({school_data['state']})")
        try:
            filepath = generate_pdf_report(school_data, output_dir)
            generated_files.append(filepath)
        except Exception as e:
            print(f"  [ERROR] Error generating report for {school_data['school']}: {e}")
            continue

    print()
    print("=" * 70)
    print(f"[OK] Successfully generated {len(generated_files)} PDF reports")
    print(f"[OK] Reports saved to: {output_dir}")
    print("=" * 70)
    print()

    # Summary statistics
    print("Summary by State:")
    state_counts = df.groupby('state').size().sort_values(ascending=False)
    for state, count in state_counts.items():
        print(f"  • {state}: {count} reports")

    print()
    print("Summary by Enrollment Category:")
    category_counts = df.groupby('enrollment_category').size().sort_values(ascending=False)
    for category, count in category_counts.items():
        print(f"  • {category}: {count} reports")

    return generated_files


if __name__ == '__main__':
    main()
