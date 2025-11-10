# Acadexis Salary Comparison API

FastAPI application that exposes salary comparison data from PostgreSQL database.

## Features

- Get salary comparison data by enrollment category
- Filter by institution (unitid), state, or enrollment category
- Async PostgreSQL database connection with connection pooling
- CORS support for cross-origin requests
- Health check endpoint

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 3. Run the API

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **GET** `/` - API information and available endpoints

### Health Check
- **GET** `/health` - Check API and database connection status

### Salary Data Endpoints

#### Get All Salary Data
- **GET** `/salary-by-enrollment`
- Returns all salary comparison data

**Query Parameters:**
- `unitid` (optional): Filter by specific institution unitid
- `state` (optional): Filter by state abbreviation (e.g., "CA", "NY")
- `enrollment_category` (optional): Filter by enrollment size
  - `Small (<5k Enrollment)`
  - `Medium (5k–20k Enrollment)`
  - `Large (20k+ Enrollment)`

**Example Requests:**
```bash
# Get all data
curl http://localhost:8000/salary-by-enrollment

# Get data for California
curl http://localhost:8000/salary-by-enrollment?state=CA

# Get data for large institutions
curl http://localhost:8000/salary-by-enrollment?enrollment_category=Large%20(20k%2B%20Enrollment)

# Get data for specific institution
curl http://localhost:8000/salary-by-enrollment?unitid=110635
```

#### Get Salary Data by Institution ID
- **GET** `/salary-by-enrollment/{unitid}`
- Returns salary data for a specific institution

**Example:**
```bash
curl http://localhost:8000/salary-by-enrollment/110635
```

## Response Format

```json
{
  "unitid": 110635,
  "school": "University of California-Los Angeles",
  "state": "CA",
  "enrollment": 45000,
  "enrollment_category": "Large (20k+ Enrollment)",
  "employee_count": 325,
  "median_salary": 128000.00,
  "state_median_salary": 115000.00,
  "percent_diff_from_state_category": 11.30
}
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Integration with PDF Generator

Update the PDF generator script ([marketing/generate_salary_pdfs.py](../marketing/generate_salary_pdfs.py)) to use this API:

```python
API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    'enrollment': '/salary-by-enrollment',
}
```

## Database Requirements

This API expects the following PostgreSQL tables:
- `employee_details`
- `departments`
- `working_titles`
- `carnegie_institutions`
- `carnegie_enrollment_data`

The query is based on the enrollment query from `customize statistics/sql_scripts.sql`.

## Development

The API uses:
- **FastAPI** - Modern, fast web framework
- **asyncpg** - Async PostgreSQL driver
- **Pydantic** - Data validation
- **uvicorn** - ASGI server
