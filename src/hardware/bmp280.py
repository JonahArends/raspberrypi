##### BMP280 SENSOR MODDULE #####
'''Temperature and pressure sensor'''

### IMPORTS
import board
import busio
import adafruit_bmp280

### DEFINE SENSOR
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)


def get_temperature() -> float:
    '''Get the temperature'''
    return sensor.temperature
