"""File handling utilities for reading and validating sales data"""
import os

def read_sales_data(filename):
    """Reads sales data from file handling encoding issues"""
    try:
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for enc in encodings:
            try:
                with open(filename, 'r', encoding=enc) as f:
                    lines = f.readlines()
                lines = [line.strip() for line in lines if line.strip()]
                if lines:
                    return lines[1:] if lines[0].startswith('TransactionID') else lines
                return lines
            except UnicodeDecodeError:
                continue
        raise FileNotFoundError(f"Could not read {filename}")
    except FileNotFoundError as e:
        print(f"File not found: {filename}")
        raise

def parse_transactions(raw_lines):
    """Parses raw lines into clean list of dictionaries"""
    transactions = []
    for line in raw_lines:
        try:
            parts = line.split('|')
            if len(parts) < 8:
                continue
            qty_str = parts[4].replace(',', '')
            price_str = parts[5].replace(',', '')
            trans = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', ' ').strip(),
                'Quantity': int(qty_str),
                'UnitPrice': float(price_str),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            transactions.append(trans)
        except (ValueError, IndexError):
            continue
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """Validates and filters transactions"""
    valid = []
    invalid = 0
    for t in transactions:
        if (t['Quantity'] > 0 and t['UnitPrice'] > 0 and 
            t['CustomerID'] and t['Region'] and
            t['TransactionID'].startswith('T') and
            t['ProductID'].startswith('P') and
            t['CustomerID'].startswith('C')):
            valid.append(t)
        else:
            invalid += 1
    filtered = valid
    if region:
        filtered = [t for t in filtered if t['Region'] == region]
    if min_amount or max_amount:
        filtered = [t for t in filtered if
                   (not min_amount or t['Quantity']*t['UnitPrice'] >= min_amount) and
                   (not max_amount or t['Quantity']*t['UnitPrice'] <= max_amount)]
    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'filtered_by_region': len(valid) - len(filtered) if region else 0,
        'final_count': len(filtered)
    }
    return filtered, invalid, summary
