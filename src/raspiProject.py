##### RASPI PROJECT SCRIPT #####

### IMPORTS
from sys import argv
from multiprocessing import Process
import subprocess

from src.hardware import bmp280, ttp223, ky020
from src.hardware.leds import LED
from src.hardware.relais import RELAIS

### VARS
GPIO_PINS = {
    'RED': 1,
    'YELLOW': 2,
    'GREEN': 3,
    'ORANGE': 4,

    'TOUCH_PIN': 5,
    'TILT_PIN': 6,
    'FAN_PIN': 7,
}

### LEDS
led = LED(led_pins=[GPIO_PINS['RED'], GPIO_PINS['YELLOW'], GPIO_PINS['GREEN'], GPIO_PINS['ORANGE']])
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])

### TEMPERATURE
def temperature_tasks():
    while True:
        temperature = bmp280.get_temperature()
        if temperature < 22:
            led.off(led_pin=GPIO_PINS['RED'])
            led.off(led_pin=GPIO_PINS['YELLOW'])
            led.on(led_pin=GPIO_PINS['GREEN'])
            fan.off()
        if 22 <= temperature < 25:
            led.off(led_pin=GPIO_PINS['RED'])
            led.off(led_pin=GPIO_PINS['GREEN'])
            led.on(led_pin=GPIO_PINS['YELLOW'])
            fan.intervall()
        else:
            led.off(led_pin=GPIO_PINS['YELLOW'])
            led.off(led_pin=GPIO_PINS['GREEN'])
            led.on(led_pin=GPIO_PINS['RED'])
            fan.on()

### TOUCH
def touch_tasks():
    while True:
        if touch.observe_state():
            led.blink(led_pin=GPIO_PINS['RED'])

### TILT
def tilt_tasks():
    while True:
        if tilt.observe_state():
            led.blink(led_pin=GPIO_PINS['ORANGE'])

### MAIN
def main():
    if argv[1] in ['-t', '--test']:
        ...
    elif argv[1] in ['-h', '--healthcheck']:
        ...
    elif argv[1] in ['-a', '--api']:
        subprocess.call(['python3', 'api/main.py'], shell=True)
    else:
        temperature_process = Process(target=temperature_tasks, daemon=True)
        touch_process = Process(target=touch_tasks, daemon=True)
        tilt_process = Process(target=tilt_tasks, daemon=True)

        temperature_process.start()
        touch_process.start()
        tilt_process.start()

        temperature_process.join()
        touch_process.join()
        tilt_process.join()

### EXECUTE
if __name__ == '__main__':
    main()
