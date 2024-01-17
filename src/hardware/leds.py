##### RASPI LED MODULE #####
''''''

### IMPORTS
from time import sleep
import RPi.GPIO as GPIO

### LED CLASS
class LED:
    def __init__(self, led_pins: list) -> None:
        for led_pin in led_pins:
            GPIO.setup(led_pin, GPIO.OUT)
        self.stop_while: bool = False

    ### LED ON
    def on(self, *, led_pin: int, stop_while: bool = False):
        self.stop_while = stop_while
        GPIO.setup(led_pin, GPIO.HIGH)

    ### LED OFF
    def off(self, *, led_pin: int, stop_while: bool = False):
        self.stop_while = stop_while
        GPIO.setup(led_pin, GPIO.LOW)

    ### LED BLINK
    def blink(self, *, led_pin: int, sleeptime: float = 0.5, stop_while: bool = False):
        self.stop_while = stop_while
        while not self.stop_while:
            GPIO.setup(led_pin, GPIO.HIGH)
            sleep(sleeptime)
            GPIO.setup(led_pin, GPIO.LOW)
            sleep(sleeptime)
