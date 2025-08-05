from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from wms_logic import WMSLogic

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Helper Function ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---
@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')


import csv

@app.route('/mappings')
def sku_mappings():
    """Renders the page for managing SKU mappings."""
    mappings = []
    with open('wms_mapping.csv', mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for row in reader:
            mappings.append({'sku': row[0], 'msku': row[1]})
    return render_template('mappings.html', mappings=mappings)


@app.route('/add_mapping', methods=['POST'])
def add_mapping():
    """Adds a new SKU to MSKU mapping."""
    sku = request.form['sku']
    msku = request.form['msku']
    with open('wms_mapping.csv', mode='a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([sku, msku])
    return redirect(url_for('sku_mappings'))


@app.route('/delete_mapping', methods=['POST'])
def delete_mapping():
    """Deletes an SKU to MSKU mapping."""
    sku_to_delete = request.form['sku']
    rows = []
    with open('wms_mapping.csv', 'r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    with open('wms_mapping.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        for row in rows:
            if row[0] != sku_to_delete:
                writer.writerow(row)

    return redirect(url_for('sku_mappings'))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload and processing."""
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- Core Logic Integration ---
        logic = WMSLogic()

        # 1. Load and standardize the data
        load_success, load_message = logic.load_and_process_sales_data(filepath)
        if not load_success:
            # Handle error - maybe render an error page
            return f"Error loading file: {load_message}"

        # 2. Map SKUs
        map_success, map_message = logic.process_data()
        if not map_success:
            return f"Error processing file: {map_message}"

        # 3. Save the processed file for download
        processed_filename = f"processed_{filename}"
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        save_success, save_message = logic.save_processed_data(processed_filepath)
        if not save_success:
            return f"Error saving processed file: {save_message}"

        # --- Database Loading ---
        from load_data import load_data_to_teable
        # Check if Teable credentials are configured
        if os.environ.get("TEABLE_API_TOKEN") and os.environ.get("TEABLE_BASE_ID"):
            print("Attempting to load data to Teable.io...")
            load_data_to_teable(processed_filepath)
        else:
            print("Skipping Teable.io data load: TEABLE_API_TOKEN or TEABLE_BASE_ID not set.")

        # Render a results page
        return render_template('results.html',
                               original_filename=filename,
                               processed_filename=processed_filename,
                               summary_message=map_message)

    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    """Serves the processed file for download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    # Note: This is a development server.
    # For production, use a proper WSGI server like Gunicorn.
    app.run(debug=True, host='0.0.0.0', port=8080)
