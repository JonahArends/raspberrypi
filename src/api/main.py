##### FASTAPI API CODE #####

### IMPORTS
import os
import sys
import subprocess
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

sys.path.append('src/hardware')
sys.path.append('src')
from hardware import bmp280, ttp223, ky020
from raspiProject import GPIO_PINS
from hardware.relais import RELAIS
from hardware.leds import LED

### VARS
process = {'id': None}

### HARDWARE
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])
led = LED(led_pins=[GPIO_PINS['RED'], GPIO_PINS['YELLOW'], GPIO_PINS['GREEN'], GPIO_PINS['ORANGE']])

### API
app = FastAPI()

### SECURITY
'''to do'''

### RUN PROGRAMM
def run_script():
    sp = subprocess.Popen(['python3 src/raspiProject.py --run &'], shell=True, stdout=subprocess.PIPE)
    process['id'] = sp.pid
    stdout, stderr = sp.communicate()
    print(stdout.decode())

### KILL PROGRAMM
def kill_script():
    sp = subprocess.Popen(['python3 src/raspiProject.py --kill'], shell=True, stdout=subprocess.PIPE)
    sp.communicate()

### TEST PROGRAMM
def test_script():
    sp = subprocess.Popen(['python3 src/raspiProject.py --test'], shell=True, stdout=subprocess.PIPE)
    sp.communicate()

### START PROGRAMM
@app.post('/run')
def start_script(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_script)
    return {"status": "Script started"}

### STOP PROGRAMM
@app.post('/kill')
def stop_script(background_tasks: BackgroundTasks):
    background_tasks.add_task(kill_script)
    return {"status": "Script stopped"}

### TEST PROGRAMM
@app.post('/test')
def start_test_script(background_tasks: BackgroundTasks):
    background_tasks.add_task(test_script)
    return {"status": "Start test"}


### CHECK PROGRAMM STATE
@app.get('/check')
def check():
    if process['id']:
        return True
    return False

### TEMPERATURE
@app.get('/temperature')
def get_temperature():
    temperature = round(bmp280.get_temperature(), 1)
    return temperature

### STATE
@app.get('/ttp223')
def get_touch_state():
    if not touch.state():
        return False
    return True

@app.get('/ky020')
def get_tilt_state():
    if tilt.state():
        return False
    return True

@app.get('/led')
def led_state():
    return led.active()

@app.get('/fan')
def get_fan_state():
    if not fan.state():
        return False
    return True

# ### LIST REPORTS
# @app.get('/reports/list')
# def list_reports():
#     reports = os.listdir('src/tests/reports/')
#     return reports

# ### GET REPORT
# @app.get('/reports/{filename}')
# def download_report(filename: str):
#     return FileResponse(path=f'src/tests/reports/{filename}', media_type='application/octet-stream')
