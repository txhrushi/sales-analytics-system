"""API integration utilities"""
import requests

def fetch_all_products():
    """Fetches all products from DummyJSON API"""
    try:
        response = requests.get('https://dummyjson.com/products?limit=100')
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        print(f"Successfully fetched {len(products)} products from API")
        return products
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return []

def create_product_mapping(api_products):
    """Creates a mapping of product IDs to product info"""
    mapping = {}
    for prod in api_products:
        mapping[prod['id']] = {
            'title': prod.get('title', ''),
            'category': prod.get('category', ''),
            'brand': prod.get('brand', ''),
            'rating': prod.get('rating', 0)
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API product information"""
    enriched = []
    for trans in transactions:
        enriched_trans = trans.copy()
        prod_id_str = trans['ProductID'].replace('P', '')
        try:
            prod_id = int(prod_id_str)
            if prod_id in product_mapping:
                prod_info = product_mapping[prod_id]
                enriched_trans['API_Category'] = prod_info['category']
                enriched_trans['API_Brand'] = prod_info['brand']
                enriched_trans['API_Rating'] = prod_info['rating']
                enriched_trans['API_Match'] = True
            else:
                enriched_trans['API_Category'] = None
                enriched_trans['API_Brand'] = None
                enriched_trans['API_Rating'] = None
                enriched_trans['API_Match'] = False
        except:
            enriched_trans['API_Category'] = None
            enriched_trans['API_Brand'] = None
            enriched_trans['API_Rating'] = None
            enriched_trans['API_Match'] = False
        enriched.append(enriched_trans)
    return enriched

def save_enriched_data(enriched_transactions, filename='output/enriched_sales_data.txt'):
    """Saves enriched transactions back to file"""
    import os
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        header = ['TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand', 'API_Rating', 'API_Match']
        f.write('|'.join(header) + '\n')
        for trans in enriched_transactions:
            row = [
                str(trans.get('TransactionID', '')),
                str(trans.get('Date', '')),
                str(trans.get('ProductID', '')),
                str(trans.get('ProductName', '')),
                str(trans.get('Quantity', '')),
                str(trans.get('UnitPrice', '')),
                str(trans.get('CustomerID', '')),
                str(trans.get('Region', '')),
                str(trans.get('API_Category', '')),
                str(trans.get('API_Brand', '')),
                str(trans.get('API_Rating', '')),
                str(trans.get('API_Match', ''))
            ]
            f.write('|'.join(row) + '\n')
