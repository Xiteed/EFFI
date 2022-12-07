import requests
import pandas as pd
import csv
from datetime import datetime
import sys

sys.path.insert(0, "gpio/actuators")


URL = "https://corlysis.com:8086/query"
HEADERS = {"Accept": "application/csv"}
PARAMS = {"db": "effidb", "u": "token",
          "p": "1d612c67390c15daa4ab59dcf8016f2c",
          "q": ""}


def get_data(measurement):
    PARAMS['q'] = f"select * from {measurement}"

    response = requests.get(URL, headers=HEADERS, params=PARAMS)

    if response.status_code != 200:
        return response.content
    else:
        decoded_content = response.content.decode("UTF-8")
        data = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(data)
        df = pd.DataFrame(data_list[1:], columns=[data_list[0]])

        df = df.drop(['name', 'tags'], axis=1)

        df['time'] = df['time'].apply(lambda x: x.str.slice(0, 13))
        df['time'] = [datetime.fromtimestamp(
            int(int(t) / 1000)) for t in df['time'].squeeze()]

        return df


# if __name__ == '__main__':
#     print(get_data("temp_test"))
    #display.setText(get_data("water_test").iloc[0, 2])
