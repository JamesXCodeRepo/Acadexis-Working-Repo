# Higher Education Salary Analysis Tool

This tool generates PDF reports with box and whisker plots for salary analysis across multiple higher education institutions.

## Files

- `salary_data.csv` - Sample salary data for 3 institutions (UC Berkeley, Stanford, MIT)
- `generate_salary_pdfs.py` - Python script to generate PDF reports
- `requirements.txt` - Python dependencies
- `salary_reports/` - Output directory for generated PDF files (created automatically)

## Data Structure

The CSV file contains the following fields:

- `institution_name` - Name of the higher education institution
- `job_title` - Specific job title
- `job_family` - Job category (Faculty, Student Services, Administrative, Technology)
- `min_salary` - Minimum salary in the distribution
- `q1_salary` - First quartile (25th percentile)
- `median_salary` - Median salary (50th percentile)
- `q3_salary` - Third quartile (75th percentile)
- `max_salary` - Maximum salary in the distribution
- `sample_size` - Number of employees in this category

## Installation

Install required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Generate all PDF reports:

```bash
python generate_salary_pdfs.py
```

This will:
1. Read the salary data from `salary_data.csv`
2. Create a `salary_reports/` directory
3. Generate one PDF per job title per institution
4. Each PDF contains a box and whisker plot showing the salary distribution

## Output

Each PDF report includes:
- Box and whisker plot visualization
- Salary statistics (min, Q1, median, Q3, max)
- Job family classification
- Sample size
- Color-coded plot elements with legend

Example filename: `Stanford_University_Assistant_Professor_salary_report.pdf`

## Sample Data

The sample dataset includes:
- **3 Institutions**: UC Berkeley, Stanford, MIT
- **Job Families**: Faculty, Student Services, Administrative, Technology
- **Multiple Job Titles** per institution covering various roles and seniority levels

## Customization

To use your own data:
1. Update `salary_data.csv` with your data following the same column structure
2. Run the script to generate reports for your custom dataset
