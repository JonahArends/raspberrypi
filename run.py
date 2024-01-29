##### RUN RASPI PROJECT #####

### IMPORTS
import subprocess
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

### START TASKS
def run_api():
    subprocess.call('uvicorn host=0.0.0.0 port=5000 src.api.main:app', shell=True)

def run_web():
    subprocess.call('gunicorn -w 4 -b 0.0.0.0:8000 web.main:app', shell=True)

### THREADS
def main():
    api_thread = Thread(target=run_api)
    web_thread = Thread(target=run_web)

    api_thread.start()
    sleep(1)
    web_thread.start()

### EXECUTE
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
