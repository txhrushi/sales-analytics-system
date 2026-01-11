"""Report generation utilities"""
from datetime import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """Generates comprehensive sales report"""
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    from utils.data_processor import (
        calculate_total_revenue, region_wise_sales, top_selling_products,
        customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('='*50 + '\n')
        f.write('SALES ANALYTICS REPORT\n')
        f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'Records Processed: {len(transactions)}\n')
        f.write('='*50 + '\n\n')
        
        # Overall Summary
        total_revenue = calculate_total_revenue(transactions)
        f.write('OVERALL SUMMARY\n')
        f.write('-'*50 + '\n')
        f.write(f'Total Revenue: ₹{total_revenue:,.2f}\n')
        f.write(f'Total Transactions: {len(transactions)}\n')
        if transactions:
            f.write(f'Average Order Value: ₹{total_revenue/len(transactions):,.2f}\n')
        dates = sorted(set([t['Date'] for t in transactions]))
        if dates:
            f.write(f'Date Range: {dates[0]} to {dates[-1]}\n')
        f.write('\n')
        
        # Region-wise Performance
        regions = region_wise_sales(transactions)
        f.write('REGION-WISE PERFORMANCE\n')
        f.write('-'*50 + '\n')
        f.write(f'{"Region":<15} {"Sales":>15} {"% Total":>10} {"Count":>8}\n')
        f.write('-'*50 + '\n')
        for region, data in regions.items():
            f.write(f'{region:<15} ₹{data["total_sales"]:>13,.0f} {data["percentage"]:>9.2f}% {data["transaction_count"]:>7}\n')
        f.write('\n')
        
        # Top Products
        top_products = top_selling_products(transactions, 5)
        f.write('TOP 5 PRODUCTS\n')
        f.write('-'*50 + '\n')
        for rank, (name, qty, revenue) in enumerate(top_products, 1):
            f.write(f'{rank}. {name:<30} Qty: {qty:>5} Rev: ₹{revenue:>10,.0f}\n')
        f.write('\n')
        
        # Top Customers
        customers = customer_analysis(transactions)
        top_customers = sorted(customers.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
        f.write('TOP 5 CUSTOMERS\n')
        f.write('-'*50 + '\n')
        for rank, (cust_id, data) in enumerate(top_customers, 1):
            f.write(f'{rank}. {cust_id:<10} Spent: ₹{data["total_spent"]:>10,.0f} Orders: {data["purchase_count"]:>3}\n')
        f.write('\n')
        
        # Daily Trend
        daily = daily_sales_trend(transactions)
        f.write('DAILY SALES TREND\n')
        f.write('-'*50 + '\n')
        f.write(f'{"Date":<15} {"Revenue":>15} {"Transactions":>15}\n')
        f.write('-'*50 + '\n')
        for date in sorted(daily.keys())[:10]:
            data = daily[date]
            f.write(f'{date:<15} ₹{data["revenue"]:>13,.0f} {data["transaction_count"]:>14}\n')
        f.write('\n')
        
        # Peak Sales Day
        peak = find_peak_sales_day(transactions)
        if peak:
            f.write('PEAK SALES DAY\n')
            f.write('-'*50 + '\n')
            f.write(f'Date: {peak[0]}\n')
            f.write(f'Revenue: ₹{peak[1]:,.0f}\n')
            f.write(f'Transactions: {peak[2]}\n')
            f.write('\n')
        
        # Low Performers
        low_prods = low_performing_products(transactions, 10)
        if low_prods:
            f.write('LOW PERFORMING PRODUCTS\n')
            f.write('-'*50 + '\n')
            for name, qty, revenue in low_prods[:5]:
                f.write(f'{name:<30} Qty: {qty:>3} Rev: ₹{revenue:>8,.0f}\n')
            f.write('\n')
        
        # API Enrichment Summary
        if enriched_transactions:
            enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
            f.write('API ENRICHMENT SUMMARY\n')
            f.write('-'*50 + '\n')
            f.write(f'Total Enriched: {enriched_count}/{len(enriched_transactions)}\n')
            if enriched_transactions:
                f.write(f'Success Rate: {enriched_count/len(enriched_transactions)*100:.1f}%\n')
            f.write('\n')
        
        f.write('='*50 + '\n')
        f.write('END OF REPORT\n')
        f.write('='*50 + '\n')
