##### RUN RASPI PROJECT #####

### IMPORTS
import subprocess
from threading import Thread

### START TASKS
def run_api():
    subprocess.call('python src/raspiProject.py --api', shell=True)

def run_web():
    subprocess.call('python web/main.py', shell=True)

### THREADS
api_thread = Thread(target=run_api)
web_thread = Thread(target=run_web)

api_thread.start()
web_thread.start()
