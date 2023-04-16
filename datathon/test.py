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

rangeslider_marks = {0:'2015', 12:'2016', 24:'2017', 36:'2018', 48:'2019',
                     60:'2020', 72:'2021', 84:'2022', 96:'2023'}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Crime in Montreal by Date", style={'textAlign': 'center'}),

        html.Label("Month/Year"),
        dcc.Slider(min=0,
                   max=98,
                   step=1,
                   value=99,
                   marks=rangeslider_marks,
                   tooltip={"placement": "bottom", "always_visible": False},
                   updatemode='drag',
                   persistence=True,
                   persistence_type='session',
                   id="monthyear"
        ),

        dcc.Graph(id='my-graph')
    ],
    style={"margin": 30}
)


@app.callback(
    Output('my-graph', 'figure'),
    Input('monthyear', 'value'),
)
def update_graph(dateindex):

    crime_freq = df.dropna(subset=['PDQ'])

    crime_freq = crime_freq.groupby('PDQ').agg({'CATEGORIE': 'count'}).sort_values(by='CATEGORIE',ascending=False)
    crime_freq = crime_freq.rename(columns={'CATEGORIE': 'crime_count'})
    combined_table = pd.merge(df, crime_freq, on="PDQ", how='inner')
    combined_table = combined_table.drop_duplicates(subset=['PDQ']).sort_values(by='PDQ', ascending=False)

    fig = px.choropleth_mapbox(combined_table, geojson=geojson, 
                           color = "crime_count",
                           locations="PDQ", featureidkey="properties.PDQ",
                           center={'lat': 45.508888, 'lon': -73.561668},
                           mapbox_style="carto-positron",
                           zoom=9
                           )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == "__main__":
    app.run(debug=True)