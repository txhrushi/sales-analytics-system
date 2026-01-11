"""Data processing utilities for analysis"""
from collections import defaultdict
from datetime import datetime

def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions"""
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    """Analyzes sales by region"""
    total_revenue = calculate_total_revenue(transactions)
    region_data = defaultdict(lambda: {'total_sales': 0, 'transaction_count': 0})
    for t in transactions:
        region = t['Region']
        region_data[region]['total_sales'] += t['Quantity'] * t['UnitPrice']
        region_data[region]['transaction_count'] += 1
    result = {}
    for region, data in sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True):
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': (data['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
        }
    return result

def top_selling_products(transactions, n=5):
    """Finds top n products by total quantity sold"""
    products = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
    for t in transactions:
        prod = t['ProductName']
        products[prod]['quantity'] += t['Quantity']
        products[prod]['revenue'] += t['Quantity'] * t['UnitPrice']
    sorted_prods = sorted(products.items(), key=lambda x: x[1]['quantity'], reverse=True)[:n]
    return [(name, data['quantity'], data['revenue']) for name, data in sorted_prods]

def customer_analysis(transactions):
    """Analyzes customer purchase patterns"""
    customers = defaultdict(lambda: {'total_spent': 0, 'purchase_count': 0, 'products': set()})
    for t in transactions:
        cust = t['CustomerID']
        customers[cust]['total_spent'] += t['Quantity'] * t['UnitPrice']
        customers[cust]['purchase_count'] += 1
        customers[cust]['products'].add(t['ProductName'])
    result = {}
    for cust, data in sorted(customers.items(), key=lambda x: x[1]['total_spent'], reverse=True):
        result[cust] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': data['total_spent'] / data['purchase_count'] if data['purchase_count'] > 0 else 0,
            'products_bought': sorted(list(data['products']))
        }
    return result

def daily_sales_trend(transactions):
    """Analyzes sales trends by date"""
    daily = defaultdict(lambda: {'revenue': 0, 'transaction_count': 0, 'customers': set()})
    for t in transactions:
        date = t['Date']
        daily[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily[date]['transaction_count'] += 1
        daily[date]['customers'].add(t['CustomerID'])
    result = {}
    for date in sorted(daily.keys()):
        data = daily[date]
        result[date] = {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
    return result

def find_peak_sales_day(transactions):
    """Identifies the date with highest revenue"""
    daily = daily_sales_trend(transactions)
    if not daily:
        return None
    peak_date = max(daily.keys(), key=lambda d: daily[d]['revenue'])
    return (peak_date, daily[peak_date]['revenue'], daily[peak_date]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """Identifies products with low sales"""
    products = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
    for t in transactions:
        prod = t['ProductName']
        products[prod]['quantity'] += t['Quantity']
        products[prod]['revenue'] += t['Quantity'] * t['UnitPrice']
    low_prods = [(name, data['quantity'], data['revenue']) for name, data in products.items() if data['quantity'] < threshold]
    return sorted(low_prods, key=lambda x: x[1])
