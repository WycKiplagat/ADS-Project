#load libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import numpy as np
from scipy import spatial
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.express as px

# Build the app
# Output the pixelname and other locational features of the farmer
# Plot the location of the farmer on the map
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'subheadingsText': "red",
    'outputText': "blue",
    'submitText': 'green'
}

grid = pd.read_csv('the.grid.Kenya_pixelboundaries.csv')

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1("KENYAN FARMERS ARC2 SATELLITE PIXELS ALLOCATION",
                style={'textAlign': 'center', 'color': colors['text']}
                )]),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["Latitude"]),
                    html.Div(dcc.Input(id='latitude', type='number', min=-4.5, max=4.5, step=0.001, value=0))
                ], style={'width': '150px'}),

                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["Longitude"]),
                    html.Div(dcc.Input(id='longitude', type='number', min=34, max=42, step=0.001, value=0))
                ], style={'width': '150px'})
            ], style={'display': 'flex', 'flex-direction': 'row'}),

            html.Div(children=[
                html.Button('Submit', id='submit-button', n_clicks=0,
                            style={'textAlign': 'center', 'backgroundColor': colors['submitText']})
            ]),

            html.Div(children=[
                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["PixelName"]),
                    html.Div(id='Nearest-Pixel', style={"color": colors['outputText']})
                ], style={'width': '150px'})
            ]),

            html.Div(children=[
                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["PixelLatitude"]),
                    html.Div(id='PixelCenterPoint(Lat)', style={"color": colors['outputText']})
                ], style={'width': '150px'}),

                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["PixelLongitude"]),
                    html.Div(id='PixelCenterPoint(Lon)', style={"color": colors['outputText']})
                ], style={'width': '150px'})

            ], style={'display': 'flex', 'flex-direction': 'row'}),

            html.Div(children=[
                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']}, children=["Country"]),
                    html.Div(id='Country', style={"color": colors['outputText']})
                ], style={'width': '150px'}),

                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']}, children=["County"]),
                    html.Div(id='County', style={"color": colors['outputText']})
                ], style={'width': '150px'})
            ], style={'display': 'flex', 'flex-direction': 'row'}),

            html.Div(children=[
                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']},
                               children=["Constituency"]),
                    html.Div(id='Constituency', style={"color": colors['outputText']})
                ], style={'width': '150px'}),

                html.Div(children=[
                    html.Br(),
                    html.Label(style={"font-weight": "bold", 'color': colors['subheadingsText']}, children=["Ward"]),
                    html.Div(id='Ward', style={"color": colors['outputText']})
                ], style={'width': '150px'})
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], style={'backgroundColor': colors['background'], 'padding': 10, 'flex': 1}),

        html.Div(children=[
            html.Label(style={"font-weight": "bold", 'textAlign': 'center', 'color': colors['subheadingsText']},
                       children=["LOCATION OF THE FARMER ON THE MAP"]),
            dcc.Graph(id='my-graph', figure={})
        ], style={'border': 'solid 2px blue'})

    ], style={'display': 'flex', 'flex-direction': 'row'})
])


@app.callback(Output('Nearest-Pixel', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    pixel = str(grid.loc[index, ["PixelName"]].values)[2:-2]
    return pixel


@app.callback(Output('PixelCenterPoint(Lat)', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    lat = str(grid.loc[index, ["Latitude"]].values)[1:-1]
    return lat


@app.callback(Output('PixelCenterPoint(Lon)', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    lon = str(grid.loc[index, ["Longitude"]].values)[1:-1]
    return lon


@app.callback(Output('Country', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    country = str(grid.loc[index, ["Country"]].values)[2:-2]
    return country


@app.callback(Output('County', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    county = str(grid.loc[index, ["county"]].values)[2:-2]
    return county


@app.callback(Output('Constituency', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    constituency = str(grid.loc[index, ["constituency"]].values)[2:-2]
    return constituency


@app.callback(Output('Ward', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_output(n_clicks, input1, input2):
    the_grid = grid[['Latitude', 'Longitude']].to_numpy()
    pixelpoints = spatial.KDTree(the_grid)
    distance, index = pixelpoints.query((input1, input2), k=1)
    ward = str(grid.loc[index, ["ward"]].values)[2:-2]
    return ward


@app.callback(Output('my-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('latitude', 'value'),
               State('longitude', 'value')])
def update_graph(n_clicks, input1, input2):
    data = pd.DataFrame([
        {"Latitude": input1, "Longitude": input2}
    ])
    fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", zoom=3, width=800, mapbox_style='open-street-map')
    fig.update_traces(marker=dict(size=10, color="red"))
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)