from db_access import get_data
# from weather import get_daily_temperatures


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
    pass


def is_ventilation_necessary():
    pass
