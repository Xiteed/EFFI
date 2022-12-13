import json
from db_access import get_data
import pandas as pd
from weather import get_precipiation

def get_current_values():
    df = get_data('water_resources').iloc[-1:]
    return float(df['tank_volume'].values[0])

def get_predicted_water_level():
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())

    current_value = get_current_values()
    predicted_value = current_value + get_precipiation()
    if predicted_value > float(data_json["tank_volume"]):
        return data_json["tank_volume"]
    else :
        return predicted_value

def is_watering_necessary():
    
    return 
