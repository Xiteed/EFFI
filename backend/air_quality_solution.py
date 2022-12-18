import json
from db_access import get_data
import weather

OPTIMAL_TEMP = 0

try:
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())
    OPTIMAL_TEMP = data_json["optimal_temp"]
except:
    OPTIMAL_TEMP = 22


def get_current_values():
    try:
        data = get_data("air_quality")
    except:
        return False
    temp = data["temperature"].iloc[-1].item()
    hum = data["humidity"].iloc[-1].item()
    gas = data["gas"].iloc[-1].item()

    data_json = {
        'temp': temp,
        'hum': hum,
        'gas': gas
    }
    return data_json


def get_optimal_ventilation_times():
    global OPTIMAL_TEMP
    temperatures = weather.get_temperature()
    temperatures = temperatures.iloc[6:23]
    avg_temperature = int(temperatures['temperature_2m'].mean())
    if (avg_temperature % 2) == 1:
        avg_temperature = avg_temperature - 1
    data_json = {}
    with open('ventilation_config.json', 'r') as file:
        data_json = json.loads(file.read())
    time_slots = data_json[str(avg_temperature)]
    return time_slots


def is_ventilation_necessary():
    air_quality = get_current_values()
    if int(air_quality["hum"]) < 40 or int(air_quality["hum"]) > 60 or int(air_quality["gas"]) > 1000:
        return True

    return False
