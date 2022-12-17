from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import sys
import geocoder

# As the dependencies below can be found in different directories, the python PATH variable needs to be adjusted
sys.path.append('backend')

import water_solution
import data_collector
import heat_solution

views = Blueprint('views', __name__)

CONFIG_FILE = 'user_info.json'
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
    current_values = water_solution.get_current_values()
    predicted_value = water_solution.get_predicted_water_level()
    predicted_value_with_watering = water_solution.get_predicted_water_level_with_use()
    current_values['predicted_value'] = predicted_value
    current_values['predicted_value_with_watering'] = predicted_value_with_watering
    if not current_values:
        flash('Error Accessing DB', category='error')
    return render_template('water.html', water_resources_data=current_values)


@views.route('/heat', methods=['GET'])
def heat():
    air_quality_data = heat_solution.get_current_values()
    if not air_quality_data:
        flash('Error Accessing DB', category='error')
    return render_template('heat.html', air_quality_data=air_quality_data)


@views.route('/start', methods=['GET'])
def start():
    global STARTED
    data_collector.start()
    STARTED = True
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
    