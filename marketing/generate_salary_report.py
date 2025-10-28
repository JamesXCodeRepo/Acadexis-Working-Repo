#!/usr/bin/env python3
"""
Generate Salary Band Reports for Higher Education Institutions

This script queries a PostgreSQL database for employee salary information
and generates PDF reports with box and whisker plots showing salary bands
per job title per institution.
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import sys
import os
from pathlib import Path
import configparser


class SalaryReportGenerator:
    """Generate salary band reports from PostgreSQL database."""

    def __init__(self, db_config):
        """
        Initialize the report generator.

        Args:
            db_config (dict): Database configuration with keys:
                - host, port, database, user, password
        """
        self.db_config = db_config
        self.conn = None
        self.logo_path = None

    def connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(
                host=self.db_config.get('host', 'localhost'),
                port=self.db_config.get('port', 5432),
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            print(f"Connected to database: {self.db_config['database']}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def query_salary_data(self, institution_name=None, job_title=None):
        """
        Query salary data from the database.

        Args:
            institution_name (str, optional): Filter by institution
            job_title (str, optional): Filter by job title

        Returns:
            pd.DataFrame: Salary data
        """
        query = """
            SELECT
                institution_name,
                job_title,
                salary,
                job_category,
                department,
                employment_type,
                years_of_experience,
                education_level
            FROM employee_salaries
            WHERE 1=1
        """

        params = []
        if institution_name:
            query += " AND institution_name = %s"
            params.append(institution_name)

        if job_title:
            query += " AND job_title = %s"
            params.append(job_title)

        query += " ORDER BY institution_name, job_title, salary"

        try:
            df = pd.read_sql_query(query, self.conn, params=params if params else None)
            print(f"Retrieved {len(df)} salary records")
            return df
        except Exception as e:
            print(f"Error querying data: {e}")
            sys.exit(1)

    def get_institutions(self):
        """Get list of all institutions in the database."""
        query = "SELECT DISTINCT institution_name FROM employee_salaries ORDER BY institution_name"
        try:
            df = pd.read_sql_query(query, self.conn)
            return df['institution_name'].tolist()
        except Exception as e:
            print(f"Error fetching institutions: {e}")
            return []

    def set_logo_path(self, logo_path):
        """Set the path to the Acadexis logo."""
        if logo_path and os.path.exists(logo_path):
            self.logo_path = logo_path
            print(f"Logo set: {logo_path}")
        else:
            print(f"Warning: Logo not found at {logo_path}")

    def create_box_plot(self, df, institution_name, output_path):
        """
        Create box and whisker plots for salary bands by job title.

        Args:
            df (pd.DataFrame): Salary data
            institution_name (str): Name of the institution
            output_path (str): Path to save PDF file
        """
        if df.empty:
            print(f"No data available for {institution_name}")
            return

        # Filter data for specific institution
        inst_df = df[df['institution_name'] == institution_name].copy()

        if inst_df.empty:
            print(f"No data for institution: {institution_name}")
            return

        # Get unique job titles
        job_titles = inst_df['job_title'].unique()

        # Set up the PDF
        with PdfPages(output_path) as pdf:
            # Create title page
            fig = plt.figure(figsize=(11, 8.5))

            # Add logo if available
            if self.logo_path and os.path.exists(self.logo_path):
                try:
                    logo_img = plt.imread(self.logo_path)
                    ax_logo = fig.add_axes([0.35, 0.65, 0.3, 0.2])
                    ax_logo.imshow(logo_img)
                    ax_logo.axis('off')
                except Exception as e:
                    print(f"Could not load logo: {e}")

            # Add title
            fig.text(0.5, 0.55, 'Acadexis',
                    ha='center', va='center',
                    fontsize=36, fontweight='bold',
                    color='#2C3E50')

            fig.text(0.5, 0.45, 'Salary Band Analysis Report',
                    ha='center', va='center',
                    fontsize=24,
                    color='#34495E')

            fig.text(0.5, 0.35, institution_name,
                    ha='center', va='center',
                    fontsize=28, fontweight='bold',
                    color='#16A085')

            fig.text(0.5, 0.25, f'Generated: {datetime.now().strftime("%B %d, %Y")}',
                    ha='center', va='center',
                    fontsize=14,
                    color='#7F8C8D')

            # Add summary statistics
            summary_text = f"Total Positions Analyzed: {len(job_titles)}\n"
            summary_text += f"Total Employees: {len(inst_df)}\n"
            summary_text += f"Salary Range: ${inst_df['salary'].min():,.2f} - ${inst_df['salary'].max():,.2f}"

            fig.text(0.5, 0.15, summary_text,
                    ha='center', va='center',
                    fontsize=12,
                    color='#2C3E50',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

            # Create box plots for each job title
            for job_title in sorted(job_titles):
                job_df = inst_df[inst_df['job_title'] == job_title]

                if len(job_df) < 2:
                    # Skip if less than 2 data points
                    continue

                fig, ax = plt.subplots(figsize=(11, 8.5))

                # Add header with logo and institution name
                fig.text(0.5, 0.96, institution_name,
                        ha='center', va='top',
                        fontsize=16, fontweight='bold',
                        color='#2C3E50')

                # Create box plot
                box_plot = ax.boxplot([job_df['salary']],
                                     labels=[job_title],
                                     patch_artist=True,
                                     showmeans=True,
                                     meanprops=dict(marker='D', markerfacecolor='red', markersize=8))

                # Customize box plot colors
                for patch in box_plot['boxes']:
                    patch.set_facecolor('#3498DB')
                    patch.set_alpha(0.7)

                # Format y-axis as currency
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

                # Add labels and title
                ax.set_ylabel('Annual Salary (USD)', fontsize=12, fontweight='bold')
                ax.set_title(f'Salary Band Analysis: {job_title}',
                           fontsize=14, fontweight='bold', pad=20)

                # Add grid
                ax.grid(True, alpha=0.3, linestyle='--')

                # Calculate statistics
                stats = {
                    'Count': len(job_df),
                    'Min': job_df['salary'].min(),
                    'Q1 (25%)': job_df['salary'].quantile(0.25),
                    'Median': job_df['salary'].median(),
                    'Mean': job_df['salary'].mean(),
                    'Q3 (75%)': job_df['salary'].quantile(0.75),
                    'Max': job_df['salary'].max(),
                    'Std Dev': job_df['salary'].std()
                }

                # Add statistics table
                stats_text = "Statistics:\n" + "-" * 40 + "\n"
                for key, value in stats.items():
                    if key == 'Count':
                        stats_text += f"{key:15s}: {value}\n"
                    else:
                        stats_text += f"{key:15s}: ${value:,.2f}\n"

                # Add additional information
                if 'job_category' in job_df.columns:
                    categories = job_df['job_category'].unique()
                    if len(categories) > 0:
                        stats_text += f"\nJob Category: {', '.join(categories)}"

                if 'department' in job_df.columns:
                    departments = job_df['department'].unique()
                    if len(departments) > 0:
                        stats_text += f"\nDepartments: {', '.join(departments)}"

                # Position stats text box
                ax.text(1.15, 0.5, stats_text,
                       transform=ax.transAxes,
                       fontsize=9,
                       verticalalignment='center',
                       fontfamily='monospace',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

                # Add individual data points
                y_data = job_df['salary'].values
                x_data = [1] * len(y_data)
                ax.scatter(x_data, y_data, alpha=0.5, s=50, color='navy', zorder=3)

                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()

            # Create comparative plot if multiple job titles exist
            if len(job_titles) > 1:
                fig, ax = plt.subplots(figsize=(11, 8.5))

                # Add header
                fig.text(0.5, 0.96, institution_name,
                        ha='center', va='top',
                        fontsize=16, fontweight='bold',
                        color='#2C3E50')

                # Prepare data for comparative plot
                job_data = [inst_df[inst_df['job_title'] == jt]['salary'].values
                           for jt in sorted(job_titles)]

                # Create box plot
                box_plot = ax.boxplot(job_data,
                                     labels=sorted(job_titles),
                                     patch_artist=True,
                                     showmeans=True,
                                     meanprops=dict(marker='D', markerfacecolor='red', markersize=6))

                # Customize colors
                colors = plt.cm.Set3(range(len(job_titles)))
                for patch, color in zip(box_plot['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)

                # Format y-axis
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

                # Labels and title
                ax.set_ylabel('Annual Salary (USD)', fontsize=12, fontweight='bold')
                ax.set_xlabel('Job Title', fontsize=12, fontweight='bold')
                ax.set_title(f'Comparative Salary Analysis - All Positions',
                           fontsize=14, fontweight='bold', pad=20)

                # Rotate x-axis labels if needed
                plt.xticks(rotation=45, ha='right')

                # Add grid
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')

                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()

        print(f"Report saved: {output_path}")

    def generate_report(self, institution_name=None, output_dir='reports'):
        """
        Generate salary report for one or all institutions.

        Args:
            institution_name (str, optional): Specific institution to report on
            output_dir (str): Directory to save reports
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Query all data
        df = self.query_salary_data()

        if df.empty:
            print("No data available to generate report")
            return

        # Generate report for specific institution or all institutions
        if institution_name:
            institutions = [institution_name]
        else:
            institutions = self.get_institutions()

        for inst in institutions:
            # Create safe filename
            safe_name = inst.replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f'salary_report_{safe_name}_{timestamp}.pdf')

            print(f"\nGenerating report for: {inst}")
            self.create_box_plot(df, inst, output_path)


def load_config(config_file='config.ini'):
    """Load database configuration from file."""
    config = configparser.ConfigParser()

    if os.path.exists(config_file):
        config.read(config_file)
        db_config = {
            'host': config.get('database', 'host', fallback='localhost'),
            'port': config.getint('database', 'port', fallback=5432),
            'database': config.get('database', 'database'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password')
        }
        return db_config
    else:
        print(f"Config file not found: {config_file}")
        print("Using environment variables or defaults")
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'acadexis_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }


def main():
    """Main function to run the salary report generator."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate salary band reports')
    parser.add_argument('--institution', '-i', type=str,
                       help='Specific institution name to generate report for')
    parser.add_argument('--output-dir', '-o', type=str, default='reports',
                       help='Output directory for reports (default: reports)')
    parser.add_argument('--config', '-c', type=str, default='config.ini',
                       help='Configuration file path (default: config.ini)')
    parser.add_argument('--logo', '-l', type=str,
                       help='Path to Acadexis logo image file')

    args = parser.parse_args()

    # Load configuration
    db_config = load_config(args.config)

    # Create report generator
    generator = SalaryReportGenerator(db_config)

    # Set logo if provided
    if args.logo:
        generator.set_logo_path(args.logo)

    # Connect to database
    generator.connect()

    try:
        # Generate reports
        generator.generate_report(
            institution_name=args.institution,
            output_dir=args.output_dir
        )
    finally:
        # Disconnect from database
        generator.disconnect()

    print("\nReport generation complete!")


if __name__ == '__main__':
    main()
