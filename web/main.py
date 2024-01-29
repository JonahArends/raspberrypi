##### FLASK CODE #####

### IMPORTS
import requests
from flask import Flask, render_template, request

### VARS
API_BASE = '127.0.0.1:5000'
API_URL = f'http://{API_BASE}'

### APP
app = Flask(__name__)

### START SCRIPT
@app.route('/start', methods=['POST'])
def start_script():
    response = requests.post(f'{API_URL}/run', timeout=10)
    return str(response.status_code)

### STOP SCRIPT
@app.route('/stop', methods=['POST'])
def stop_script():
    response =requests.post(f'{API_URL}/kill', timeout=10)
    return str(response.status_code)

### TEST SCRIPT
@app.route('/test', methods=['POST'])
def test_script():
    response = requests.post(f'{API_URL}/test', timeout=10)
    return str(response.status_code)

### UPDATE TEMPERATURE
@app.route('/temperature', methods=['GET'])
def update_temperature():
    response = requests.get(f'{API_URL}/temperature', timeout=10)
    temperature = f'{response.text}°C'
    return temperature

### REPORTS LIST
@app.route('/listreports', methods=['GET'])
def list_reports():
    response = requests.get(f'{API_URL}/reports/list', timeout=10)
    data = response.txt
    return data

### DOWNLOAD REPORTS
@app.route('/download_files', methods=['POST'])
def download_files():
    checkboxes = request.get_json()
    files = []
    for checkbox in checkboxes:
        response = requests.get(f'{API_URL}/reports/' + checkbox, timeout=10)
        files.append((checkbox, response.content))
    return zip(files)

### ROOT ROUTE
@app.route('/')
def root():
    return render_template('index.html')

### RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
