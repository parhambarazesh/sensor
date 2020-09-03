import requests
import pandas as pd
import plotly.express as px
from datetime import datetime


token='c32e62f4-2d96-4059-9a19-97faf1978ab4'

start_time='2018-08-01T22:00:00Z'
end_time=str(datetime.now())[:19].replace(' ','T')+'Z'
building_id='908686'
url='https://app.ic-meter.com/icm/api/buildings/2.0/building/indoor/'+building_id+'?start_time='+start_time+'&end_time='+end_time+'&resolution=minute&access_token='+token
response=requests.get(url)
response.status_code

df=pd.DataFrame(pd.json_normalize(response.json()).units[0][0])

time=[d['time'] for d in df.indoorMeasurements]
temp=[d['temperature'] for d in df.indoorMeasurements]
humidity=[d['humidity'] for d in df.indoorMeasurements]
co2=[d['co2'] for d in df.indoorMeasurements]
noise=[d['noiseAverage'] for d in df.indoorMeasurements]

all_data={'temp':pd.DataFrame({'time':time,'temp':temp}),
'temp':pd.DataFrame({'time':time,'temp':temp}),
'humidity':pd.DataFrame({'time':time,'humidity':humidity}),
'co2':pd.DataFrame({'time':time,'co2':co2}),
'noise':pd.DataFrame({'time':time,'noise':noise}),}

data_list=['temp','humidity','co2','noise']

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
