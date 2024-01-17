##### MAIN FLASK CODE #####

### IMPORTS
import threading
from time import sleep
import requests
from flask import Flask, render_template
from turbo_flask import Turbo

### VARs

### APP
app = Flask(__name__)
turbo = Turbo(app)

### UPDATE TEMPERATURE
def update_temperature():
    while True:
        response = requests.get('http://sensors-backend/temperature')
        temperature = response.text
        turbo.push(turbo.replace('temperature', temperature))
        sleep(1)

### ROUTE
@app.route('/')
def root():
    response = requests.get('http://sensors-backend/temperature')
    temperature = response.text
    return render_template('template/index.html', temperature=temperature)
