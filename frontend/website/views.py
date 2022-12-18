from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import sys
import geocoder

# As the dependencies below can be found in different directories, the python PATH variable needs to be adjusted
sys.path.append('/home/pi20/Documents/EFFI/backend')

import water_solution
import data_collector
import air_quality_solution

views = Blueprint('views', __name__)

CONFIG_FILE = '/home/pi20/Documents/EFFI/user_info.json'
STARTED = False


@views.route('/')
def home():
    global STARTED
    if is_user_data_set():
        vars = {'started': STARTED}
        return render_template('home.html', vars=vars)
    else:
        return redirect(url_for('views.add_config'))



@views.route('/config', methods=['GET'])
def config():
    if is_user_data_set():
        user_data = get_user_data()
        return render_template('config.html', user_data=user_data)
    else:
        return redirect(url_for('views.add_config'))


@views.route('/config/input', methods=['GET', 'POST'])
def add_config():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        roof_size = request.form.get('roof_size')
        tank_volume = request.form.get('tank_volume')
        garden_size = request.form.get('garden_size')
        if not latitude:
            flash('Latitude is required!', category='error')
        elif not longitude:
            flash('Longitude is required!', category='error')
        elif not roof_size:
            flash('Roof size is required!', category='error')
        elif not tank_volume:
            flash('Tank volume is required!', category='error')
        elif not garden_size:
            flash('Garden size is required!', category='error')
        else:
            data = {
                'latitude': latitude,
                'longitude': longitude,
                'roof_size': roof_size,
                'tank_volume': tank_volume,
                'garden_size': garden_size
            }
            safe_user_data(data)

            return redirect(url_for('views.config'))
    user_info = get_user_data()
    return render_template('config_form.html', user_info=user_info)


@views.route('/water', methods=['GET'])
def water():
    tank_level = water_solution.get_current_values()
    predicted_value = water_solution.get_predicted_water_level()
    predicted_value_with_watering = water_solution.get_predicted_water_level_with_use()
    data = {'tank_level': tank_level, 'predicted_value': predicted_value, 'predicted_value_with_watering': predicted_value_with_watering}
    if not tank_level:
        flash('Error Accessing DB', category='error')
    # data = {'tank_level': 3.5, 'predicted_value': 3.6, 'predicted_value_with_watering': 2.5}
    return render_template('water.html', water_resources_data=data)


@views.route('/heat', methods=['GET'])
def heat():
    # air_quality_data = air_quality_solution.get_current_values()
    # if not air_quality_data:
    #     flash('Error Accessing DB', category='error')
    optimal_times_arr = air_quality_solution.get_optimal_ventilation_times()
    # if not air_quality_data:
    #     flash('Error Accessing DB', category='error')
    optimal_times = {'first_slot': optimal_times_arr[0] + " - " + optimal_times_arr[1], 'second_slot': optimal_times_arr[2] + " - " + optimal_times_arr[3], 'third_slot': ''}
    if len(optimal_times_arr) == 6:
        optimal_times['third_slot'] = optimal_times_arr[4] + " - " + optimal_times_arr[5]
    air_quality_data = {'temp': 22, 'hum': 54, 'gas': 351}
    return render_template('heat.html', air_quality_data=air_quality_data, optimal_times=optimal_times)


@views.route('/start', methods=['GET'])
def start():
    global STARTED
    data_collector.start()
    STARTED = True
    return redirect(url_for('views.home'))


@views.route('/stop', methods=['GET'])
def stop():
    global STARTED
    data_collector.stop()
    STARTED = False
    return redirect(url_for('views.home'))


@views.route('/config/input/latlng', methods=['GET'])
def set_latlng():
    current_user_data = get_user_data()
    geo = geocoder.ipinfo('me')
    latlng = geo.latlng
    current_user_data['latitude'] = str(latlng[0])
    current_user_data['longitude'] = str(latlng[1])
    safe_user_data(current_user_data)
    return redirect(url_for('views.add_config'))


def get_user_data():
    global CONFIG_FILE
    with open(CONFIG_FILE, 'r') as file:
        data_json = json.loads(file.read())
        return data_json


def safe_user_data(data):
    user_data_json = json.dumps(data)
    f = open(CONFIG_FILE, mode='w')
    f.write(user_data_json)


def is_user_data_set():
    user_data = get_user_data()
    set = True
    for data in user_data.values():
        if data == "":
            set = False
            break
    return set
    