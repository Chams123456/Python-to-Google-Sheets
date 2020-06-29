import serial
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def main_func():
    arduino = serial.Serial('com3', 9600)
    print('Established serial connection to Arduino')
    arduino_data = arduino.readline()
    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('x')

    for item in list_values:
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats}')

    # CALL FUNCTIONS FOR OTHER PROCESSING
    #
    
    # Push data to cloud
    # date_time_array = []
    date_time_array = get_the_date_and_time()
    push_data_to_cloud(list_in_floats, date_time_array)

    global counter
    counter += 1

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()
    print('Connection closed')
    print('<----------------------------->')


def push_data_to_cloud(push_data, date_time_list):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds_sample = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds_sample)
    sheet = client.open("TestVideo").sheet1

    # existing_data = sheet.get_all_records()
    data_to_append = [date_time_list[0], date_time_list[1], push_data[0], push_data[1]]
    sheet.append_row(data_to_append)

    print('Readings pushed to cloud')


def get_the_date_and_time():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    dt_array = dt_string.split(' ')
    return dt_array


# ----------------------------------------Main Code------------------------------------
# Declare variables to be used
list_values = []
list_in_floats = []
counter = 0

print('Program started')

# Counter - collect 62 data points and then break

# Setting up the Arduino
schedule.every(10).seconds.do(main_func)

while True:
    schedule.run_pending()

    if counter >= 60:
        break

    time.sleep(1)

print('Data collected Successfully')
