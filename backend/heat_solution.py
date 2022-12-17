import json
from db_access import get_data
import weather

data_json = {}
with open('user_info.json', 'r') as file:
    data_json = json.loads(file.read())
OPTIMAL_TEMP = data_json["optimal_temp"]

def get_current_values():
    # try:
    #     data = get_data("air_quality")
    # except:
    #     return False
    # temp = data["temperature"].iloc[-1].item()
    # hum = data["humidity"].iloc[-1].item()
    # gas = data["gas"].iloc[-1].item()

    # # Calculate gas score.

    # data_json = {
    #     'temp': temp,
    #     'hum': hum,
    #     'gas': gas
    # }
    data_json = {
        'temp': 22,
        'hum': 54,
        'gas': 352
    }
    return data_json

def get_optimal_ventilation_times():
    global OPTIMAL_TEMP
    temperatures = weather.get_temperature()
    temperatures = temperatures.iloc[6:23]
    temperatures = temperatures['temperature_2m'].mean()
    temperatures = int(temperatures)
    if (temperatures%2) == 1:
        temperatures = temperatures - 1
    data_json = {}
    with open('ventilation_config.json', 'r') as file:
        data_json = json.loads(file.read())
    time_slots = data_json[str(temperatures)]
    return time_slots

def is_ventilation_necessary():
    # air_quality
    if get_current_values["hum"] < 40 or get_current_values["hum"] > 60 or get_current_values["gas"] < 1000 or get_current_values["gas"] > 2000:
        return True
 
    return False

# get_optimal_ventilation_times()
