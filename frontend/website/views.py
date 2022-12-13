from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import sys

sys.path.append('backend')

from db_access import get_data
import data_collector
import heat_solution

views = Blueprint('views', __name__)

CONFIG_FILE = 'user_info.json'
STARTED = False


@views.route('/')
def home():
    global STARTED
    vars = {'started': STARTED}
    return render_template('home.html', vars=vars)


@views.route('/config', methods=['GET'])
def config():
    try:
        user_data = get_user_data()
        return render_template('config.html', user_data=user_data)
    except:
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

    return render_template('config_form.html')


@views.route('/water', methods=['GET'])
def water():
    return render_template('water.html')


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


def get_user_data():
    global CONFIG_FILE
    with open(CONFIG_FILE, 'r') as file:
        data_json = json.loads(file.read())
        return data_json


def safe_user_data(data):
    user_data_json = json.dumps(data)
    f = open(CONFIG_FILE, mode='w')
    f.write(user_data_json)


get_user_data()
