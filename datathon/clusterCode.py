import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path

"""
Author: Colin Yee
Date: 3/10/23

Background:
**Plotly** is a data visualization library that allows users to create interactive charts and graphs.
Users can interact with the charts by zooming, panning, hovering, and clicking on the data points to get 
additional information. Plotly also allows users to add annotations, text, and images to their charts, making 
it easy to highlight important data points or trends.

**GeoJSON** is a file format for encoding geographical data structures like points, lines, and polygons into a JSON format. 
It consist of objects representing features with properties like name and location data. 
They are used to display and manipulate geographical data. 

The code below essentially:
1. Finds the correct GeoJson and Criminal Logs Data (you may need to change the paths appropriately)
2. Loads the GeoJson into Json Fomat and the criminal logs into a dataframe.
3. Creates a very basic, barebones map in Plotly using the geojson and criminal logs.
"""

"""
The **Path** library is a Python module for working with file and directory paths.
Path.cwd() returns the current working directory as a Path object. 
The current working directory is the directory in which the Python script is currently running.
"""
# You will probably need to manipulate the dataframe to get something good from it :D
criminalLogsPath = Path.cwd() / 'actes-criminels.csv'

# Load the criminal dataframe
df = pd.read_csv(criminalLogsPath)

df = df.dropna()


quart_map = {
    'jour': 1,
    'soir': 2,
    'nuit': 3
}

df['QUART'] = df['QUART'].map(quart_map)

# Convert date string to datetime

df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')

# Convert datetime to ordinal



# Randomly choose 10000 rows from the dataframe

df = df.sample(n=10000)


# Define the scatter plot trace
scatter = go.Scatter3d(
    x=df['PDQ'],
    y=df['LATITUDE'],
    z=df['LONGITUDE'],
    mode='markers',
    marker=dict(
        size=2,
        color=df['CATEGORIE'].astype('category').cat.codes,
        colorscale='Viridis',
        opacity=0.1
    )
)

# Define the cluster trace
clusters = go.Mesh3d(
    x=df['PDQ'],
    y=df['LATITUDE'],
    z=df['LONGITUDE'], alphahull=7,
    opacity=0.1,
    color='cyan'
)

# Define the layout
layout = go.Layout(
    title='Criminal Clusters',
    scene=dict(
        xaxis=dict(title='PDQ'),
        yaxis=dict(title='Latitude'),
        zaxis=dict(title='Longitude')
    )
)

# Create the figure
fig = go.Figure(data=[scatter, clusters], layout=layout)

# Show the figure
fig.show()
