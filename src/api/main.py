##### FASTAPI API CODE #####

### IMPORTS
import os
import sys
import signal
import subprocess
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

sys.path.append('src/hardware')
from hardware import bmp280, ttp223, ky020
from raspiProject import GPIO_PINS
from hardware.relais import RELAIS

### VARS
process = {'id': None}

### HARDWARE
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])

### API
app = FastAPI()

### SECURITY
'''to do'''

### START PROGRAMM
@app.websocket("/run")
async def run_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not process['id']:
        sp = subprocess.Popen(['python3 src/raspiProject.py --run &'], stdout=subprocess.PIPE)
        process['id'] = sp.pid
        while True:
            output = sp.stdout.readline().decode('utf-8')
            await websocket.send_text(output)

### STOP PROGRAMM
@app.post('/kill')
async def kill():
    subprocess.call(['python3 src/raspiProject.py --kill'], shell=True)
    return True

### CHECK PROGRAMM STATE
@app.get('/check')
async def check():
    if process['id']:
        return True
    return False

### TEST PROGRAMM
@app.websocket("/test")
async def test_endpoint(websocket: WebSocket):
    await websocket.accept()
    if process['id']:
        os.kill(process['id'], signal.SIGTERM)
    if not process['id']:
        sp = subprocess.Popen(['python3 ./raspiProject.py --test'], stdout=subprocess.PIPE)
        process['id'] = sp.pid
        while True:
            output = sp.stdout.readline().decode('utf-8')
            await websocket.send_text(output)

### LIST REPORTS
@app.get('/reports/list')
async def list_reports():
    reports = os.listdir('src/tests/reports/')
    return reports

### GET REPORT
@app.get('/reports/{filename}')
async def download_report(filename: str):
    return FileResponse(path=f'src/tests/reports/{filename}', media_type='application/octet-stream')

### TEMPERATURE
@app.get('/temperature')
async def get_temperature():
    temperature = round(bmp280.get_temperature(), 1)
    return temperature

### STATE
@app.get('/state/touch')
async def get_touch_state():
    return touch.state()

@app.get('/state/tilt')
async def get_tilt_state():
    return tilt.state()

@app.get('/state/fan')
async def get_fan_state():
    return fan.state()
