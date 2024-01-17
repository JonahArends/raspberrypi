##### FASTAPI #####

### IMPORTS
import os
import signal
import subprocess
from multiprocessing import process
from fastapi import FastAPI
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
@api.get('/run')
async def run():
    if not process['id']:
        sp = subprocess.Popen(['python3', './raspiProject.py'])
        process['id'] = sp.pid
        return True
    return False

### STOP PROGRAMM
@api.get('/kill')
async def kill():
    if process['id']:
        os.kill(process['id'], signal.SIGTERM)
        return True
    return False

### TEST PROGRAMM
@api.get('/test')
async def test():
    if process['id']:
        os.kill(process['id'], signal.SIGTERM)
    if not process['id']:
        sp = subprocess.Popen(['python3', './raspiProject.py', '--test'])
        process['id'] = sp.pid

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
