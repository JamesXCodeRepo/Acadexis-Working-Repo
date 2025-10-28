#!/usr/bin/env python3
"""
Add sample data to the employee_salaries database.

This script demonstrates how to programmatically add salary data
to the PostgreSQL database.
"""

import psycopg2
import sys
import configparser
import os
from datetime import date


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
        sys.exit(1)


def add_employee_record(cursor, employee_data):
    """
    Add a single employee record to the database.

    Args:
        cursor: Database cursor
        employee_data (dict): Employee information
    """
    query = """
        INSERT INTO employee_salaries (
            institution_name,
            institution_type,
            job_title,
            job_category,
            department,
            salary,
            hire_date,
            employment_type,
            years_of_experience,
            education_level,
            location
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING employee_id;
    """

    values = (
        employee_data.get('institution_name'),
        employee_data.get('institution_type'),
        employee_data.get('job_title'),
        employee_data.get('job_category'),
        employee_data.get('department'),
        employee_data.get('salary'),
        employee_data.get('hire_date'),
        employee_data.get('employment_type'),
        employee_data.get('years_of_experience'),
        employee_data.get('education_level'),
        employee_data.get('location')
    )

    cursor.execute(query, values)
    employee_id = cursor.fetchone()[0]
    return employee_id


def main():
    """Main function to add sample data."""
    print("Acadexis Salary Database - Add Sample Data")
    print("=" * 50)

    # Load configuration
    db_config = load_config()

    # Sample data to add
    sample_employees = [
        {
            'institution_name': 'Harvard University',
            'institution_type': 'Private',
            'job_title': 'Professor',
            'job_category': 'Faculty',
            'department': 'Computer Science',
            'salary': 195000.00,
            'hire_date': date(2012, 9, 1),
            'employment_type': 'Full-Time',
            'years_of_experience': 19,
            'education_level': 'Doctorate',
            'location': 'Cambridge, MA'
        },
        {
            'institution_name': 'Harvard University',
            'institution_type': 'Private',
            'job_title': 'Associate Professor',
            'job_category': 'Faculty',
            'department': 'Computer Science',
            'salary': 155000.00,
            'hire_date': date(2016, 8, 15),
            'employment_type': 'Full-Time',
            'years_of_experience': 11,
            'education_level': 'Doctorate',
            'location': 'Cambridge, MA'
        },
        {
            'institution_name': 'Harvard University',
            'institution_type': 'Private',
            'job_title': 'Assistant Professor',
            'job_category': 'Faculty',
            'department': 'Computer Science',
            'salary': 135000.00,
            'hire_date': date(2020, 9, 1),
            'employment_type': 'Full-Time',
            'years_of_experience': 5,
            'education_level': 'Doctorate',
            'location': 'Cambridge, MA'
        },
        {
            'institution_name': 'Yale University',
            'institution_type': 'Private',
            'job_title': 'Professor',
            'job_category': 'Faculty',
            'department': 'Economics',
            'salary': 188000.00,
            'hire_date': date(2011, 8, 20),
            'employment_type': 'Full-Time',
            'years_of_experience': 20,
            'education_level': 'Doctorate',
            'location': 'New Haven, CT'
        },
        {
            'institution_name': 'Yale University',
            'institution_type': 'Private',
            'job_title': 'Associate Professor',
            'job_category': 'Faculty',
            'department': 'Economics',
            'salary': 148000.00,
            'hire_date': date(2017, 8, 15),
            'employment_type': 'Full-Time',
            'years_of_experience': 10,
            'education_level': 'Doctorate',
            'location': 'New Haven, CT'
        },
    ]

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )

        print(f"Connected to database: {db_config['database']}")
        print()

        cursor = conn.cursor()

        # Add each employee
        added_count = 0
        for employee in sample_employees:
            try:
                employee_id = add_employee_record(cursor, employee)
                print(f"Added: {employee['institution_name']} - "
                      f"{employee['job_title']} (ID: {employee_id})")
                added_count += 1
            except Exception as e:
                print(f"Error adding record: {e}")

        # Commit changes
        conn.commit()

        print()
        print(f"Successfully added {added_count} employee records")

        # Show summary
        cursor.execute("""
            SELECT institution_name, COUNT(*) as count
            FROM employee_salaries
            GROUP BY institution_name
            ORDER BY institution_name
        """)

        print()
        print("Current database summary:")
        print("-" * 50)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} employees")

        # Close connection
        cursor.close()
        conn.close()

        print()
        print("Database connection closed")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
