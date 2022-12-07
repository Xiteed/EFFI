from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import sys

sys.path.append('backend')

from db_access import get_data

views = Blueprint('views', __name__)

CONFIG_FILE = 'user_info.json'


@views.route('/')
def home():
    return render_template('home.html')


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
    heat_data = get_current_temphumgas()
    return render_template('heat.html', heat_data=heat_data)


def get_user_data():
    global CONFIG_FILE
    data = open(CONFIG_FILE)
    data_json = json.loads(data.read())
    return data_json


def safe_user_data(data):
    user_data_json = json.dumps(data)
    f = open(CONFIG_FILE, mode='w')
    f.write(user_data_json)


def get_current_temphumgas():
    data = get_data("temp_test")
    temp = data["temperature"].iloc[-1].item()
    hum = data["humidity"].iloc[-1].item()
    gas = data["gas"].iloc[-1].item()
    data_json = {
        'temp': temp,
        'hum': hum,
        'gas': gas
    }
    return data_json
