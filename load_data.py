import pandas as pd
import requests
import json
import os

# --- Configuration ---
# To use this script, set the following environment variables:
# 1. TEABLE_API_TOKEN: Your personal access token from Teable.io.
# 2. TEABLE_BASE_ID: The ID of the base (database) where you want to load data.
API_TOKEN = os.environ.get("TEABLE_API_TOKEN", "YOUR_TEABLE_API_TOKEN")
BASE_ID = os.environ.get("TEABLE_BASE_ID", "YOUR_TEABLE_BASE_ID")
TEABLE_API_URL = "https://api.teable.io/api/base/{baseId}/table/{tableId}/record"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
}

def find_record(table_id: str, query: str):
    """Finds a record in a Teable table."""
    url = TEABLE_API_URL.format(baseId=BASE_ID, tableId=table_id)
    params = {'where': json.dumps(query)}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        records = response.json().get('records', [])
        if records:
            return records[0]['id']
    except requests.exceptions.RequestException as e:
        print(f"  ERROR finding record in {table_id}: {e}")
    return None

def create_record(table_id: str, payload: dict):
    """Creates a record in a Teable table."""
    url = TEABLE_API_URL.format(baseId=BASE_ID, tableId=table_id)
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json().get('id')
    except requests.exceptions.RequestException as e:
        print(f"  ERROR creating record in {table_id}: {e.response.text}")
    return None

def load_data_to_teable(processed_filepath: str):
    """
    Loads processed sales data into the Teable database schema.
    """
    if not os.path.exists(processed_filepath):
        print(f"Error: Processed file not found at {processed_filepath}")
        return

    print(f"--- Starting Data Load for {processed_filepath} ---")
    df = pd.read_csv(processed_filepath)
    df.dropna(subset=['msku'], inplace=True)
    if len(df) == 0:
        print("No mappable data to load. Aborting.")
        return

    # 1. Upsert Products
    print("\nStep 1: Upserting Products...")
    unique_mskus = df['msku'].unique()
    for msku in unique_mskus:
        if not find_record('Products', {'msku': {'is': msku}}):
            create_record('Products', {"fields": {"msku": msku, "product_name": msku.replace('-', ' ').title()}})

    # 2. Upsert SKUs
    print("\nStep 2: Upserting SKUs...")
    unique_skus = df[['sku', 'msku']].drop_duplicates()
    for _, row in unique_skus.iterrows():
        sku, msku = row['sku'], row['msku']
        if not find_record('SKUs', {'sku': {'is': sku}}):
            create_record('SKUs', {"fields": {"sku": sku, "product_link": msku}})

    # 3. Create Sales Records
    print("\nStep 3: Creating Sales Records...")
    for _, row in df.iterrows():
        create_record('SalesData', {
            "fields": {
                "order_date": row.get('order_date'),
                "quantity": row.get('quantity'),
                "price": row.get('price'),
                "sku_link": row.get('sku')
            }
        })
    print("\n--- Data Load Finished ---")


if __name__ == '__main__':
    if API_TOKEN == "YOUR_TEABLE_API_TOKEN" or BASE_ID == "YOUR_TEABLE_BASE_ID":
        print("ERROR: Please set the TEABLE_API_TOKEN and TEABLE_BASE_ID environment variables.")
    else:
        dummy_data = {
            'order_id': [1001, 1002, 1004],
            'order_date': ['2025-08-01', '2025-08-02', '2025-08-03'],
            'sku': ['pen', 'pen-blue', 'pencil'],
            'quantity': [5, 10, 2],
            'price': [1.50, 1.40, 0.75],
            'msku': ['cste-pen', 'cste-pen', 'cste-pencil']
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_filepath = 'temp_processed_sales.csv'
        dummy_df.to_csv(dummy_filepath, index=False)

        load_data_to_teable(dummy_filepath)
        os.remove(dummy_filepath)
