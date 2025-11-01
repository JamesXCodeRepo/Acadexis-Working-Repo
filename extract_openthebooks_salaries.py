"""
OpenTheBooks Salary Data Extractor - CONTENT-BASED PAGINATION
Uses intelligent content comparison to detect when pagination should stop

Key Innovation: Compares actual extracted data between pages instead of 
trying to find pagination buttons. If data is identical, we've reached the end.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse
import os
import hashlib

def setup_driver():
    """Initialize Chrome WebDriver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_page_content_hash(page_data):
    """
    Create a hash of the page content to detect duplicates
    
    Args:
        page_data: List of dictionaries containing row data
    
    Returns:
        Hash string representing the content
    """
    if not page_data:
        return None
    
    # Create a string representation of the data (excluding Page field)
    content_str = ""
    for row in page_data:
        # Sort keys to ensure consistent ordering
        sorted_items = sorted([(k, v) for k, v in row.items() if k != 'Page'])
        content_str += str(sorted_items)
    
    # Return hash of content
    return hashlib.md5(content_str.encode()).hexdigest()

def pages_are_identical(current_data, previous_data):
    """
    Compare two pages of data to see if they're identical
    
    Args:
        current_data: List of dicts from current page
        previous_data: List of dicts from previous page
    
    Returns:
        bool: True if pages contain identical data
    """
    if not current_data or not previous_data:
        return False
    
    # Check if record counts match
    if len(current_data) != len(previous_data):
        return False
    
    # Compare hashes
    current_hash = get_page_content_hash(current_data)
    previous_hash = get_page_content_hash(previous_data)
    
    return current_hash == previous_hash

def extract_page_data(soup, year, state, employer_name, page_num, stored_headers):
    """
    Extract data from a single page
    
    Returns:
        tuple: (page_data, headers) - list of dicts and header list
    """
    page_data = []
    
    # Find tables
    tables = soup.find_all('table')
    
    if not tables:
        return page_data, stored_headers
    
    # Process tables
    for table in tables:
        rows = table.find_all('tr')
        
        # Extract headers if not already stored
        if stored_headers is None and rows:
            header_row = rows[0]
            stored_headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        
        # Extract data rows (skip first row if it's a header)
        start_idx = 1 if stored_headers else 0
        for row_idx, row in enumerate(rows[start_idx:], start=1):
            try:
                cols = row.find_all('td')
                
                # Skip if this is a header row or not enough columns
                if row.find_all('th') or len(cols) < 3:
                    continue
                
                row_data = {
                    'Year': year,
                    'State': state,
                    'Employer': employer_name,
                    'Source': 'OpenTheBooks.com',
                    'Page': page_num
                }
                
                # Extract column data
                for col_idx, col in enumerate(cols):
                    col_text = col.get_text(strip=True)
                    
                    if stored_headers and col_idx < len(stored_headers):
                        header = stored_headers[col_idx]
                        row_data[header] = col_text
                    else:
                        row_data[f'Column_{col_idx}'] = col_text
                
                page_data.append(row_data)
                    
            except Exception as e:
                continue
    
    return page_data, stored_headers

def try_click_next(driver):
    """
    Attempt to click the next page button using multiple methods
    
    Returns:
        bool: True if click was attempted, False otherwise
    """
    try:
        # Try multiple XPath patterns for next button
        xpaths = [
            "//a[@rel='next']",
            "//a[contains(@class, 'next') and not(contains(@class, 'disabled'))]",
            "//li[contains(@class, 'next') and not(contains(@class, 'disabled'))]/a",
            "//a[contains(text(), 'Next') and not(contains(@class, 'disabled'))]",
            "//a[contains(text(), '›') and not(contains(@class, 'disabled'))]",
        ]
        
        for xpath in xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                
                for elem in elements:
                    if elem.is_displayed():
                        # Check if disabled
                        classes = elem.get_attribute('class') or ''
                        if 'disabled' in classes.lower():
                            continue
                        
                        # Try to click
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                        time.sleep(1)
                        elem.click()
                        time.sleep(4)
                        return True
            except:
                continue
        
        return False
    except:
        return False

def extract_salary_data(driver, state, year, employer_name):
    """
    Extract salary data with content-based pagination detection
    
    Args:
        driver: Selenium WebDriver instance
        state: State name (e.g., "Connecticut") 
        year: Year to extract data for (e.g., 2024)
        employer_name: Institution name
    
    Returns:
        pandas DataFrame with salary data
    """
    
    # Format state name for URL
    state_url = state.lower().replace(' ', '-')
    encoded_employer = urllib.parse.quote(employer_name)
    url = f"https://www.openthebooks.com/{state_url}-state-employees/?Year_S={year}&Emp_S={encoded_employer}"
    
    print(f"\n🌐 Fetching: {url}")
    print(f"   State: {state} | Employer: {employer_name} | Year: {year}")
    driver.get(url)
    
    # Wait for table to load
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        print("   ✓ Table found")
        time.sleep(5)
    except TimeoutException:
        print("   ⚠️  Timeout waiting for table")
        time.sleep(10)
    
    # Initialize tracking variables
    all_data = []
    page_num = 1
    max_pages = 50
    stored_headers = None
    previous_page_data = None
    consecutive_duplicates = 0
    max_consecutive_duplicates = 2  # Stop after 2 identical pages in a row
    
    print(f"\n{'='*70}")
    print(f"📊 Starting extraction with content-based pagination detection")
    print(f"{'='*70}")
    
    while page_num <= max_pages:
        print(f"\n📄 PAGE {page_num}")
        print(f"{'─'*70}")
        
        # Get page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract data from current page
        current_page_data, stored_headers = extract_page_data(
            soup, year, state, employer_name, page_num, stored_headers
        )
        
        # Display headers on first page
        if page_num == 1 and stored_headers:
            print(f"📝 Headers: {stored_headers}")
        
        records_count = len(current_page_data)
        print(f"📋 Extracted {records_count} records from page {page_num}")
        
        # Check if page is empty
        if records_count == 0:
            print(f"⚠️  No data on page {page_num} - stopping")
            break
        
        # CONTENT COMPARISON: Check if this page is identical to previous page
        if previous_page_data is not None:
            if pages_are_identical(current_page_data, previous_page_data):
                consecutive_duplicates += 1
                print(f"⚠️  Page {page_num} is IDENTICAL to page {page_num - 1}")
                print(f"   Duplicate count: {consecutive_duplicates}/{max_consecutive_duplicates}")
                
                if consecutive_duplicates >= max_consecutive_duplicates:
                    print(f"🛑 Stopping: Detected {consecutive_duplicates} consecutive duplicate pages")
                    print(f"   This indicates we've reached the end or pagination is stuck")
                    break
            else:
                # Pages are different - reset duplicate counter
                consecutive_duplicates = 0
                print(f"✓ Page {page_num} contains NEW data")
        
        # Add current page data to total
        all_data.extend(current_page_data)
        print(f"📊 Total records so far: {len(all_data)}")
        
        # Store current page data for next comparison
        previous_page_data = current_page_data.copy()
        
        # Try to go to next page
        print(f"\n🔍 Attempting to navigate to page {page_num + 1}...")
        clicked = try_click_next(driver)
        
        if not clicked:
            print(f"✓ Could not find next button - assuming last page")
            break
        
        print(f"✓ Clicked next button, waiting for page to load...")
        
        page_num += 1
        
        # Safety check
        if page_num > max_pages:
            print(f"\n⚠️  Reached maximum page limit ({max_pages})")
            break
    
    print(f"\n{'='*70}")
    print(f"✅ EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"📊 Total unique records extracted: {len(all_data)}")
    print(f"📄 Pages processed: {page_num - consecutive_duplicates}")
    
    return pd.DataFrame(all_data)

def clean_salary_column(df):
    """Clean and convert salary column to numeric values"""
    salary_cols = [col for col in df.columns if any(keyword in col.lower() 
                   for keyword in ['wage', 'salary', 'pay', 'compensation', 'annual'])]
    
    if salary_cols:
        primary_salary_col = salary_cols[0]
        df['Annual_Wages'] = df[primary_salary_col]
        df['Annual_Wages_Numeric'] = df['Annual_Wages'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
        
        try:
            df['Annual_Wages_Numeric'] = pd.to_numeric(df['Annual_Wages_Numeric'], errors='coerce')
        except:
            pass
    
    return df

def extract_all_schools(state, schools_list, year, output_dir='output'):
    """Extract salary data for multiple schools"""
    
    os.makedirs(output_dir, exist_ok=True)
    driver = setup_driver()
    results = {}
    
    try:
        for school_idx, school in enumerate(schools_list, 1):
            print(f"\n{'='*80}")
            print(f"🏫 SCHOOL {school_idx}/{len(schools_list)}: {school}")
            print(f"{'='*80}")
            
            df = extract_salary_data(driver, state, year, school)
            
            if not df.empty:
                # Clean salary data
                df = clean_salary_column(df)
                
                # Remove duplicate records (just in case)
                original_count = len(df)
                df = df.drop_duplicates()
                if len(df) < original_count:
                    print(f"\n🧹 Removed {original_count - len(df)} duplicate records")
                
                # Save to CSV
                safe_name = school.replace(' ', '_').replace('/', '_')
                filename = f"{output_dir}/{safe_name}_{year}_salaries.csv"
                df.to_csv(filename, index=False)
                
                print(f"\n💾 Saved {len(df)} records to {filename}")
                
                # Print statistics
                if 'Annual_Wages_Numeric' in df.columns:
                    print(f"\n💰 Salary Statistics for {school}:")
                    print(f"   Number of Employees: {len(df)}")
                    valid_salaries = df['Annual_Wages_Numeric'].dropna()
                    if len(valid_salaries) > 0:
                        print(f"   Highest Salary: ${valid_salaries.max():,.2f}")
                        print(f"   Lowest Salary: ${valid_salaries.min():,.2f}")
                        print(f"   Average Salary: ${valid_salaries.mean():,.2f}")
                        print(f"   Median Salary: ${valid_salaries.median():,.2f}")
                
                # Show page distribution
                if 'Page' in df.columns:
                    print(f"\n📄 Records per page:")
                    for page, count in df['Page'].value_counts().sort_index().items():
                        print(f"   Page {page}: {count} records")
                
                results[school] = len(df)
            else:
                print(f"\n❌ No data found for {school}")
                results[school] = 0
            
            # Delay between schools
            time.sleep(3)
    
    finally:
        driver.quit()
    
    return results

def main():
    """Main execution function"""
    print("="*80)
    print("🔍 OpenTheBooks Extractor - CONTENT-BASED PAGINATION")
    print("="*80)
    print("\nKey Feature: Uses intelligent content comparison to detect")
    print("when to stop pagination, rather than relying on button detection.")
    print("="*80)
    
    # USER PARAMETERS
    STATE = "Kentucky"
    SCHOOLS = [
        "University of Louisville"
    ]


    YEAR = 2024
    OUTPUT_DIR = "output"
    
    print(f"\n📋 Extraction Parameters:")
    print(f"   State: {STATE}")
    print(f"   Year: {YEAR}")
    print(f"   Number of Schools: {len(SCHOOLS)}")
    print(f"   Output Directory: {OUTPUT_DIR}")
    
    print(f"\n🏫 Schools to process:")
    for idx, school in enumerate(SCHOOLS, 1):
        print(f"   {idx}. {school}")
    
    print(f"\n{'='*80}")
    print("🚀 Starting extraction...")
    print(f"{'='*80}")
    
    # Run extraction
    results = extract_all_schools(STATE, SCHOOLS, YEAR, OUTPUT_DIR)
    
    # Print final summary
    print(f"\n{'='*80}")
    print("🎉 EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print("\n📊 Results Summary:")
    total_records = 0
    for school, count in results.items():
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {school}: {count} records")
        total_records += count
    
    print(f"\n📈 Total Records Extracted: {total_records}")
    print(f"📁 CSV files saved to: {OUTPUT_DIR}/")
    
    print("\n📄 Generated Files:")
    for school in SCHOOLS:
        safe_name = school.replace(' ', '_').replace('/', '_')
        filename = f"{safe_name}_{YEAR}_salaries.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"   ✓ {filename} ({file_size:.1f} KB)")

if __name__ == "__main__":
    main()
