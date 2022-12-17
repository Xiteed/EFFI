import json
import datetime
from db_access import get_data
import pandas as pd
from weather import get_precipiation

# returns current tank level and moisture status 
def get_current_values():
    df = get_data('water_resources').iloc[-1:]
    tank_level = round(float(df['tank_volume'].values[0]), 2)
    return {'tank_level': tank_level, 'moisture': 'OK'}


def get_predicted_water_level():
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())

    current_value = get_current_values()['tank_level']
    predicted_value = current_value + get_precipiation() * float(data_json["roof_size"])
    if predicted_value > float(data_json["tank_volume"]):
        return data_json["tank_volume"]
    else:
        return round(predicted_value, 2)


def get_water_need():
    data_json = {}
    with open('water_config.json', 'r') as file:
        data_json = json.loads(file.read())
    mydate = datetime.datetime.now()
    water_need = float(data_json[mydate.strftime("%B")]) - get_precipiation()
    return round(water_need, 2)


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

get_current_values()