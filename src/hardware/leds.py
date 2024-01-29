##### RASPI LED MODULE #####
'''Controll LEDs on raspberry pi'''

### IMPORTS
from time import sleep
import RPi.GPIO as GPIO

### LED CLASS
class LED:
    def __init__(self, led_pins: list) -> None:
        GPIO.setmode(GPIO.BCM)
        self.led_pins = led_pins
        for led_pin in self.led_pins:
            GPIO.setup(led_pin, GPIO.OUT)
        self.stop_while: bool = False

    ### LED ON
    def on(self, *, led_pin: int):
        GPIO.output(led_pin, GPIO.HIGH)

    ### LED OFF
    def off(self, *, led_pin: int):
        GPIO.output(led_pin, GPIO.LOW)

    ### LED BLINK
    def blink(self, *, led_pin: int, sleeptime: float = 0.5):
        while not self.stop_while:
            GPIO.output(led_pin, GPIO.HIGH)
            sleep(sleeptime)
            GPIO.output(led_pin, GPIO.LOW)
            sleep(sleeptime)

    ### CHECK LED
    def active(self):
        inactive_leds = {}
        for led_pin in self.led_pins:
            current_state = GPIO.output(led_pin)
            if current_state == GPIO.LOW:
                inactive_leds[led_pin] = True
            inactive_leds[led_pin] = False
        return inactive_leds
