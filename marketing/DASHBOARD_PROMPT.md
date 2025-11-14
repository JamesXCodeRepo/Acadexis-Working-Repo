# PDF Dashboard Generation Prompt

## Instructions for Claude

You are tasked with generating professional PDF salary comparison dashboards using Python. I will provide you with salary data and you should create a comprehensive visualization script that generates beautiful, publication-ready PDFs.

---

## Data Structure

I will provide data in the following format (one record per school):

```
school | state | enrollment | enrollment_category | employee_count | school_median_salary | schools_in_category | category_median_salary | percent_diff_from_category_median | percent_diff
```

**Field Descriptions:**
- `school`: School/institution name (e.g., "University of California-Berkeley", "Stanford University")
- `state`: Two-letter state abbreviation (e.g., "CA", "NY")
- `enrollment`: Numeric enrollment size (e.g., 15000, 28000)
- `enrollment_category`: Text category (e.g., "Small (<5k Enrollment)", "Medium (5k–20k Enrollment)", "Large (20k+ Enrollment)")
- `employee_count`: Number of faculty members in sample
- `school_median_salary`: Median salary for this specific school
- `schools_in_category`: Number of schools in this enrollment category within the state
- `category_median_salary`: Median salary for all schools in this category within the state
- `percent_diff_from_category_median`: Percentage difference from category median (school vs category)
- `percent_diff`: Alternative/additional percentage difference field (use if different from above)

---

## Dashboard Requirements

### Layout & Design
- **Page Size**: Letter size (11" × 8.5")
- **Resolution**: 300 DPI for print quality
- **Color Scheme**: Apply professional styling from [marketing/styling_config.json](styling_config.json)
- **Structure**:
  1. **Header Section** (12% of page height): Dark gradient background with school/category info
  2. **Content Section** (82% of page height): Charts and statistics
  3. **Footer Section** (6% of page height): Dark gradient with attribution

### Header Section
- Display school name prominently
- Show state, enrollment size, and enrollment category
- Show employee count (sample size)
- Use dark navy gradient (#1a3a5c to #2d5a7b)
- White text for contrast
- Example: "Stanford University | CA | 16,000 students | Medium (5k–20k Enrollment)"

### Content Section
Should include multiple visualizations:

1. **Primary Chart (60% of width)**:
   - **Dumbbell/Lollipop Chart** comparing school median salary vs category median salary
   - Horizontal layout with salary on x-axis
   - Green connecting line if school is above category median
   - Red connecting line if school is below category median
   - Two dots: one for school median (blue), one for category median (gray)
   - Clear salary values labeled above each dot (e.g., "$128,000")
   - Labels below dots identifying each value

2. **Statistics Box (40% of width)**:
   - School Median Salary
   - Category Median Salary (not state median - this is category/enrollment-level)
   - Dollar Difference
   - Percentage Difference from Category Median
   - Enrollment Category
   - Number of Schools in Category
   - Employee Count (sample size)

### Footer Section
- Dark gradient background matching header
- Attribution text: "Acadexis Salary Benchmarking Report | Confidential"
- Light gray text

---

## Technical Specifications

### Libraries
Use the following Python libraries:
- `pandas`: Data manipulation
- `matplotlib`: Visualization
- `numpy`: Numerical operations
- `pathlib`: File handling
- `json`: Configuration loading

### Color Palette (from styling_config.json)
```json
{
  "background_primary": "#1a3a5c",
  "background_secondary": "#2d5a7b",
  "text_primary": "#ffffff",
  "text_secondary": "#e8f4f8",
  "chart_background": "#f5f5f5",
  "positive": "#2ecc71",
  "negative": "#e74c3c"
}
```

### Typography
- **Headers**: 24-28pt, bold, white text
- **Subheaders**: 14pt, light text
- **Chart Titles**: 14pt, bold, dark text
- **Statistics Labels**: 10pt, bold
- **Statistics Values**: 11pt, normal weight

---

## Output Format

Generate a Python script that:

1. **Accepts input data** as:
   - CSV file
   - JSON
   - Pandas DataFrame
   - Command-line arguments

2. **Produces output**:
   - One PDF per school (one PDF per row of data)
   - Files saved to `salary_dashboards/` folder
   - Filename format: `{school_name}_salary_dashboard.pdf` (e.g., `Stanford_University_salary_dashboard.pdf`)

3. **Includes error handling**:
   - Missing data validation
   - File path creation
   - Graceful fallbacks

4. **Provides feedback**:
   - Console output showing progress
   - Summary of generated files
   - Any warnings or errors

---

## Example Data Input

```
school,state,enrollment,enrollment_category,employee_count,school_median_salary,schools_in_category,category_median_salary,percent_diff_from_category_median,percent_diff
University of California-Los Angeles,CA,45000,Large (20k+ Enrollment),325,128000.00,42,115000.00,11.30,11.30
University of California-Davis,CA,38000,Large (20k+ Enrollment),268,120000.00,42,115000.00,4.35,4.35
Columbia University,NY,28000,Medium (5k–20k Enrollment),145,87000.00,18,83000.00,4.82,4.82
University of Texas at Austin,TX,12000,Medium (5k–20k Enrollment),76,74000.00,21,71000.00,4.23,4.23
Stanford University,CA,16000,Medium (5k–20k Enrollment),245,145000.00,25,105000.00,38.10,38.10
```

---

## Customization Options

The script should support:
1. **Custom color schemes** via configuration file (already provided: `styling_config.json`)
2. **Custom fonts** (default: sans-serif)
3. **Multiple chart types** (dumbbell/lollipop is primary, bar chart optional)
4. **Additional metrics display** (optional comparison tables, trend data)
5. **Export formats** (PDF primary, PNG optional)
6. **Logo/branding insertion** (optional)

---

## Deliverables

When providing the script, include:

1. **Main Python script** (`generate_school_dashboards.py`)
2. **Configuration file** (use existing `styling_config.json` or create dashboard-specific config)
3. **README** with usage instructions
4. **Example data file** (CSV format matching example above)
5. **Sample output** (example PDF for one school)

---

## Success Criteria

The generated PDFs should:
- ✓ Display all school data clearly and accurately
- ✓ Compare school median salary vs category median salary prominently
- ✓ Use professional colors and typography from styling guide
- ✓ Have proper alignment and spacing (header/content/footer)
- ✓ Be print-ready at 300 DPI
- ✓ Load configuration from external file (styling_config.json)
- ✓ Generate one PDF per school
- ✓ Handle missing/invalid data gracefully
- ✓ Complete batch processing in reasonable time
- ✓ Show percentage difference clearly (green if above, red if below)
- ✓ Include all metadata: enrollment size, employee count, schools in category

---

## Key Notes

- **One PDF per school**: Each row of input data = one complete dashboard PDF
- **Category-level comparison**: School vs category median (not state median)
- **Dumbbell chart focus**: Primary visualization should be the salary comparison chart
- **All fields required**: Every input field should appear somewhere on the dashboard
- **Professional styling**: Follow the color palette and typography from `styling_config.json`

---

## How to Use This Prompt

### Step 1: Prepare Your Data
Format your data as CSV with these columns (in any order):
```
school, state, enrollment, enrollment_category, employee_count, school_median_salary,
schools_in_category, category_median_salary, percent_diff_from_category_median, percent_diff
```

### Step 2: Copy the Prompt
Copy this entire document and paste it in your Claude conversation.

### Step 3: Provide Your Data
Add a message like:

```
[Paste DASHBOARD_PROMPT.md content above]

Here's my school salary data in CSV format:

school,state,enrollment,enrollment_category,employee_count,school_median_salary,schools_in_category,category_median_salary,percent_diff_from_category_median,percent_diff
University of California-Los Angeles,CA,45000,Large (20k+ Enrollment),325,128000.00,42,115000.00,11.30,11.30
University of California-Davis,CA,38000,Large (20k+ Enrollment),268,120000.00,42,115000.00,4.35,4.35
Stanford University,CA,16000,Medium (5k–20k Enrollment),245,145000.00,25,105000.00,38.10,38.10
[... more rows ...]

Please generate the dashboard generation script now.
```

### Step 4: Customize (Optional)
If you want specific customizations, mention them:

```
Additional requirements:
- Use company logo in top-right corner
- Add a page break between different states
- Include a summary comparison table at the end
- Export both PDF and PNG versions
```

### Step 5: Use the Generated Script
The script will create individual PDF dashboards in a `salary_dashboards/` folder, one per school.