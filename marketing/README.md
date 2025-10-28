# Acadexis Salary Band Report Generator

Generate professional salary band analysis reports for higher education institutions using PostgreSQL data and box-and-whisker plots.

## Overview

This tool queries employee salary information from a PostgreSQL database and generates comprehensive PDF reports featuring:

- Box and whisker plots showing salary distributions by job title
- Statistical analysis (min, max, median, mean, quartiles, standard deviation)
- Professional branding with Acadexis logo
- Institution-specific headers
- Comparative analysis across multiple positions

## Features

- **Database Integration**: Direct PostgreSQL connectivity for real-time data analysis
- **Statistical Visualization**: Box and whisker plots for clear salary band representation
- **Professional Reports**: PDF output with custom branding and institutional headers
- **Flexible Filtering**: Generate reports for specific institutions or all institutions
- **Comprehensive Statistics**: Detailed statistical breakdowns for each position
- **Comparative Analysis**: Side-by-side comparison of multiple job titles

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database server
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or navigate to the marketing directory**:
   ```bash
   cd marketing
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**:
   ```bash
   # Connect to your PostgreSQL instance
   psql -U postgres

   # Create database
   CREATE DATABASE acadexis_db;

   # Connect to the database
   \c acadexis_db

   # Run the schema file
   \i schema.sql
   ```

4. **Configure database connection**:
   ```bash
   # Copy the example config file
   cp config.ini.example config.ini

   # Edit config.ini with your database credentials
   nano config.ini
   ```

## Database Schema

The PostgreSQL table `employee_salaries` includes the following fields:

| Field | Type | Description |
|-------|------|-------------|
| employee_id | SERIAL | Primary key |
| institution_name | VARCHAR(255) | Name of the institution |
| job_title | VARCHAR(255) | Employee job title |
| salary | NUMERIC(12,2) | Annual salary in USD |
| job_category | VARCHAR(100) | Category (Faculty, Administrative, etc.) |
| department | VARCHAR(255) | Department name |
| institution_type | VARCHAR(100) | Public, Private, Community College |
| employment_type | VARCHAR(50) | Full-Time, Part-Time, Adjunct |
| hire_date | DATE | Date of hire |
| years_of_experience | INTEGER | Years of experience |
| education_level | VARCHAR(100) | Highest degree earned |
| location | VARCHAR(255) | Geographic location |

### Sample Data

The schema.sql file includes sample data for demonstration:
- Stanford University
- UC Berkeley
- MIT

Sample positions include:
- Professor
- Associate Professor
- Assistant Professor
- Department Chair
- Lecturer
- Registrar
- Financial Aid Director

## Usage

### Basic Usage

Generate reports for all institutions:
```bash
python generate_salary_report.py
```

### Generate Report for Specific Institution

```bash
python generate_salary_report.py --institution "Stanford University"
```

### Specify Output Directory

```bash
python generate_salary_report.py --output-dir /path/to/reports
```

### Include Acadexis Logo

```bash
python generate_salary_report.py --logo /path/to/acadexis_logo.png
```

### Use Custom Configuration File

```bash
python generate_salary_report.py --config /path/to/custom_config.ini
```

### Combined Options

```bash
python generate_salary_report.py \
  --institution "MIT" \
  --output-dir ./reports \
  --logo ./assets/acadexis_logo.png \
  --config ./config.ini
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| --institution | -i | Specific institution to report on | All institutions |
| --output-dir | -o | Output directory for PDF reports | ./reports |
| --config | -c | Path to configuration file | ./config.ini |
| --logo | -l | Path to Acadexis logo image | None |

## Configuration

Edit `config.ini` to set database connection parameters:

```ini
[database]
host = localhost
port = 5432
database = acadexis_db
user = postgres
password = your_password_here

[report]
output_dir = reports
```

Alternatively, use environment variables:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

## Output

Reports are saved as PDF files in the specified output directory with the naming format:
```
salary_report_{institution_name}_{timestamp}.pdf
```

Example:
```
reports/salary_report_Stanford_University_20250128_143022.pdf
```

### Report Contents

Each PDF report includes:

1. **Title Page**:
   - Acadexis logo (if provided)
   - Institution name
   - Generation date
   - Summary statistics

2. **Individual Position Analysis** (one page per job title):
   - Box and whisker plot
   - Statistical breakdown
   - Job category and department information
   - Individual data points overlaid

3. **Comparative Analysis** (if multiple positions exist):
   - Side-by-side box plots
   - Cross-position salary comparison

## Adding Your Own Data

### Method 1: SQL Insert

```sql
INSERT INTO employee_salaries (
    institution_name,
    job_title,
    salary,
    job_category,
    department,
    employment_type
) VALUES (
    'Your University',
    'Assistant Professor',
    95000.00,
    'Faculty',
    'Computer Science',
    'Full-Time'
);
```

### Method 2: CSV Import

```bash
# Create a CSV file with your data
# Then import using psql
\copy employee_salaries(institution_name, job_title, salary, job_category, department, employment_type)
FROM 'your_data.csv'
DELIMITER ','
CSV HEADER;
```

### Method 3: Python Script

Create a custom data import script using psycopg2:

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="acadexis_db",
    user="postgres",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("""
    INSERT INTO employee_salaries (institution_name, job_title, salary)
    VALUES (%s, %s, %s)
""", ("Harvard University", "Professor", 180000.00))

conn.commit()
conn.close()
```

## Logo Setup

To include the Acadexis logo in reports:

1. Save your logo image file (PNG, JPG, or similar format)
2. Use the `--logo` parameter when running the script
3. Or add the logo path to the configuration file

Supported formats: PNG, JPG, JPEG, GIF

## Troubleshooting

### Database Connection Issues

```
Error: could not connect to server
```
- Verify PostgreSQL is running
- Check database credentials in config.ini
- Ensure database exists and schema is loaded

### No Data in Reports

```
No data available for institution
```
- Verify data exists in the database
- Check institution name spelling (case-sensitive)
- Run query manually to confirm data presence

### Missing Dependencies

```
ModuleNotFoundError: No module named 'psycopg2'
```
- Install requirements: `pip install -r requirements.txt`
- Consider using a virtual environment

### Logo Not Loading

```
Warning: Logo not found at path
```
- Check logo file path is correct
- Verify file format is supported (PNG, JPG)
- Ensure file has read permissions

## Examples

### Example 1: Generate Report for All Institutions

```bash
python generate_salary_report.py
```

Output:
```
Connected to database: acadexis_db
Retrieved 24 salary records

Generating report for: Stanford University
Report saved: reports/salary_report_Stanford_University_20250128_143022.pdf

Generating report for: UC Berkeley
Report saved: reports/salary_report_UC_Berkeley_20250128_143025.pdf

Generating report for: MIT
Report saved: reports/salary_report_MIT_20250128_143028.pdf

Database connection closed
Report generation complete!
```

### Example 2: Single Institution with Logo

```bash
python generate_salary_report.py \
  --institution "Stanford University" \
  --logo ./acadexis_logo.png
```

### Example 3: Custom Output Location

```bash
python generate_salary_report.py \
  --output-dir /home/reports/2025 \
  --institution "UC Berkeley"
```

## Database Queries

### View All Institutions

```sql
SELECT DISTINCT institution_name
FROM employee_salaries
ORDER BY institution_name;
```

### View All Job Titles for an Institution

```sql
SELECT DISTINCT job_title, COUNT(*) as count
FROM employee_salaries
WHERE institution_name = 'Stanford University'
GROUP BY job_title
ORDER BY job_title;
```

### Calculate Salary Statistics

```sql
SELECT
    job_title,
    COUNT(*) as num_employees,
    MIN(salary) as min_salary,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM employee_salaries
WHERE institution_name = 'MIT'
GROUP BY job_title
ORDER BY avg_salary DESC;
```

## Architecture

```
marketing/
├── generate_salary_report.py   # Main script
├── schema.sql                   # Database schema and sample data
├── requirements.txt             # Python dependencies
├── config.ini.example           # Configuration template
├── config.ini                   # Your configuration (create this)
├── README.md                    # This file
└── reports/                     # Generated PDF reports (auto-created)
```

## Contributing

To add new features or improve the report generator:

1. Modify `generate_salary_report.py` for new functionality
2. Update `schema.sql` if database changes are needed
3. Update this README with new instructions

## License

Copyright © 2025 Acadexis. All rights reserved.

## Support

For issues or questions, please contact your Acadexis representative or refer to the internal documentation.

## Version History

- **v1.0.0** (2025-01-28): Initial release
  - PostgreSQL integration
  - Box and whisker plot generation
  - PDF report output
  - Multi-institution support
  - Statistical analysis
