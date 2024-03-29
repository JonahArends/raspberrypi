##### RASPI RELAIS MODULE #####
'''Controll relais on raspberry pi'''

### IMPORTS
from time import sleep
import RPi.GPIO as GPIO

### LED CLASS
class RELAIS:
    def __init__(self, relais_pin: int) -> None:
        GPIO.setup(relais_pin, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)
        self.relais_pin = relais_pin

    ### RELAIS ON
    def on(self):
        GPIO.output(self.relais_pin, GPIO.HIGH)

    ### RELAIS OFF
    def off(self):
        GPIO.output(self.relais_pin, GPIO.LOW)

    ### RELAIS INTERVALL
    def intervall(self, sleeptime: float = 10):
        GPIO.output(self.relais_pin, GPIO.HIGH)
        sleep(sleeptime)
        GPIO.output(self.relais_pin, GPIO.LOW)
        sleep(sleeptime)

    ### RELAIS STATE
    def state(self):
        current_state = GPIO.input(self.relais_pin)
        if current_state == GPIO.LOW:
            return False
        return True
