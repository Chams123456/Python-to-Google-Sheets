import csv
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def writing_to_csv_file (cdt):
    if os.path.isfile('my_file1.csv'):
        # If file exists then append
        print('file exists')
        with open('my_file1.csv', mode='a',newline='') as f:
            thewriter = csv.writer(f)

            for i in range((len(cdt))):
                thewriter.writerow([cdt[i]['Date'], cdt[i]['Time'], cdt[i]['Temperature'], cdt[i]['Humidity']])

    else:
        # Create new file
        print('file does not exist')
        with open('my_file1.csv', mode='w', newline='') as f:
            thewriter = csv.writer(f)

            for i in range((len(cdt))):
                thewriter.writerow([cdt[i]['Date'], cdt[i]['Time'], cdt[i]['Temperature'], cdt[i]['Humidity']])

    print('CSV file Created')



def pull_data_from_cloud():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds_sample = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds_sample)
    sheet = client.open("trial1").sheet1
    data = sheet.get_all_records()
    print('Obtained data from cloud')
    return data


cloud_data = pull_data_from_cloud()
writing_to_csv_file(cloud_data)