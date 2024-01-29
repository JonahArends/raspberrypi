##### FASTAPI API CODE #####

### IMPORTS
import os
import sys
import signal
import select
import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

sys.path.append('src/hardware')
sys.path.append('src')
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
@app.post('/run')
async def run():
    sp = subprocess.call(['python3 src/raspiProject.py --run'], shell=True)
    return True

### STOP PROGRAMM
@app.post('/kill')
async def kill():
    sp = subprocess.call(['python3 src/raspiProject.py --kill'], shell=True)
    return True

### TEST PROGRAMM
@app.post('/test')
async def test():
    sp = subprocess.call(['python3 src/raspiProject.py --test'], shell=True)
    return True

### CHECK PROGRAMM STATE
@app.get('/check')
async def check():
    if process['id']:
        return True
    return False

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
