# Salary Data Analysis and PDF Generation System

This folder contains a comprehensive salary analysis system for higher education institutions. The system generates professional PDF reports with box and whisker plots showing salary bands for different job titles across multiple institutions.

## Files

- `salary_data.csv` - Sample salary data from 3 higher education institutions (UC Berkeley, Stanford, MIT)
- `generate_salary_pdfs.py` - Python script to auto-generate PDF reports
- `requirements.txt` - Python dependencies
- `pdf_reports/` - Output directory for generated PDFs (created automatically)

## Data Structure

The CSV file contains the following fields:

- **Institution Name** - Name of the higher education institution
- **Job Title** - Specific job title (e.g., "Assistant Professor", "IT Manager")
- **Job Family** - Broader category (e.g., "Faculty", "Information Technology", "Student Services")
- **Min Salary** - Minimum salary for the position
- **Q1 Salary** - First quartile (25th percentile)
- **Median Salary** - Median salary (50th percentile)
- **Q3 Salary** - Third quartile (75th percentile)
- **Max Salary** - Maximum salary for the position

This data structure is specifically designed for creating box and whisker plots, which visualize salary distributions effectively.

## Installation

Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

## Usage

Generate all PDF reports:

```bash
python3 generate_salary_pdfs.py
```

This will create two types of PDFs:

### 1. Individual PDFs (30 files)
- One PDF per job title per institution
- Location: `pdf_reports/`
- Naming format: `{Institution}_{JobTitle}.pdf`
- Example: `MIT_Assistant_Professor.pdf`

Each individual PDF includes:
- Box and whisker plot for that specific position
- Job family information
- Complete salary statistics (Min, Q1, Median, Q3, Max, Range)
- Professional formatting with clear labels

### 2. Comparison PDFs (10 files)
- One PDF per job title showing all institutions
- Location: `pdf_reports/comparisons/`
- Naming format: `Comparison_{JobTitle}.pdf`
- Example: `Comparison_Assistant_Professor.pdf`

Each comparison PDF includes:
- Side-by-side box plots comparing all institutions
- Color-coded boxes for easy differentiation
- Legend explaining box plot elements
- Useful for salary benchmarking across institutions

## Understanding Box and Whisker Plots

Box plots display salary distributions through five key statistics:

- **Bottom whisker**: Minimum salary
- **Bottom of box**: Q1 (25% of salaries are below this)
- **Line in box**: Median salary (middle value)
- **Top of box**: Q3 (75% of salaries are below this)
- **Top whisker**: Maximum salary
- **Red diamond**: Mean (average) salary

The box represents the middle 50% of salaries (interquartile range).

## Sample Data

The sample dataset includes:
- **3 Institutions**: UC Berkeley, Stanford, MIT
- **10 Job Titles** across 3 job families:
  - **Faculty**: Assistant Professor, Associate Professor, Full Professor, Lecturer, Department Chair
  - **Student Services**: Academic Advisor, Admissions Officer, Financial Aid Counselor
  - **Information Technology**: IT Manager, Systems Administrator

## Customization

To use with your own data:

1. Update `salary_data.csv` with your institution data
2. Maintain the same column structure
3. Run the script to generate updated PDFs

The script automatically:
- Creates output directories if they don't exist
- Formats salary values as currency
- Handles any number of institutions and job titles
- Sanitizes filenames for safe file system storage

## Output

Running the script generates:
- 30 individual PDFs (one per job title per institution)
- 10 comparison PDFs (one per job title)
- Total: 40 professionally formatted PDF reports

All PDFs are print-ready and suitable for:
- Salary benchmarking
- Compensation analysis
- Budget planning
- HR presentations
- Academic administration reporting
