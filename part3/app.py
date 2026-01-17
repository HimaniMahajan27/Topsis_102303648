from flask import Flask, request, send_file, render_template
from topsis_himani import topsis_run
import os
import re

app = Flask(__name__)

# Folders for uploads and results
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Home page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/topsis', methods=['POST'])
def topsis_service():
    file = request.files.get('file')
    weights = request.form.get('weights')
    impacts = request.form.get('impacts')

    # Basic validation
    if not file or not weights or not impacts:
        return "File, weights and impacts are required", 400

    weights_list = weights.split(",")
    impacts_list = impacts.split(",")

    if len(weights_list) != len(impacts_list):
        return "Number of weights must equal number of impacts", 400

    for imp in impacts_list:
        if imp not in ["+", "-"]:
            return "Impacts must be + or -", 400

    # Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Generate result file
    output_filename = f"result_{file.filename}"
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    try:
        topsis_run(input_path, weights, impacts, output_path)
    except Exception as e:
        return f"Error running TOPSIS: {str(e)}", 500

    # Send file for download
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
