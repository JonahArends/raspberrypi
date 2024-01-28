##### FLASK CODE #####

### IMPORTS
import requests
import websocket
import aiohttp
import asyncio
from flask import Flask, render_template, request
from flask_sock import Sock

### VARS
API_BASE = '127.0.0.1:5000'
API_URL = f'http://{API_BASE}'

### APP
app = Flask(__name__)
sock = Sock(app)

### FETCH
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
    
async def update_temperature():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'{API_URL}/temperature')
        temperature = f'{html}°C'
        return temperature

### START SCRIPT
@sock.route('/start')
def start_script(ws):
    ws_url = f"ws://{API_BASE}/run"
    ws_client = websocket.create_connection(ws_url)
    while True:
        message = ws_client.recv()
        if not ws_client.closed:
            ws.send(message)
        else:
            print("WebSocket connection closed")
            break

### STOP SCRIPT
@app.route('/stop', methods=['POST'])
def stop_script():
    requests.post(f'{API_URL}/kill', timeout=10)

### TEST SCRIPT
@sock.route('/test')
def test_script(ws):
    ws_url = f"ws://{API_BASE}/test"
    ws_client = websocket.create_connection(ws_url)
    while True:
        message = ws_client.recv()
        if not ws_client.closed:
            ws.send(message)
        else:
            print("WebSocket connection closed")
            break

### UPDATE TEMPERATURE
@app.route('/temperature', methods=['GET'])
def update_temperature():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(update_temperature())
    loop.close()
    return result

### REPORTS LIST
@app.route('/listreports', methods=['GET'])
def list_reports():
    response = requests.get(f'{API_URL}/reports/list', timeout=60)
    data = response.txt
    return data

### DOWNLOAD REPORTS
@app.route('/download_files', methods=['POST'])
def download_files():
    checkboxes = request.get_json()
    files = []
    for checkbox in checkboxes:
        response = requests.get(f'{API_URL}/reports/' + checkbox, timeout=60)
        files.append((checkbox, response.content))
    return zip(files)

### ROOT ROUTE
@app.route('/')
def root():
    return render_template('index.html')

### RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
