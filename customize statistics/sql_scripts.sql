-- By Enrollment
WITH school_medians AS (
  SELECT
    carnegie.unitid,
    carnegie.name AS school,
    carnegie.stabbr AS state,
    MAX(enroll.enrollment) AS enrollment,
    CASE
      WHEN MAX(enroll.enrollment) < 5000 THEN 'Small (<5k)'
      WHEN MAX(enroll.enrollment) BETWEEN 5000 AND 20000 THEN 'Medium (5k–20k)'
      WHEN MAX(enroll.enrollment) > 20000 THEN 'Large (20k+)'
      ELSE 'Unknown'
    END AS enrollment_category,
    COUNT(DISTINCT employee.id) AS employee_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY employee.fte_annualized_base_salary) AS median_salary
  FROM employee_details AS employee
  LEFT JOIN carnegie_institutions AS carnegie
    ON employee.institution_id = carnegie.id
  LEFT JOIN (
      SELECT unitid, MAX(enrollment) AS enrollment
      FROM carnegie_enrollment_data
      WHERE student_classification = 1
      GROUP BY unitid
  ) AS enroll
    ON carnegie.unitid = enroll.unitid
  WHERE employee.fte IN ('1', '1.0')
    AND employee.working_title_id IN (62,172,274,335,2,364,451,476,532,533,549,600,65,510)
    AND employee.fiscal_year = 2026
  GROUP BY carnegie.unitid, carnegie.name, carnegie.stabbr
  HAVING COUNT(DISTINCT employee.id) > 15
),
category_medians AS (
  SELECT
    enrollment_category,
    COUNT(DISTINCT unitid) AS number_of_schools,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY median_salary) AS category_median_salary
  FROM school_medians
  WHERE enrollment_category IS NOT NULL
  GROUP BY enrollment_category
)
SELECT
  s.unitid,
  s.school,
  s.state,
  s.enrollment,
  s.enrollment_category,
  s.employee_count,
  ROUND(s.median_salary::numeric, 2) AS school_median_salary,
  st.number_of_schools AS schools_in_category,
  ROUND(st.category_median_salary::numeric, 2) AS category_median_salary,
  ROUND(
    ((s.median_salary - st.category_median_salary) / st.category_median_salary * 100)::numeric,
    2
  ) AS percent_diff_from_category_median
FROM school_medians s
JOIN category_medians st
  ON s.enrollment_category = st.enrollment_category
ORDER BY s.enrollment_category, percent_diff_from_category_median DESC;


-- State
WITH school_medians AS (
  SELECT
    carnegie.unitid,
    carnegie.name AS school,
    carnegie.stabbr AS state,
    COUNT(DISTINCT employee.id) AS employee_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY employee.fte_annualized_base_salary) AS median_salary
  FROM employee_details AS employee
  LEFT JOIN carnegie_institutions AS carnegie
    ON employee.institution_id = carnegie.id
  WHERE employee.fte IN ('1', '1.0')
    AND employee.working_title_id IN (62,172,274,335,2,364,451,476,532,533,549,600,65,510)
    AND employee.fiscal_year = 2026
  GROUP BY carnegie.unitid, carnegie.name, carnegie.stabbr
  HAVING COUNT(DISTINCT employee.id) > 15
),
state_medians AS (
  SELECT
    state,
    COUNT(DISTINCT unitid) as number_of_schools,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY median_salary) AS state_median_salary
  FROM school_medians
  GROUP BY state
)
SELECT
  s.unitid,
  s.school,
  s.state,
  s.employee_count,
  ROUND(s.median_salary::numeric, 2) as school_median_salary,
  st.number_of_schools as schools_in_state,
  ROUND(st.state_median_salary::numeric, 2) as state_median_salary,
  ROUND(
    ((s.median_salary - st.state_median_salary) / st.state_median_salary * 100)::numeric,
    2
  ) AS percent_diff_from_state_median
FROM school_medians s
JOIN state_medians st
  ON s.state = st.state
ORDER BY s.state, percent_diff_from_state_median DESC;

-- By Classification
WITH school_medians AS (
  SELECT
    carnegie.unitid,
    carnegie.name AS school,
    carnegie.stabbr AS state,
    class.name AS classification,  -- from carnegie_basic2021s
    COUNT(DISTINCT employee.id) AS employee_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY employee.fte_annualized_base_salary) AS median_salary
  FROM employee_details AS employee
  LEFT JOIN departments AS depart
    ON employee.department_id = depart.id
  LEFT JOIN working_titles AS title
    ON employee.working_title_id = title.id
  LEFT JOIN carnegie_institutions AS carnegie
    ON employee.institution_id = carnegie.id
  LEFT JOIN carnegie_basic2021s AS class
    ON class.code = carnegie.carnegie_basic2021_id
  WHERE employee.fte IN ('1', '1.0')
    AND employee.working_title_id IN (62,172,274,335,2,364,451,476,532,533,549,600,65,510)
    AND employee.fiscal_year = 2026
  GROUP BY carnegie.unitid, carnegie.name, carnegie.stabbr, class.name
  HAVING COUNT(DISTINCT employee.id) > 15
),
classification_medians AS (
  SELECT
    classification,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY median_salary) AS classification_median_salary
  FROM school_medians
  GROUP BY classification
)
SELECT
  s.unitid,
  s.school,
  s.state,
  s.classification,
  s.employee_count,
  s.median_salary,
  st.classification_median_salary AS national_classification_median,
  ROUND(
    ((s.median_salary - st.classification_median_salary) / st.classification_median_salary * 100)::numeric,
    2
  ) AS percent_diff_from_classification
FROM school_medians s
JOIN classification_medians st
  ON s.classification = st.classification
ORDER BY s.classification, percent_diff_from_classification DESC;

