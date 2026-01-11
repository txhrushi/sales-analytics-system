# Sales Analytics System

Sales Analytics System - Python Data Processing, API Integration, and Report Generation Assignment

## Overview

This project implements a comprehensive Sales Analytics System that processes sales data, integrates with external APIs, performs deep analysis, and generates detailed reports. It's designed to handle data quality issues, perform complex calculations, and enrich data with external information.

## Features

### Part 1: File Handling & Preprocessing (30 points)
- **Encoding Handling**: Reads files with multiple encoding support (UTF-8, Latin-1, CP1252)
- **Data Parsing**: Splits pipe-delimited data and handles formatting issues
- **Data Validation**: Validates transactions based on strict criteria
- **Filtering**: Supports region-based and amount-based filtering

### Part 2: Data Processing (25 points)
- **Sales Summary**: Calculates total revenue, region-wise sales, top products
- **Customer Analysis**: Analyzes purchase patterns and customer lifetime value
- **Date-based Trends**: Tracks daily sales patterns and identifies peak sales days
- **Product Performance**: Identifies low-performing products

### Part 3: API Integration (20 points)
- **DummyJSON API**: Fetches product information from external API
- **Data Enrichment**: Enriches sales transactions with API product details
- **Error Handling**: Graceful error handling for API failures
- **Data Mapping**: Creates efficient product ID to info mappings

### Part 4: Report Generation (15 points)
- **Comprehensive Reports**: Generates detailed formatted text reports
- **Multiple Sections**: Summary, regions, products, customers, trends, analysis
- **Professional Formatting**: Well-structured, readable output
- **Metrics Calculation**: All calculations verified for accuracy

### Part 5: Main Application (10 points)
- **User Interaction**: Interactive prompts for filtering options
- **Workflow Execution**: 10-step process with progress tracking
- **Error Handling**: Comprehensive exception handling
- **File Management**: Automatic directory creation and file handling

## Project Structure

```
sales-analytics-system/
├── README.md                          # This file
├── main.py                            # Main application entry point
├── requirements.txt                   # Python dependencies
├── utils/
│   ├── file_handler.py               # File I/O and validation
│   ├── data_processor.py             # Data analysis functions
│   ├── api_handler.py                # API integration
│   └── report_generator.py           # Report generation
├── data/
│   └── sales_data.txt                # Input sales data file
└── output/
    ├── enriched_sales_data.txt       # Enriched transactions output
    └── sales_report.txt              # Generated report
```

## Installation

### Requirements
- Python 3.7+
- requests library (for API calls)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/txhrushi/sales-analytics-system.git
cd sales-analytics-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Prepare your data file:
- Place `sales_data.txt` in the `data/` directory
- Ensure the file is pipe-delimited with the format: `TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region`

## Usage

### Running the Application

```bash
python main.py
```

The application will:
1. Read and parse the sales data
2. Display available filter options
3. Prompt for filtering preferences (optional)
4. Validate all transactions
5. Perform comprehensive analysis
6. Fetch product data from DummyJSON API
7. Enrich transactions with API information
8. Generate detailed report
9. Save all outputs to respective files

### Features During Execution

- **Progress Tracking**: Real-time updates on processing status
- **User Prompts**: Interactive options for data filtering
- **Error Handling**: Graceful handling of missing files or API errors
- **Auto-completion**: Automatic creation of output directories

## Output Files

### enriched_sales_data.txt
Pipe-delimited file containing:
- Original transaction fields
- API_Category, API_Brand, API_Rating (from external API)
- API_Match flag (True/False indicating successful enrichment)

### sales_report.txt
Formatted report including:
- **Overall Summary**: Total revenue, transactions, average order value, date range
- **Region-wise Performance**: Sales by region with percentages
- **Top 5 Products**: Best-selling products by quantity
- **Top 5 Customers**: Highest-value customers
- **Daily Sales Trend**: Revenue and transaction count by date
- **Peak Sales Day**: Date with highest revenue
- **Low Performing Products**: Products below threshold
- **API Enrichment Summary**: Success rate of API enrichment

## Data Processing Details

### Encoding Handling
- Automatically detects and handles multiple encodings
- Falls back gracefully if primary encoding fails
- Supports UTF-8, Latin-1, and CP1252 encodings

### Data Cleaning
- Removes commas from numeric values
- Removes commas from product names
- Validates all required fields
- Filters out invalid records:
  - Quantity ≤ 0
  - UnitPrice ≤ 0
  - Missing CustomerID or Region
  - Invalid ID formats (must start with correct prefix: T, P, C)

### Validation Rules
- TransactionID must start with 'T'
- ProductID must start with 'P'
- CustomerID must start with 'C'
- Quantity must be > 0
- UnitPrice must be > 0
- All required fields must be present

## API Integration

### DummyJSON API
- **Endpoint**: https://dummyjson.com/products
- **Method**: GET
- **Limit**: 100 products
- **Response Fields Used**: id, title, category, brand, rating

### Enrichment Logic
- Extracts numeric ID from ProductID (e.g., P101 → 101)
- Maps to API product information if available
- Sets API_Match flag based on availability
- Handles missing products gracefully

## Error Handling

- **File Not Found**: Clear error message, graceful exit
- **API Failures**: Returns empty list, continues with available data
- **Data Parsing Errors**: Skips invalid records, logs count
- **Encoding Issues**: Automatically tries alternative encodings
- **Invalid Data**: Validates and removes corrupted records

## Performance

- **File Reading**: Efficient line-by-line processing
- **Data Structures**: Uses defaultdict for aggregation
- **API Calls**: Single batch call with limit=100
- **Memory**: Optimized for datasets up to 10,000+ records

## Testing Checklist

- [x] File reading with multiple encodings
- [x] Data parsing and cleaning
- [x] Transaction validation
- [x] Region-wise analysis
- [x] Product analysis
- [x] Customer analysis
- [x] Date-based trends
- [x] API integration
- [x] Data enrichment
- [x] Report generation
- [x] User interaction
- [x] Error handling

## Grading Criteria (100 points)

- Part 1 (File Handling): 30 points
- Part 2 (Data Processing): 25 points
- Part 3 (API Integration): 20 points
- Part 4 (Report Generation): 15 points
- Part 5 (Main Application): 10 points

## Author

Tx Hrushi

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the assignment documentation or contact the course instructor.
