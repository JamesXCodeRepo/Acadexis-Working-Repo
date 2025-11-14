# Dashboard Generation - Quick Start Guide

## TL;DR

Use the **DASHBOARD_PROMPT.md** file to generate PDF dashboards from school salary data.

---

## Quick Steps

### 1. Prepare Your Data
Create a CSV file with this structure:

```csv
school,state,enrollment,enrollment_category,employee_count,school_median_salary,schools_in_category,category_median_salary,percent_diff_from_category_median,percent_diff
Stanford University,CA,16000,Medium (5k–20k Enrollment),245,145000.00,25,105000.00,38.10,38.10
Harvard University,MA,21000,Medium (5k–20k Enrollment),312,156000.00,18,140000.00,11.43,11.43
```

### 2. Copy & Paste the Prompt

Go to [DASHBOARD_PROMPT.md](DASHBOARD_PROMPT.md) and copy the entire content.

### 3. Provide Data to Claude

Paste the prompt + your data in a Claude conversation:

```
[Paste DASHBOARD_PROMPT.md]

Here's my school data:

school,state,enrollment,...
[your data rows]

Please generate the dashboard script.
```

### 4. Run the Generated Script

Claude will generate a Python script. Save it and run:

```bash
python generate_school_dashboards.py --input school_data.csv
```

### 5. Check Output

Look in the `salary_dashboards/` folder for PDFs (one per school):
- `Stanford_University_salary_dashboard.pdf`
- `Harvard_University_salary_dashboard.pdf`
- etc.

---

## Data Fields Explained

| Field | Example | Description |
|-------|---------|-------------|
| `school` | "Stanford University" | Institution name |
| `state` | "CA" | Two-letter state code |
| `enrollment` | 16000 | Total student enrollment |
| `enrollment_category` | "Medium (5k–20k Enrollment)" | Size category |
| `employee_count` | 245 | Faculty sample size |
| `school_median_salary` | 145000.00 | School's median salary |
| `schools_in_category` | 25 | How many schools in same category/state |
| `category_median_salary` | 105000.00 | Median for all schools in category |
| `percent_diff_from_category_median` | 38.10 | % diff: school vs category |
| `percent_diff` | 38.10 | Alternative % diff (if different) |

---

## What Each Dashboard Shows

### Header
- School name (large, bold)
- State, enrollment size, enrollment category
- Employee count
- Generation date
- Dark gradient background (navy blue)

### Middle Section (Chart + Stats)
**Left side (60% width):**
- Dumbbell chart comparing school vs category median
- Green line if school is above
- Red line if school is below
- Salary values clearly labeled

**Right side (40% width):**
- Statistics box with:
  - School median salary
  - Category median salary
  - Dollar difference
  - Percentage difference
  - Number of schools in category
  - Employee count

### Footer
- Attribution: "Acadexis Salary Benchmarking Report | Confidential"
- Dark gradient background (matches header)

---

## Customization Options

Pass these in your prompt to Claude:

```
Customizations:
- Change header text color to gold
- Add school logo in top-right
- Use a different color scheme (provide hex codes)
- Include additional metrics
- Export as PNG in addition to PDF
```

---

## Troubleshooting

**Issue:** "Missing columns" error
- **Solution:** Check that all required columns are in your CSV (see Data Fields table above)

**Issue:** PDFs look different each time
- **Solution:** This is normal if styling_config.json is being modified. Check that colors match your brand

**Issue:** Script doesn't generate any PDFs
- **Solution:** Check that input CSV has valid data and correct column names

**Issue:** Salary values show as "$0" or incorrect format
- **Solution:** Ensure salary columns are numeric, not text. Remove commas from numbers in CSV

---

## File Structure

After running the script, you'll have:

```
marketing/
├── generate_school_dashboards.py    (generated script)
├── school_data.csv                  (your input data)
├── styling_config.json              (uses existing config)
├── salary_dashboards/               (output folder)
│   ├── Stanford_University_salary_dashboard.pdf
│   ├── Harvard_University_salary_dashboard.pdf
│   └── ... (more PDFs, one per school)
└── DASHBOARD_PROMPT.md              (this file)
```

---

## Example Output

Each PDF will be a professional, print-ready report showing:
- School name and location
- Comparison to peers in same enrollment category
- Salary metrics with visual dumbbell chart
- All relevant statistics
- Professional styling with colors from your guide

---

## Contact/Support

If you need modifications to the generated script:
1. Describe the change you want
2. Paste the relevant code section
3. Ask Claude to update it

The script is designed to be customizable and maintainable!