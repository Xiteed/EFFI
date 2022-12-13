import requests
import pandas as pd
import csv
from datetime import datetime
import sys

# Declare global parameters for accessing the influxdb.
URL = "https://corlysis.com:8086/query"
HEADERS = {"Accept": "application/csv"}
PARAMS = {"db": "effidb", "u": "token",
          "p": "24378526400017a008459a68bf933251",
          "q": ""}


def get_data(measurement):
    PARAMS['q'] = f"select * from {measurement}"

    response = requests.get(URL, headers=HEADERS, params=PARAMS)

    if response.status_code != 200:
        return response.content
    else:
        # Decode the downloaded csv file and create a pandas data frame.
        decoded_content = response.content.decode('UTF-8')
        data = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(data)
        df = pd.DataFrame(data_list[1:], columns=[data_list[0]])

        # Remove unnecessary columns 'name' and 'tags'
        df = df.drop(['name', 'tags'], axis=1)

        # Convert the column 'time' to a python datetime type.
        df['time'] = df['time'].apply(lambda x: x.str.slice(0, 13))
        df['time'] = [datetime.fromtimestamp(
            int(int(t) / 1000)) for t in df['time'].squeeze()]

        return df
