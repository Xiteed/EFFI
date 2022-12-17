import json
import datetime
from db_access import get_data
import pandas as pd
from weather import get_precipiation


def get_current_values():
    # df = get_data('water_resources').iloc[-1:]
    # return float(df['tank_volume'].values[0])
    return {'tank_level': 2.05, 'moisture': 'OK'}


def get_predicted_water_level():
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())

    current_value = get_current_values()['tank_level']
    predicted_value = current_value + get_precipiation()
    if predicted_value > float(data_json["tank_volume"]):
        return data_json["tank_volume"]
    else:
        return predicted_value


def get_water_need():
    data_json = {}
    with open('water_config.json', 'r') as file:
        data_json = json.loads(file.read())
    mydate = datetime.datetime.now()
    water_need = float(data_json[mydate.strftime("%B")]) - get_precipiation()
    return water_need


def get_predicted_water_level_with_use():
    if is_watering_necessary():
        return get_predicted_water_level() - get_water_need()
    else:
        return get_predicted_water_level()


def is_watering_necessary():
    if get_water_need() > 0:
        return True
    else:
        return False
