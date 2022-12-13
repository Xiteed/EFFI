from db_access import get_data
import weather

OPTIMAL_TEMP = 22


def get_current_values():
    try:
        data = get_data("air_quality")
    except:
        return False
    temp = data["temperature"].iloc[-1].item()
    hum = data["humidity"].iloc[-1].item()
    gas = data["gas"].iloc[-1].item()

    # Calculate gas score.

    data_json = {
        'temp': temp,
        'hum': hum,
        'gas': gas
    }
    return data_json


def get_optimal_ventilation_times():
    global OPTIMAL_TEMP
    temperatures = weather.get_temperature()
    temperatures['temp_diff'] = OPTIMAL_TEMP - temperatures['temperature_2m']
    print(temperatures)
    avg_diff = temperatures['temperature_2m'].mean()
    print(avg_diff)
    max_diff = temperatures['temp_diff'].max()
    min_diff = temperatures['temp_diff'].min()
    temperatures['temp_diff'] = round(
        (temperatures['temp_diff'] - min_diff) / (max_diff - min_diff) * 10, 2)


def is_ventilation_necessary():
    # air_quality
    pass


get_optimal_ventilation_times()
