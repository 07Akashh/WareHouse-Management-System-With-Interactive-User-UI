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

        # --- Database Loading Placeholder ---
        # In a real application, this is where you would call the database loading logic.
        # from load_data import load_data_to_teable
        # print("Placeholder: Would now call load_data_to_teable(...)")

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
