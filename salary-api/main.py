"""
Acadexis Salary Comparison API

FastAPI application that exposes salary comparison data from PostgreSQL database.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import asyncpg
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Acadexis Salary Comparison API",
    description="API for retrieving salary comparison data by enrollment category",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for response
class SalaryByEnrollment(BaseModel):
    unitid: int
    school: str
    state: str
    enrollment: int
    enrollment_category: str
    employee_count: int
    median_salary: float
    state_median_salary: float
    percent_diff_from_state_category: float


# Database connection pool
db_pool = None


async def get_db_pool():
    """Get or create database connection pool."""
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'postgres'),
            min_size=2,
            max_size=10
        )
    return db_pool


@app.on_event("startup")
async def startup():
    """Initialize database pool on startup."""
    await get_db_pool()
    print("Database pool initialized")


@app.on_event("shutdown")
async def shutdown():
    """Close database pool on shutdown."""
    global db_pool
    if db_pool:
        await db_pool.close()
        print("Database pool closed")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Acadexis Salary Comparison API",
        "version": "1.0.0",
        "endpoints": {
            "/salary-by-enrollment": "Get salary data by enrollment category",
            "/salary-by-enrollment/{unitid}": "Get salary data for specific institution"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    pool = await get_db_pool()
    try:
        async with pool.acquire() as conn:
            await conn.fetchval('SELECT 1')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.get("/salary-by-enrollment", response_model=List[SalaryByEnrollment])
async def get_salary_by_enrollment(
    unitid: Optional[int] = Query(None, description="Filter by specific institution unitid"),
    state: Optional[str] = Query(None, description="Filter by state abbreviation"),
    enrollment_category: Optional[str] = Query(None, description="Filter by enrollment category")
):
    """
    Get salary comparison data by enrollment category.

    This endpoint returns median salary data for institutions compared to their
    state median within the same enrollment category.

    Parameters:
    - unitid: Optional filter for a specific institution
    - state: Optional filter by state abbreviation
    - enrollment_category: Optional filter by enrollment size (Small, Medium, Large)
    """
    pool = await get_db_pool()

    # Base query (modified from sql_scripts.sql)
    query = """
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
    WHERE 1=1
    """

    # Add filters
    params = []
    param_counter = 1

    if unitid is not None:
        query += f" AND s.unitid = ${param_counter}"
        params.append(unitid)
        param_counter += 1

    if state is not None:
        query += f" AND s.state = ${param_counter}"
        params.append(state.upper())
        param_counter += 1

    if enrollment_category is not None:
        query += f" AND s.enrollment_category = ${param_counter}"
        params.append(enrollment_category)
        param_counter += 1

    query += " ORDER BY s.state, s.enrollment_category, percent_diff_from_state_category DESC"

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, *params)

            if not rows and unitid is not None:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data found for unitid: {unitid}"
                )

            # Convert rows to dictionaries
            results = [dict(row) for row in rows]
            return results

    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/salary-by-enrollment/{unitid}", response_model=SalaryByEnrollment)
async def get_salary_by_enrollment_unitid(unitid: int):
    """
    Get salary comparison data for a specific institution by unitid.

    Parameters:
    - unitid: The institution's unitid
    """
    results = await get_salary_by_enrollment(unitid=unitid)

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for unitid: {unitid}"
        )

    return results[0]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
