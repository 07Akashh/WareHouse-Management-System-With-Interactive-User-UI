import pandas as pd
from sku_mapper import SKUMapper
from sales_data_processor import process_sales_file
import os

class WMSLogic:
    """
    Handles the core business logic for the WMS application,
    independent of the GUI.
    """
    def __init__(self):
        self.mapper = SKUMapper('wms_mapping.csv')
        self.sales_df = None
        self.processed_df = None
        self.unmapped_skus = []

    def load_and_process_sales_data(self, filepath: str) -> tuple[bool, str]:
        """
        Loads and processes a sales data file using the flexible processor.

        Args:
            filepath: The path to the sales data CSV.

        Returns:
            A tuple (success, message).
        """
        if not os.path.exists(filepath):
            return False, "Error: File not found."

        # Use the new processor to get a standardized DataFrame
        standardized_df = process_sales_file(filepath)

        if standardized_df is None:
            return False, f"Error: Could not process file '{os.path.basename(filepath)}'. The format might be unsupported."

        self.sales_df = standardized_df
        return True, f"Successfully processed {os.path.basename(filepath)}."

    def process_data(self) -> tuple[bool, str]:
        """
        Processes the loaded sales data by mapping SKUs to MSKUs.

        Returns:
            A tuple (success, message).
        """
        if self.sales_df is None:
            return False, "Error: No sales data loaded to process."

        if self.mapper.mapping_df is None:
            return False, "Error: SKU mapping data is not available."

        self.processed_df = self.sales_df.copy()
        self.processed_df['msku'] = self.processed_df['sku'].apply(self.mapper.get_msku)

        mapped_count = self.processed_df['msku'].notna().sum()
        total_count = len(self.processed_df)

        self.unmapped_skus = self.processed_df[self.processed_df['msku'].isna()]['sku'].unique()

        message = f"Processing complete. Mapped {mapped_count} of {total_count} records."
        if len(self.unmapped_skus) > 0:
            message += f"\nFound {len(self.unmapped_skus)} unmapped SKUs: {', '.join(map(str, self.unmapped_skus))}"

        return True, message

    def save_processed_data(self, filepath: str) -> tuple[bool, str]:
        """
        Saves the processed DataFrame to a CSV file.

        Args:
            filepath: The path to save the new CSV file.

        Returns:
            A tuple (success, message).
        """
        if self.processed_df is None:
            return False, "Error: No processed data to save."

        try:
            self.processed_df.to_csv(filepath, index=False)
            return True, f"Successfully saved processed data to: {filepath}"
        except Exception as e:
            return False, f"Error saving file: {e}"
