import requests
import csv

CSV_URL = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'

def dataManipulation():
    with requests.Session() as r:

        #download CSV data
        download = r.get(CSV_URL)

        #decode into utf-8 format
        csvdata = download.content.decode('utf-8')

        #run through csv conversion
        csvreaderdata = csv.reader(csvdata.splitlines(), delimiter=',')
        
        #convert csv data into list 
        big_data_list = list(csvreaderdata)

        #remove title list and first + 2nd day list of no data
        big_data_list.pop(0) #remove titles
        big_data_list.pop(0) #remove first row of no data
        big_data_list.pop(0) #remove second row of no data

        data_list = []
        
        #filter out unnecessary data
        for row in big_data_list:
            day_list = []
            day_list.append(row[0]) #date
            day_list.append(row[7]) #cases
            if row[6] == '':
                day_list.append('0')
            else:
                day_list.append(row[6]) #deaths
            if row[5] == '':
                day_list.append('0')
            else:
                day_list.append(row[5]) #recoveries
            data_list.append(day_list)

        #create list of cases
        list_cases = []
        for row in data_list:
            list_cases.append(int(row[1]))
        
        #create list of new cases
        list_new_cases = ['1']
        case_counter = 1
        while len(list_cases) > case_counter:
            list_new_cases.append(str(list_cases[case_counter] - list_cases[case_counter - 1]))
            case_counter += 1

        #create list of deaths
        list_deaths = []
        for row in data_list:
            if row[2] == '':
                list_deaths.append('0')
            else:
                list_deaths.append(int(row[2]))
        
        #create list of new deaths
        list_new_deaths = ['0']
        death_counter = 1
        while len(list_deaths) > death_counter:
            list_new_deaths.append(str(int(list_deaths[death_counter]) - int(list_deaths[death_counter - 1])))
            death_counter += 1

        #create list of recoveries
        list_recoveries = []
        for row in data_list:
            if row[3] == '':
                list_recoveries.append('0')
            else:
                list_recoveries.append(row[3])

        #create list of new recoveries
        list_new_recoveries = ['0']
        recovery_counter = 1
        while len(list_recoveries) > recovery_counter:
            list_new_recoveries.append(str(int(list_recoveries[recovery_counter]) - int(list_recoveries[recovery_counter - 1])))
            recovery_counter += 1
        
        #append new calculated lists to daily case
        final_counter = 0
        while len(data_list) > final_counter:
            data_list[final_counter].append(list_new_cases[final_counter])
            data_list[final_counter].append(list_new_deaths[final_counter])
            data_list[final_counter].append(list_new_recoveries[final_counter])
            final_counter += 1
    
    return data_list