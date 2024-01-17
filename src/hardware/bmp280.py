##### BMP280 SENSOR MODDULE #####
'''Temperature and pressure sensor'''

### IMPORTS
import board
import adafruit_bmp280

### DEFINE SENSOR
i2c = board.I2C() # Verwendung der Standard-I2C-Bus des Boards
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)


def get_temperature() -> float:
    '''Get the temperature'''
    return sensor.temperature
