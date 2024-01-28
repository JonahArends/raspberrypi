##### KY020 SENSOR MODDULE #####
'''Tilt sensor'''

### IMPORTS
import RPi.GPIO as GPIO

### TOUCH CLASS
class TILT:
    def __init__(self, tilt_pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(tilt_pin, GPIO.IN) #, pull_up_down=GPIO.PUD_UP)
        self.tilt_pin = tilt_pin

    def state(self) -> bool:
        current_state = GPIO.input(self.tilt_pin)
        if current_state == GPIO.LOW:
            return False
        return True
