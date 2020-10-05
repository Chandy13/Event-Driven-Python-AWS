import requests
import csv
import datetime

CSV_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
RECOVERYCSV_URL = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

with requests.Session() as r:
    download = r.get(CSV_URL)
    recoverydownload = r.get(RECOVERYCSV_URL)

    csvdata = download.content.decode('utf-8')
    recoverycsvdata = recoverydownload.content.decode('utf-8')

    csvreaderdata = csv.reader(csvdata.splitlines(), delimiter=',')
    recoveryreaderdata = csv.reader(recoverycsvdata.splitlines(), delimiter=',')
    
    #list of data with a list of [date, cases, deaths]
    data_list = list(csvreaderdata)
    
    #remove title list and first day list to match list of recoveries
    data_list.pop(0)
    data_list.pop(0)
    
    #list of data with recoveries
    recovery_data_list = list(recoveryreaderdata)

    #create list of dates
    list_date = []
    for row in data_list:
        list_date.append(row[0])

    #create date object
    date_obj_list = []
    for day in list_date:
        #split string by hyphens
        split_list_date = day.split('-')
        #create date object using new list of string dates
        date_obj = datetime.datetime(int(split_list_date[0]),int(split_list_date[1]),int(split_list_date[2]))
        date_obj_list.append(date_obj)

    #create list of recoveries
    list_recoveries = []
    for row in recovery_data_list:
        if row[1] == 'US':
            list_recoveries.append(row[6])
    
    #append recoveries to end of data list
    counter = 0
    while len(data_list) > counter:
        data_list[counter].append(list_recoveries[counter])
        counter += 1
    #print test
    print(data_list)
