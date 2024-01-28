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

### START SCRIPT
@sock.route('/start')
async def start_script(ws):
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
async def stop_script():
    requests.post(f'{API_URL}/kill', timeout=10)
    return True

### TEST SCRIPT
@sock.route('/test')
async def test_script(ws):
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
async def update_temperature():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_URL}/temperature') as resp:
            temperature = f'{await resp.text()}°C'
            return temperature

### REPORTS LIST
@app.route('/listreports', methods=['GET'])
async def list_reports():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_URL}/reports/list') as resp:
            data = await resp.text()
            return data

### DOWNLOAD REPORTS
@app.route('/download_files', methods=['POST'])
async def download_files():
    checkboxes = request.get_json()
    files = []
    async with aiohttp.ClientSession() as session:
        for checkbox in checkboxes:
            async with session.get(f'{API_URL}/reports/' + checkbox) as resp:
                files.append((checkbox, await resp.read()))
    return zip(files)

### ROOT ROUTE
@app.route('/')
async def root():
    return render_template('index.html')

### RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
