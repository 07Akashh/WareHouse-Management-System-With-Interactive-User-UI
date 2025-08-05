import requests
import json
import os

# --- Configuration ---
# To use this script, set the following environment variables:
# 1. TEABLE_API_TOKEN: Your personal access token from Teable.io.
# 2. TEABLE_BASE_ID: The ID of the base (database) where you want to create tables.
#    You can find this in the URL of your base.
API_TOKEN = os.environ.get("TEABLE_API_TOKEN", "YOUR_TEABLE_API_TOKEN")
BASE_ID = os.environ.get("TEABLE_BASE_ID", "YOUR_TEABLE_BASE_ID")
TEABLE_API_URL = "https://api.teable.io/api/base/{baseId}/table"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
}

def create_table(table_schema: dict):
    """
    Sends a request to the Teable API to create a new table.
    """
    url = TEABLE_API_URL.format(baseId=BASE_ID)
    table_name = table_schema.get('name')

    print(f"Attempting to create table: {table_name}...")

    # Check if a table with the same name already exists
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        existing_tables = response.json()
        if any(t['name'] == table_name for t in existing_tables):
            print(f"  INFO: Table '{table_name}' already exists. Skipping creation.")
            return
    except requests.exceptions.RequestException as e:
        print(f"  ERROR: Could not check for existing tables. Error: {e}")
        return

    # Create the table
    try:
        response = requests.post(url, headers=HEADERS, json=table_schema)
        response.raise_for_status()
        print(f"  SUCCESS: Table '{table_name}' created.")
    except requests.exceptions.RequestException as e:
        print(f"  ERROR: Could not create table '{table_name}'.")
        print(f"  Response: {e.response.text if e.response else 'No response'}")

    print("-" * 20)


def define_schemas():
    """
    Defines the schemas for all the tables we need in the WMS.
    The field types are based on Teable's API documentation.
    """
    products_schema = {
        "name": "Products",
        "fields": [
            {"name": "msku", "type": "singleLineText", "isPrimary": True},
            {"name": "product_name", "type": "singleLineText"},
        ]
    }

    skus_schema = {
        "name": "SKUs",
        "fields": [
            {"name": "sku", "type": "singleLineText", "isPrimary": True},
            {
                "name": "product_link",
                "type": "link",
                "options": {
                    "foreignTableId": "Products", # Link by table name
                    "relationship": "many-to-one"
                }
            }
        ]
    }

    sales_data_schema = {
        "name": "SalesData",
        "fields": [
            {"name": "order_id", "type": "singleLineText"},
            {"name": "order_date", "type": "date"},
            {"name": "quantity", "type": "number", "options": {"format": "integer"}},
            {"name": "price", "type": "number", "options": {"format": "decimal", "precision": 2}},
            {
                "name": "sku_link",
                "type": "link",
                "options": {
                    "foreignTableId": "SKUs"
                }
            }
        ]
    }
    return [products_schema, skus_schema, sales_data_schema]


if __name__ == '__main__':
    print("--- WMS Database Schema Creation Script ---")
    if API_TOKEN == "YOUR_TEABLE_API_TOKEN" or BASE_ID == "YOUR_TEABLE_BASE_ID":
        print("ERROR: Please set the TEABLE_API_TOKEN and TEABLE_BASE_ID environment variables.")
    else:
        all_schemas = define_schemas()
        for schema in all_schemas:
            create_table(schema)
        print("Schema creation script finished.")
