import pandas as pd
import os

class SKUMapper:
    """
    Manages the mapping from SKU to MSKU.
    """
    def __init__(self, mapping_filepath: str):
        """
        Initializes the mapper by loading the mapping file.

        Args:
            mapping_filepath: The path to the SKU to MSKU mapping CSV file.
        """
        if not os.path.exists(mapping_filepath):
            self.mapping_df = None
            print(f"Error: Mapping file not found at {mapping_filepath}")
            return

        try:
            self.mapping_df = pd.read_csv(mapping_filepath)
            # For faster lookups, set the 'sku' column as the index.
            self.mapping_df.set_index('sku', inplace=True)
        except Exception as e:
            self.mapping_df = None
            print(f"An error occurred while loading the mapping file: {e}")

    def get_msku(self, sku: str) -> str | None:
        """
        Gets the MSKU for a given SKU.

        Args:
            sku: The SKU to look up.

        Returns:
            The corresponding MSKU, or None if not found.
        """
        if self.mapping_df is None:
            return None

        try:
            # Look up the SKU in the index and return the 'msku' value.
            msku = self.mapping_df.loc[sku, 'msku']
            # If a SKU maps to multiple MSKUs (e.g., duplicate rows), return the first one.
            if isinstance(msku, pd.Series):
                return msku.iloc[0]
            return msku
        except KeyError:
            # The SKU was not found in the index.
            return None

if __name__ == '__main__':
    # Example usage and testing
    # This allows the file to be run directly to test its functionality.
    print("Testing SKUMapper...")
    mapper = SKUMapper('wms_mapping.csv')

    if mapper.mapping_df is not None:
        test_skus = ['pen', 'pen-blue', 'pencil', 'non_existent_sku']
        expected_mskus = ['cste-pen', 'cste-pen', 'cste-pencil', None]

        for sku, expected in zip(test_skus, expected_mskus):
            msku = mapper.get_msku(sku)
            print(f"SKU: '{sku}' -> MSKU: '{msku}' (Expected: '{expected}')")
            assert msku == expected, f"Test failed for SKU: {sku}"

        print("\nAll tests passed!")
    else:
        print("\nCould not run tests because mapping data failed to load.")
