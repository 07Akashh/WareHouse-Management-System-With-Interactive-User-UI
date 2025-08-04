import customtkinter
from tkinter import filedialog
import os
from wms_logic import WMSLogic

class WMSApp(customtkinter.CTk):
    """
    Provides the graphical user interface for the WMS SKU Mapper.
    The core logic is handled by the WMSLogic class.
    """
    def __init__(self):
        super().__init__()

        self.title("WMS SKU Mapper")
        self.geometry("700x500")

        # --- Logic Handler ---
        self.logic = WMSLogic()

        # --- Configure grid layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Widgets ---
        self.top_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.load_button = customtkinter.CTkButton(self.top_frame, text="Load Sales Data", command=self.load_sales_data)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = customtkinter.CTkLabel(self.top_frame, text="No file loaded.", anchor="w")
        self.file_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.process_button = customtkinter.CTkButton(self, text="Process Data", command=self.process_data, state="disabled")
        self.process_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.save_button = customtkinter.CTkButton(self, text="Save Processed Data", command=self.save_processed_data, state="disabled")
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.log_textbox = customtkinter.CTkTextbox(self, width=250)
        self.log_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.log("Welcome to the WMS SKU Mapper.")
        if self.logic.mapper.mapping_df is None:
            self.log("ERROR: wms_mapping.csv not found or failed to load. Please check the file.")
            self.load_button.configure(state="disabled")

    def log(self, message):
        self.log_textbox.insert("end", str(message) + "\n")
        self.log_textbox.see("end")

    def load_sales_data(self):
        filepath = filedialog.askopenfilename(
            title="Select Sales Data File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if not filepath:
            self.log("File loading cancelled.")
            return

        success, message = self.logic.load_sales_data(filepath)
        self.log(message)

        if success:
            self.file_label.configure(text=f"Loaded: {os.path.basename(filepath)}")
            self.process_button.configure(state="normal")
            self.save_button.configure(state="disabled")
        else:
            self.file_label.configure(text="Load failed.")

    def process_data(self):
        self.log("Processing data...")
        success, message = self.logic.process_data()
        self.log(message)
        if success:
            self.save_button.configure(state="normal")

    def save_processed_data(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
            title="Save Processed File As"
        )
        if not save_path:
            self.log("Save operation cancelled.")
            return

        success, message = self.logic.save_processed_data(save_path)
        self.log(message)

if __name__ == '__main__':
    # This block launches the actual GUI application.
    # It will only work in an environment with a display.
    try:
        app = WMSApp()
        app.mainloop()
    except Exception as e:
        print(f"Could not start GUI. This is expected in a headless environment. Error: {e}")
        print("The core logic is tested in 'test_wms_logic.py'.")
