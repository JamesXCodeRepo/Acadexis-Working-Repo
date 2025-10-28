-- PostgreSQL Database Schema for Employee Salary Information
-- Higher Education Institutions

-- Drop table if exists
DROP TABLE IF EXISTS employee_salaries CASCADE;

-- Create employee_salaries table
CREATE TABLE employee_salaries (
    employee_id SERIAL PRIMARY KEY,
    institution_name VARCHAR(255) NOT NULL,
    institution_type VARCHAR(100),  -- e.g., 'Public', 'Private', 'Community College'
    job_title VARCHAR(255) NOT NULL,
    job_category VARCHAR(100),  -- e.g., 'Faculty', 'Administrative', 'Staff', 'Executive'
    department VARCHAR(255),
    salary NUMERIC(12, 2) NOT NULL,
    hire_date DATE,
    employment_type VARCHAR(50),  -- e.g., 'Full-Time', 'Part-Time', 'Adjunct'
    years_of_experience INTEGER,
    education_level VARCHAR(100),  -- e.g., 'Bachelor', 'Master', 'Doctorate'
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_institution_name ON employee_salaries(institution_name);
CREATE INDEX idx_job_title ON employee_salaries(job_title);
CREATE INDEX idx_job_category ON employee_salaries(job_category);
CREATE INDEX idx_salary ON employee_salaries(salary);
CREATE INDEX idx_institution_job ON employee_salaries(institution_name, job_title);

-- Insert sample data for testing
INSERT INTO employee_salaries (institution_name, institution_type, job_title, job_category, department, salary, hire_date, employment_type, years_of_experience, education_level, location)
VALUES
    -- Stanford University samples
    ('Stanford University', 'Private', 'Professor', 'Faculty', 'Computer Science', 185000.00, '2015-08-15', 'Full-Time', 15, 'Doctorate', 'Stanford, CA'),
    ('Stanford University', 'Private', 'Professor', 'Faculty', 'Computer Science', 195000.00, '2012-09-01', 'Full-Time', 18, 'Doctorate', 'Stanford, CA'),
    ('Stanford University', 'Private', 'Associate Professor', 'Faculty', 'Computer Science', 145000.00, '2018-08-20', 'Full-Time', 8, 'Doctorate', 'Stanford, CA'),
    ('Stanford University', 'Private', 'Assistant Professor', 'Faculty', 'Computer Science', 125000.00, '2020-09-01', 'Full-Time', 3, 'Doctorate', 'Stanford, CA'),
    ('Stanford University', 'Private', 'Department Chair', 'Administrative', 'Computer Science', 210000.00, '2010-07-01', 'Full-Time', 20, 'Doctorate', 'Stanford, CA'),
    ('Stanford University', 'Private', 'Lecturer', 'Faculty', 'Computer Science', 95000.00, '2019-01-15', 'Full-Time', 5, 'Master', 'Stanford, CA'),

    -- UC Berkeley samples
    ('UC Berkeley', 'Public', 'Professor', 'Faculty', 'Computer Science', 175000.00, '2014-08-15', 'Full-Time', 16, 'Doctorate', 'Berkeley, CA'),
    ('UC Berkeley', 'Public', 'Professor', 'Faculty', 'Computer Science', 180000.00, '2011-09-01', 'Full-Time', 19, 'Doctorate', 'Berkeley, CA'),
    ('UC Berkeley', 'Public', 'Associate Professor', 'Faculty', 'Computer Science', 135000.00, '2017-08-20', 'Full-Time', 9, 'Doctorate', 'Berkeley, CA'),
    ('UC Berkeley', 'Public', 'Assistant Professor', 'Faculty', 'Computer Science', 115000.00, '2021-09-01', 'Full-Time', 2, 'Doctorate', 'Berkeley, CA'),
    ('UC Berkeley', 'Public', 'Lecturer', 'Faculty', 'Computer Science', 85000.00, '2019-01-15', 'Full-Time', 4, 'Master', 'Berkeley, CA'),
    ('UC Berkeley', 'Public', 'Department Chair', 'Administrative', 'Computer Science', 195000.00, '2009-07-01', 'Full-Time', 22, 'Doctorate', 'Berkeley, CA'),

    -- MIT samples
    ('MIT', 'Private', 'Professor', 'Faculty', 'Computer Science', 190000.00, '2013-08-15', 'Full-Time', 17, 'Doctorate', 'Cambridge, MA'),
    ('MIT', 'Private', 'Professor', 'Faculty', 'Computer Science', 200000.00, '2010-09-01', 'Full-Time', 20, 'Doctorate', 'Cambridge, MA'),
    ('MIT', 'Private', 'Associate Professor', 'Faculty', 'Computer Science', 150000.00, '2016-08-20', 'Full-Time', 10, 'Doctorate', 'Cambridge, MA'),
    ('MIT', 'Private', 'Assistant Professor', 'Faculty', 'Computer Science', 130000.00, '2020-09-01', 'Full-Time', 4, 'Doctorate', 'Cambridge, MA'),
    ('MIT', 'Private', 'Lecturer', 'Faculty', 'Computer Science', 100000.00, '2018-01-15', 'Full-Time', 6, 'Master', 'Cambridge, MA'),
    ('MIT', 'Private', 'Department Chair', 'Administrative', 'Computer Science', 220000.00, '2008-07-01', 'Full-Time', 24, 'Doctorate', 'Cambridge, MA');

-- Add more sample data for additional job titles
INSERT INTO employee_salaries (institution_name, institution_type, job_title, job_category, department, salary, hire_date, employment_type, years_of_experience, education_level, location)
VALUES
    -- Registrar positions
    ('Stanford University', 'Private', 'Registrar', 'Administrative', 'Academic Affairs', 95000.00, '2016-03-01', 'Full-Time', 12, 'Master', 'Stanford, CA'),
    ('UC Berkeley', 'Public', 'Registrar', 'Administrative', 'Academic Affairs', 88000.00, '2017-05-15', 'Full-Time', 10, 'Master', 'Berkeley, CA'),
    ('MIT', 'Private', 'Registrar', 'Administrative', 'Academic Affairs', 98000.00, '2015-02-01', 'Full-Time', 14, 'Master', 'Cambridge, MA'),

    -- Financial Aid Director positions
    ('Stanford University', 'Private', 'Financial Aid Director', 'Administrative', 'Student Services', 110000.00, '2014-06-01', 'Full-Time', 15, 'Master', 'Stanford, CA'),
    ('UC Berkeley', 'Public', 'Financial Aid Director', 'Administrative', 'Student Services', 105000.00, '2016-08-15', 'Full-Time', 12, 'Master', 'Berkeley, CA'),
    ('MIT', 'Private', 'Financial Aid Director', 'Administrative', 'Student Services', 115000.00, '2013-07-01', 'Full-Time', 17, 'Master', 'Cambridge, MA');

COMMENT ON TABLE employee_salaries IS 'Employee salary information for higher education institutions';
COMMENT ON COLUMN employee_salaries.institution_name IS 'Name of the higher education institution';
COMMENT ON COLUMN employee_salaries.job_title IS 'Employee job title/position';
COMMENT ON COLUMN employee_salaries.salary IS 'Annual salary in USD';
COMMENT ON COLUMN employee_salaries.job_category IS 'Category of job (Faculty, Administrative, Staff, Executive)';
