-- By Enrollment
WITH school_medians AS (
  SELECT
    carnegie.unitid,
    carnegie.name AS school,
    carnegie.stabbr AS state,
    MAX(enroll.enrollment) AS enrollment,
    CASE
      WHEN MAX(enroll.enrollment) < 5000 THEN 'Small (<5k Enrollment)'
      WHEN MAX(enroll.enrollment) BETWEEN 5000 AND 20000 THEN 'Medium (5k–20k Enrollment)'
      WHEN MAX(enroll.enrollment) > 20000 THEN 'Large (20k+ Enrollment)'
      ELSE 'Unknown'
    END AS enrollment_category,
    COUNT(DISTINCT employee.id) AS employee_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY employee.fte_annualized_base_salary) AS median_salary
  FROM employee_details AS employee
  LEFT JOIN departments AS depart
    ON employee.department_id = depart.id
  LEFT JOIN working_titles AS title
    ON employee.working_title_id = title.id
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
state_category_medians AS (
  SELECT
    state,
    enrollment_category,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY median_salary) AS state_category_median
  FROM school_medians
  GROUP BY state, enrollment_category
)
SELECT
  s.unitid,
  s.school,
  s.state,
  s.enrollment,
  s.enrollment_category,
  s.employee_count,
  s.median_salary,
  st.state_category_median AS state_median_salary,
  ROUND(
    ((s.median_salary - st.state_category_median) / st.state_category_median * 100)::numeric,
    2
  ) AS percent_diff_from_state_category
FROM school_medians s
JOIN state_category_medians st
  ON s.state = st.state
  AND s.enrollment_category = st.enrollment_category
ORDER BY s.state, s.enrollment_category, percent_diff_from_state_category DESC;