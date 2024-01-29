##### RASPI PROJECT SCRIPT #####

### IMPORTS
from argparse import ArgumentParser
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO
import subprocess
import uvicorn
import sys


sys.path.append('src/hardware')
from hardware import bmp280, ttp223, ky020
from hardware.leds import LED
from hardware.relais import RELAIS

### VARS
GPIO_PINS = {
    'RED': 20,
    'YELLOW': 16,
    'GREEN': 26,
    'ORANGE': 21,

    'TOUCH_PIN': 19,
    'TILT_PIN': 13,
    'FAN_PIN': 4}

### LEDS
led = LED(led_pins=[GPIO_PINS['RED'], GPIO_PINS['YELLOW'], GPIO_PINS['GREEN'], GPIO_PINS['ORANGE']])
touch = ttp223.TOUCH(GPIO_PINS['TOUCH_PIN'])
tilt = ky020.TILT(GPIO_PINS['TILT_PIN'])
fan = RELAIS(GPIO_PINS['FAN_PIN'])

### TEMPERATURE
def temperature_tasks():
    print('Temperature task runs')
    while True:
        #print(bmp280.get_temperature())
        temperature = bmp280.get_temperature()
        if temperature < 22:
            #print('Temperature under 22°C')
            led.off(led_pin=GPIO_PINS['RED'])
            led.off(led_pin=GPIO_PINS['YELLOW'])
            led.on(led_pin=GPIO_PINS['GREEN'])
            fan.stop_while = True
            fan.off()
        elif 22 <= temperature < 25:
            #print('Temperature between 22°C and 25°C')
            led.off(led_pin=GPIO_PINS['RED'])
            led.off(led_pin=GPIO_PINS['GREEN'])
            led.on(led_pin=GPIO_PINS['YELLOW'])
            fan.stop_while = False
            fan.intervall()
        else:
            #print('Temperature over 25°C')
            #led.stop_while = True
            led.off(led_pin=GPIO_PINS['YELLOW'])
            led.off(led_pin=GPIO_PINS['GREEN'])
            led.on(led_pin=GPIO_PINS['RED'])
            fan.stop_while = True
            fan.on()
        sleep(0.5)

### TOUCH
def touch_tasks():
    print('Touch task runs')
    while True:
        if touch.state():
            print('Sensor touched')
            led.stop_while = False
            led.blink(led_pin=GPIO_PINS['RED'])
        else:
            led.stop_while = True
        sleep(0.5)

### TILT
def tilt_tasks():
    print('Tilt task runs')
    while True:
        if not tilt.state():
            print('Sensor tilted')
            led.stop_while = False
            led.blink(led_pin=GPIO_PINS['ORANGE'])
        else:
            led.stop_while = True
            led.off(led_pin=GPIO_PINS['ORANGE'])
        sleep(0.5)

### MAIN
def main():
    parser = ArgumentParser()
    parser.add_argument("--test", action='store_true')
    parser.add_argument("--run", action='store_true')
    parser.add_argument("--kill", action='store_true')
    args = parser.parse_args()


    if args.test:
        print('Test runs')
    elif args.run:
        print('Script runs')
        temperature_thread = Thread(target=temperature_tasks, daemon=True)
        touch_thread = Thread(target=touch_tasks, daemon=True)
        tilt_thread = Thread(target=tilt_tasks, daemon=True)

        temperature_thread.start()
        touch_thread.start()
        tilt_thread.start()

        temperature_thread.join()
        touch_thread.join()
        tilt_thread.join()
    elif args.kill:
        print('Script exists')
        GPIO.cleanup()
        subprocess.run('pkill -f "raspiProject.py"', shell=True, check=True)
        #exit()

### EXECUTE
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
