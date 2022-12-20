# EFFI Solution

This project is a minimal viable product for an application helping you to safe resources in your everyday life.

## 🚀 Features

- Helps you to safe heating energy by optimizing ventilation times.
- Provides garden watering support with implemented moisture monitoring and water tank level forecast.

## 🦋 Prerequisite

### Hardware Prequisites

- Raspberry Pi 3 + Grove Base Hat
- Grove Moisture Sensor v1.4 (PWM)
- Grove Ultrasonic Distance Sensor v2.0 (D16)
- Grove Temperature&Humidity Sensor v1.2 (D5)
- Grove Gas Sensor v1.5 (A0)
- Grove LCD v2.0 (I2C)
- Grove Buzzer v1.2 (D24)
- Grove Red LED Button v1.0 (D22)

### Software Prequisites on Raspberry Pi

- Python Installed
- Git Installed
- Several Python Libraries Installed (requests, pandas, [grove.py](https://github.com/Seeed-Studio/grove.py), openmeteo_py, flask, geocoder, )

## ⚙️ How to Run

1. Startup Raspberry Pi and configure Hostname as _raspi20_
2. Create a new directory called 'EFFI' in you _Documents_ folder (`mkdir EFFI`).
3. Move into that directory (`cd EFFI`) and clone the git project <br />
   `git clone https://github.com/Xiteed/IoT_group01_EFFI.git`
4. Configure crontab by typing `crontab -e` and add the following at the bottom <br />
   `* * * * * /usr/bin/python3 /home/pi20/Documents/EFFI/backend/observer.py` <br />
   save and exit
5. Execute `python3 frontend/app.py`
6. Open _raspi20:8080_ in a Browser to access the web interface

## 👷 Built With

- Python
- HTML

## Authors

- **Pirmin Boensch**
- **Gregor Schwerwitzel**
- **Niels Andersson**
