import unittest
import os
import pandas as pd
from wms_logic import WMSLogic

class TestWMSLogic(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.logic = WMSLogic()
        self.dummy_output_file = 'test_processed_sales.csv'

        # Ensure dummy output file does not exist before test
        if os.path.exists(self.dummy_output_file):
            os.remove(self.dummy_output_file)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.dummy_output_file):
            os.remove(self.dummy_output_file)

    def test_full_workflow(self):
        """Test the full data processing workflow from loading to saving."""
        # For this test, we'll use the flipkart dummy file as an example
        dummy_input_file = 'dummy_fk_sales.csv'

        # 1. Test loading and processing data
        success, message = self.logic.load_and_process_sales_data(dummy_input_file)
        self.assertTrue(success, f"Failed to load and process data: {message}")
        self.assertIsNotNone(self.logic.sales_df, "sales_df should not be None after loading.")

        # 2. Test mapping data (previously called process_data)
        success, message = self.logic.process_data()
        self.assertTrue(success, f"Failed to map data: {message}")
        self.assertIsNotNone(self.logic.processed_df, "processed_df should not be None after mapping.")
        self.assertIn('msku', self.logic.processed_df.columns, "'msku' column was not created.")

        # 3. Test saving data
        success, message = self.logic.save_processed_data(self.dummy_output_file)
        self.assertTrue(success, f"Failed to save data: {message}")
        self.assertTrue(os.path.exists(self.dummy_output_file), "Output file was not created.")

        # 4. Verify output file content
        result_df = pd.read_csv(self.dummy_output_file)
        expected_mskus = ['cste-pen'] # From the 'pen-blue' sku in the dummy fk file
        actual_mskus = result_df['msku'].where(pd.notna(result_df['msku']), None).tolist()

        self.assertEqual(actual_mskus, expected_mskus, "MSKU column content mismatch.")

if __name__ == '__main__':
    unittest.main()
