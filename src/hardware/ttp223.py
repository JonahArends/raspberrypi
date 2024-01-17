##### TTP223 SENSOR MODULE #####
'''Touch sensor'''

### IMPORTS
from time import sleep
import RPi.GPIO as GPIO

### TOUCH CLASS
class TOUCH:
    def __init__(self, touch_pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.previous_state = GPIO.input(touch_pin)
        self.touch_pin = touch_pin

    def observe_state(self) -> bool:
        while True:
            current_state = GPIO.input(self.touch_pin)
            if current_state != self.previous_state:
                if current_state == GPIO.LOW:
                    return True
                self.previous_state = current_state
            sleep(0.1)

    def state(self) -> bool:
        current_state = GPIO.input(self.touch_pin)
        if current_state != GPIO.LOW:
            return False
        return True
