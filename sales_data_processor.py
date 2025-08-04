import pandas as pd

# Define the expected columns for each marketplace to help with detection
AMAZON_COLS = {'FNSKU', 'Event Type', 'Reference ID'}
FK_COLS = {'Order State', 'FSN', 'Shipment ID'}
MEESHO_COLS = {'Sub Order No', 'Packet Id', 'Supplier Listed Price (Incl. GST + Commission)'}

STANDARDIZED_COLS = ['order_date', 'sku', 'quantity']

def detect_format(columns: set) -> str | None:
    """Detects the marketplace format based on the given column headers."""
    if AMAZON_COLS.issubset(columns):
        return 'amazon'
    if FK_COLS.issubset(columns):
        return 'flipkart'
    if MEESHO_COLS.issubset(columns):
        return 'meesho'
    return None

def parse_amazon(df: pd.DataFrame) -> pd.DataFrame:
    """Parses an Amazon sales DataFrame into the standardized format."""
    # The 'MSKU' column from Amazon seems to be the SKU we need to map
    df_renamed = df.rename(columns={'Date': 'order_date', 'MSKU': 'sku', 'Quantity': 'quantity'})
    return df_renamed[STANDARDIZED_COLS]

def parse_flipkart(df: pd.DataFrame) -> pd.DataFrame:
    """Parses a Flipkart sales DataFrame into the standardized format."""
    df_renamed = df.rename(columns={'Ordered On': 'order_date', 'SKU': 'sku', 'Quantity': 'quantity'})
    return df_renamed[STANDARDIZED_COLS]

def parse_meesho(df: pd.DataFrame) -> pd.DataFrame:
    """Parses a Meesho sales DataFrame into the standardized format."""
    df_renamed = df.rename(columns={'Order Date': 'order_date', 'SKU': 'sku', 'Quantity': 'quantity'})
    return df_renamed[STANDARDIZED_COLS]

def process_sales_file(filepath: str) -> pd.DataFrame | None:
    """
    Detects the format of a sales file, parses it, and returns a
    standardized DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        columns = set(df.columns)
        file_format = detect_format(columns)

        if file_format == 'amazon':
            return parse_amazon(df)
        elif file_format == 'flipkart':
            return parse_flipkart(df)
        elif file_format == 'meesho':
            return parse_meesho(df)
        else:
            print(f"Error: Could not determine file format for {filepath}")
            return None
    except Exception as e:
        print(f"An error occurred while processing {filepath}: {e}")
        return None

if __name__ == '__main__':
    print("--- Testing Sales Data Processor ---")

    files_to_test = {
        'amazon': 'dummy_amazon_sales.csv',
        'flipkart': 'dummy_fk_sales.csv',
        'meesho': 'dummy_meesho_sales.csv'
    }

    all_passed = True
    for format_name, filepath in files_to_test.items():
        print(f"\n[Test] Processing {format_name} file: {filepath}")
        processed_df = process_sales_file(filepath)

        if processed_df is not None:
            print("Processing successful. Standardized DataFrame:")
            print(processed_df.head())

            # Check if columns are standardized
            if list(processed_df.columns) != STANDARDIZED_COLS:
                print(f"FAIL: Columns are not standardized. Got {list(processed_df.columns)}")
                all_passed = False
            else:
                print("PASS: Columns are standardized.")

            # Check if data is present
            if len(processed_df) == 0:
                print("FAIL: DataFrame is empty.")
                all_passed = False
            else:
                print("PASS: Data is present.")
        else:
            print("FAIL: Processing returned None.")
            all_passed = False

    print("\n--- Test Summary ---")
    if all_passed:
        print("All sales data processor tests passed successfully!")
    else:
        print("One or more tests failed.")
