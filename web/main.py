##### FLASK CODE #####

### IMPORTS
import requests
from flask import Flask, render_template

### VARs

### APP
app = Flask(__name__)

### UPDATE TEMPERATURE
def update_temperature():
    while True:
        response = requests.get('http://sensors-backend/temperature')
        temperature = response.text
        return temperature

### ROUTE
@app.route('/')
def root():
    response = requests.get('http://sensors-backend/temperature')
    temperature = f'{response.text}°C'
    return render_template('template/index.html', temperature=temperature)

### RUN APP
if __name__ == '__main__':
    app.run()
