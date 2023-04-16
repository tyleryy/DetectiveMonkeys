import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path

# You will probably need to manipulate the dataframe to get something good from it :D
criminalLogsPath = Path.cwd() / 'actes-criminels.csv'

# Load the criminal dataframe
df = pd.read_csv(criminalLogsPath)

df = df.head(20000)

df = df.dropna()


criminal_map = {
    3: 'Vol de véhicule à moteur',
    1: 'Méfait',
    2: 'Vol dans / sur véhicule à moteur',
    0: 'Introduction',
    4: 'Vols qualifiés',
    5: ''
}


print(df['CATEGORIE'])


# Print the unique category codes in the DataFrame
print('\nUnique Category Codes in DataFrame:')
mapping = df['CATEGORIE'].astype('category').cat.codes


# Print the rows with category code 5
print('\nRows with Category Code 5:')
print(df[mapping == 5])


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


# Figure out the encoding of the crime type



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
        opacity=0.7,
        colorbar=dict(thickness=20, ticklen=4, title='Crime Type')
    ),
    showlegend=True,
)

# Define the cluster trace

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
# Create the figure
fig = go.Figure(data=[scatter], layout=layout)

# Show the figure
fig.show()
