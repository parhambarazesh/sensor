import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

time1='2020-01-01T22:00:00Z'
#end_time='2018-12-31T23:00:00Z'
time2=str(datetime.now())[:19].replace(' ','T')+'Z'

"""Getting authentication token from IC'Meter"""
url = 'https://app.ic-meter.com/icm/oauth/token'
headers={'Content-Type':'application/x-www-form-urlencoded'}
body='client_id=trusted-client&grant_type=password&scope=read&username=parham.barazesh@intellectuallabs.no&password=k2Txff8ZG'
body={'client_id':'trusted-client',
'grant_type':'password',
'scope':'read',
'username':'parham.barazesh@intellectuallabs.no',
'password':'k2Txff8ZG'}
response = requests.post(
    url,
    body,
    headers
    )
token=response.json()['access_token']

"""Get building specs"""
url='https://app.ic-meter.com/icm/api/buildings/2.0'
body={'extended':'false',
'hide_empty':'false',
'access_token':token}
building_specs = requests.get(
    url,
    body
    )

building_id=building_specs.json()[0]['buildingId']

"""get sensor data"""
url='https://app.ic-meter.com/icm/api/buildings/2.0/building/indoor/'+str(building_id)
body={'start_time':time1,
'end_time':time2,
'resolution':'minute',
'access_token':token}
sensor_data = requests.get(
    url,
    body
    )


print('CODE',sensor_data.status_code)

if sensor_data.status_code==200:
    df=pd.DataFrame(pd.json_normalize(sensor_data.json()).units[0][0])
    df=df[:-1]
    Time=[d['time'] for d in df.indoorMeasurements]
    Temperature=[d['temperature'] for d in df.indoorMeasurements]
    Humidity=[d['humidity'] for d in df.indoorMeasurements]
    CO2=[d['co2'] for d in df.indoorMeasurements]
    NoiseAverage=[d['noiseAverage'] for d in df.indoorMeasurements]
    NoisePeak=[d['noisePeak'] for d in df.indoorMeasurements]
    Light=[d['light'] for d in df.indoorMeasurements]

    all_data={'Temperature':pd.DataFrame({'Time':Time,'Temperature':Temperature}),
    'Humidity':pd.DataFrame({'Time':Time,'Humidity':Humidity}),
    'CO2':pd.DataFrame({'Time':Time,'CO2':CO2}),
    'NoiseAverage':pd.DataFrame({'Time':Time,'NoiseAverage':NoiseAverage}),
    'NoisePeak':pd.DataFrame({'Time':Time,'NoisePeak':NoisePeak}),
    'Light':pd.DataFrame({'Time':Time,'Light':Light}),}

    for item in all_data:
        fig = px.line(all_data[item], x=all_data[item].columns[0], y=all_data[item].columns[1], title=item)

        fig.update_xaxes(rangeslider_visible=True,
        rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 day", step="day", stepmode="backward"),
                    dict(count=7, label="1 week", step="day", stepmode="backward"),
                    dict(count=1, label="1 month", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ))

        fig.write_html("/home/parham/Documents/codes/factorymind/factorymind/config/static/"+item+".html")
        data=1