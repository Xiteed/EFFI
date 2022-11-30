import pandas as pd
from openmeteo_py import Hourly,Daily,Options,OWmanager

latitude = 43.262985
longitude = -2.935013

hourly = Hourly()
daily = Daily()
options = Options(latitude,longitude)

mgr = OWmanager(options,
    hourly.temperature_2m(),)

# Download data
meteo = mgr.get_data()
df = pd.DataFrame(meteo)
print(meteo)
print(df)
print(df.loc)