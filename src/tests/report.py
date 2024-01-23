##### UNITTEST REPORT GENERATOR #####

### IMPORTS
import csv
import os
import datetime

### VARS
FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}/reports/'
FILENAME = f'{datetime.date.today().strftime('%Y%m%d')}-{datetime.datetime.now().strftime('%H%M%S')}-report.csv'
FILE = FILEPATH+FILENAME
HEADER = ['ID', 'Test', 'Output', 'Result']

### GENERATE
def generate_csv(data:list):
    with open(FILE, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)
        for row in data:
            writer.writerow(row)

### EXECUTE
if __name__ == '__main__':
    generate_csv(data=[[1, 'bmp280', 22, 'Success']])
