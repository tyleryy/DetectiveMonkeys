import json
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

from dash import Dash, dcc, html, Output, Input
import math

geojsonPath = Path.cwd() / 'limitespdq.geojson'
geojson = json.load(open(geojsonPath, "r"))
criminalLogsPath = Path.cwd() / 'actes-criminels.csv'
df = pd.read_csv(criminalLogsPath)

#Add the extra column Monthyear to df
def getMonthYear(str):
    return str.split('-')[0] + '-' + str.split('-')[1]
df['MONTHYEAR'] = df['DATE'].apply(getMonthYear)


#CRUCIAL STUFF____________________________________________________________________________

maps = []
df2 = df.drop(df[df.MONTHYEAR != "2015-06"].index)
crime_freq = df2.dropna(subset=['PDQ'])
crime_freq = crime_freq.groupby('PDQ').agg({'CATEGORIE': 'count'}).sort_values(by='CATEGORIE',ascending=False)
crime_freq = crime_freq.rename(columns={'CATEGORIE': 'Crime Count'})
combined_table = pd.merge(df, crime_freq, on="PDQ", how='inner')

combined_table = combined_table.drop_duplicates(subset=['PDQ']).sort_values(by='PDQ', ascending=False)
fig = px.choropleth_mapbox(combined_table, geojson=geojson, 
    color = "Crime Count", # Might need to change depending on what you want to measure
    locations="PDQ", featureidkey="properties.PDQ",
    center={'lat': 45.508888, 'lon': -73.561668}, # Can change the coordinates to make city more centered
    mapbox_style="carto-positron", # Another option is called "open-street-map" :o
    zoom=9,
    color_continuous_scale='Viridis',
    range_color=[0, 300]
)

fig.show()