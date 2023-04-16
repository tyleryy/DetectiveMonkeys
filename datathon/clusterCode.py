import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
from dash.dependencies import Input, Output
import dash
from dash import dcc, html

# You will probably need to manipulate the dataframe to get something good from it :D
criminalLogsPath = Path.cwd() / 'actes-criminels.csv'

# Load the criminal dataframe
df = pd.read_csv(criminalLogsPath)

# Define the bar chart
crime_freq = df.pivot_table(index='PDQ', columns='CATEGORIE', values='DATE', aggfunc='count')

crime_freq = crime_freq.fillna(0)

fig = px.bar(crime_freq, barmode='stack', width=1000, height=800)

# Define the scatter plot trace
df = df.head(50000)

df = df.dropna()

criminal_map = {
    3: 'Vol de véhicule à moteur',
    1: 'Méfait',
    2: 'Vol dans / sur véhicule à moteur',
    0: 'Introduction',
    4: 'Vols qualifiés',
    5: 'Infraction entrainant la mort',
}

scatter = go.Scatter3d(
    x=df['PDQ'],
    y=df['LATITUDE'],
    z=df['LONGITUDE'],
    mode='markers',
    marker=dict(
        size=2,
        color=df['CATEGORIE'].astype('category').cat.codes,
        colorscale='Viridis',
        opacity=0.7,
        colorbar=dict(thickness=20, ticklen=4, title='Crime Type')
    ),
)

# Define the layout
layout = go.Layout(
    title='Criminal Clusters',
    scene=dict(
        xaxis=dict(title='PDQ'),
        yaxis=dict(title='Latitude'),
        zaxis=dict(title='Longitude')
    ),
    legend=dict(
        title='Legend',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='rgba(0,0,0,0.8)',
        borderwidth=1,
        font=dict(size=10)
    )
)

# Define the time bar chart


time_bar = df.groupby('QUART')['CATEGORIE'].agg(['count']).sort_values(by='count', ascending=False)
time_bar_fig = px.bar(time_bar, x=time_bar.index, y='count', width=1000, height=800)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        children=dcc.Graph(
            id='cluster-graph',
            figure={
                'data': [scatter],
                'layout': layout
            },
            style={
                'width': '1000px',
                'height': '800px',
                'margin': 'auto'
            }
        )
    ),

    html.Div(
        children=dcc.Graph(
            id='bar-chart',
            figure=fig,
            style={
                'width': '800px',
                'height': '800px',
                'margin': 'auto'
            }
        )
    ),

    html.Div(
        children=dcc.Graph(
            id='time-bar-chart',
            figure=time_bar_fig,
            style={
                'width': '800px',
                'height': '800px',
                'margin': 'auto'
            }
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True, port=2000)
