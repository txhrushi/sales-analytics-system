"""Main application entry point for Sales Analytics System"""
import sys
sys.path.insert(0, '.')
from utils.file_handler import read_sales_data
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    parse_transactions
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.file_handler import validate_and_filter
from utils.report_generator import generate_sales_report

def main():
    """Main execution function"""
    print("="*50)
    print("SALES ANALYTICS SYSTEM")
    print("="*50)
    print()
    
    try:
        # Step 1: Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print()
        
        # Step 2: Parse and clean
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")
        print()
        
        # Step 3: Show filter options
        print("[3/10] Filter Options Available:")
        regions = sorted(set([t['Region'] for t in transactions]))
        amounts = sorted([t['Quantity']*t['UnitPrice'] for t in transactions])
        print(f"Regions: {', '.join(regions)}")
        if amounts:
            print(f"Amount Range: ₹{min(amounts):.0f} - ₹{max(amounts):.0f}")
        print()
        
        filter_choice = input("Do you want to filter data? (y/n): ").lower()
        if filter_choice == 'y':
            region = input(f"Enter region (or press Enter for all): ").strip() or None
            min_amt = input("Enter min amount (or press Enter for none): ").strip()
            max_amt = input("Enter max amount (or press Enter for none): ").strip()
            min_amount = float(min_amt) if min_amt else None
            max_amount = float(max_amt) if max_amt else None
            filtered, invalid, summary = validate_and_filter(
                transactions, region=region, min_amount=min_amount, max_amount=max_amount
            )
            transactions = filtered
        else:
            filtered, invalid, summary = validate_and_filter(transactions)
            transactions = filtered
        print()
        
        # Step 4: Validation
        print("[4/10] Validating transactions...")
        print(f"✓ Valid: {len(transactions)} | Invalid: {invalid}")
        print()
        
        # Step 5: Analysis
        print("[5/10] Analyzing sales data...")
        revenue = calculate_total_revenue(transactions)
        regions_data = region_wise_sales(transactions)
        top_products = top_selling_products(transactions, 5)
        customers = customer_analysis(transactions)
        daily_trend = daily_sales_trend(transactions)
        peak_day = find_peak_sales_day(transactions)
        low_performers = low_performing_products(transactions, 10)
        print("✓ Analysis complete")
        print()
        
        # Step 6: Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_map = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")
        print()
        
        # Step 7: Enrich data
        print("[7/10] Enriching sales data...")
        enriched = enrich_sales_data(transactions, product_map)
        success_rate = (sum(1 for t in enriched if t.get('API_Match')) / len(enriched) * 100) if enriched else 0
        print(f"✓ Enriched {sum(1 for t in enriched if t.get('API_Match'))}/{len(enriched)} transactions ({success_rate:.1f}%)")
        print()
        
        # Step 8: Save enriched
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched, 'output/enriched_sales_data.txt')
        print("✓ Saved to: output/enriched_sales_data.txt")
        print()
        
        # Step 9: Generate report
        print("[9/10] Generating report...")
        generate_sales_report(transactions, enriched, 'output/sales_report.txt')
        print("✓ Report saved to: output/sales_report.txt")
        print()
        
        print("[10/10] Process Complete!")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
