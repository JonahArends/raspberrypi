##### KY020 SENSOR MODDULE #####
'''Tilt sensor'''

### IMPORTS
from time import sleep
import RPi.GPIO as GPIO

### TOUCH CLASS
class TILT:
    def __init__(self, tilt_pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(tilt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.previous_state = GPIO.input(tilt_pin)
        self.tilt_pin = tilt_pin

    def observe_state(self) -> bool:
        while True:
            current_state = GPIO.input(self.tilt_pin)
            if current_state != self.previous_state:
                if current_state == GPIO.LOW:
                    return True
                self.previous_state = current_state
            sleep(0.1)

    def state(self) -> bool:
        current_state = GPIO.input(self.tilt_pin)
        if current_state != GPIO.LOW:
            return False
        return True
