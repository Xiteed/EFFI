import json
import pandas as pd
from datetime import datetime
from openmeteo_py import Hourly, Daily, Options, OWmanager


def get_weather_data():
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())

    latitude = float(data_json["latitude"])
    longitude = float(data_json["longitude"])

    hourly = Hourly()
    daily = Daily()
    options = Options(latitude, longitude)

    mgr = OWmanager(options,
                    hourly.temperature_2m(),
                    daily.precipitation_sum(),
                    )

    # Download data
    meteo = mgr.get_data()
    return meteo


def get_temperature():
    meteo = get_weather_data()
    dfhourly = pd.DataFrame(meteo["hourly"])
    dfhourly["time"] = [datetime.fromisoformat(t) for t in dfhourly["time"]]
    return dfhourly.iloc[:25, :]


def get_precipiation():
    meteo = get_weather_data()
    dfdaily = pd.DataFrame(meteo["daily"])
    dfdaily["time"] = [datetime.fromisoformat(t) for t in dfdaily["time"]]
    return dfdaily["precipitation_sum"].sum()
