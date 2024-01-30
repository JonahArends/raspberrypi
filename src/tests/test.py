##### MAIN RASPIPROJECT TEST #####

### IMPORTS
import sys

sys.path.append('src/hardware')
sys.path.append('src')
from hardware import bmp280, ttp223, ky020
from raspiProject import GPIO_PINS
from hardware.relais import RELAIS
from hardware.leds import LED

### HARDWARE
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])
led = LED(led_pins=[GPIO_PINS['RED'], GPIO_PINS['YELLOW'], GPIO_PINS['GREEN'], GPIO_PINS['ORANGE']])

### TEMPERATURE TEST
def temperature_test(temperature):
    print('Temperature test runs')
    if temperature < 22:
        # print('Temperature under 22°C')
        led.off(led_pin=GPIO_PINS['RED'])
        led.off(led_pin=GPIO_PINS['YELLOW'])
        led.on(led_pin=GPIO_PINS['GREEN'])
        fan.stop_while = True
        fan.off()
    elif temperature < 25:
        # print('Temperature between 22°C and 25°C')
        led.off(led_pin=GPIO_PINS['RED'])
        led.off(led_pin=GPIO_PINS['GREEN'])
        led.on(led_pin=GPIO_PINS['YELLOW'])
        fan.stop_while = False
        fan.intervall()
    else:
        # print('Temperature over 25°C')
        led.off(led_pin=GPIO_PINS['YELLOW'])
        led.off(led_pin=GPIO_PINS['GREEN'])
        led.on(led_pin=GPIO_PINS['RED'])
        fan.stop_while = True
        fan.on()


