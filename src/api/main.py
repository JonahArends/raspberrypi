##### FASTAPI #####

### IMPORTS
import os
import signal
import subprocess
from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware

from src.hardware import bmp280, ttp223, ky020
from src.raspiProject import GPIO_PINS
from src.hardware.relais import RELAIS

### VARS
process = {'id': None}

### HARDWARE
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])

### API
api = FastAPI()

### SECURITY
'''to do'''

### START PROGRAMM
@api.websocket("/run")
async def run_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not process['id']:
        sp = subprocess.Popen(['python3', './raspiProject.py'], stdout=subprocess.PIPE)
        process['id'] = sp.pid
        while True:
            output = sp.stdout.readline().decode('utf-8')
            await websocket.send_text(output)

### STOP PROGRAMM
@api.get('/kill')
async def kill():
    if process['id']:
        os.kill(process['id'], signal.SIGTERM)
        return True
    return False

### TEST PROGRAMM
@api.websocket("/test")
async def test_endpoint(websocket: WebSocket):
    await websocket.accept()
    if process['id']:
        os.kill(process['id'], signal.SIGTERM)
    if not process['id']:
        sp = subprocess.Popen(['python3', './raspiProject.py', '--test'], stdout=subprocess.PIPE)
        process['id'] = sp.pid
        while True:
            output = sp.stdout.readline().decode('utf-8')
            await websocket.send_text(output)

### TEMPERATURE
@api.get('/temperature')
async def get_temperature():
    temperature = bmp280.get_temperature()
    return temperature

### STATE
@api.get('/state/touch')
async def get_touch_state():
    return touch.state()

@api.get('/state/tilt')
async def get_tilt_state():
    return tilt.state()

@api.get('/state/fan')
async def get_fan_state():
    return fan.state()
