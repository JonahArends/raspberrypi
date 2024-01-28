##### TTP223 SENSOR MODULE #####
'''Touch sensor'''

### IMPORTS
import RPi.GPIO as GPIO

### TOUCH CLASS
class TOUCH:
    def __init__(self, touch_pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.touch_pin = touch_pin

    def state(self) -> bool:
        current_state = GPIO.input(self.touch_pin)
        if current_state == GPIO.LOW:
            return False
        return True
