#!/bin/bash
# Setup script for Acadexis Salary Report Generator

echo "================================================"
echo "Acadexis Salary Report Generator - Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo ""

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (y/n): " create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment created and activated"
fi

echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Dependencies installed successfully!"
echo ""

# Create config file
if [ ! -f "config.ini" ]; then
    echo "Creating configuration file..."
    cp config.ini.example config.ini
    echo "Config file created: config.ini"
    echo "IMPORTANT: Edit config.ini with your database credentials"
else
    echo "Config file already exists: config.ini"
fi

echo ""

# Create reports directory
if [ ! -d "reports" ]; then
    echo "Creating reports directory..."
    mkdir reports
    echo "Reports directory created"
else
    echo "Reports directory already exists"
fi

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit config.ini with your PostgreSQL database credentials"
echo "2. Set up your PostgreSQL database:"
echo "   psql -U postgres -d acadexis_db -f schema.sql"
echo "3. (Optional) Place your Acadexis logo in this directory"
echo "4. Run the report generator:"
echo "   python generate_salary_report.py"
echo ""
echo "For more information, see README.md"
echo ""
