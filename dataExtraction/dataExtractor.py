import requests

CSV_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

with requests.Session() as r:
    download = r.get(CSV_URL)
    print(download.content)