import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


import src.pitch as pitch_fig
import src.tracking as tracking
#import src.viz as viz

import pandas as pd
import numpy as np
import math
import datetime

import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot as plt
import plotly
import os



import warnings
warnings.filterwarnings("ignore")

app = dash.Dash()

#Set up the initial team players for Humboldt (the baseline)
women =  ['Amanda Erickson','Ashlyn Kolarik','Caitlin McCarthy','Christina Oddone','Danielle Satterwhite',
			'Delaney Whittet','Emily Killeen','Erika Braun','Hana Law','Jessical Ruggieri','Kameryn Hoban',
			'Katelyn Meyer','Katherine Hottinger','Kelsey Kimball','Kirsten Webb','Lucy Tang','Madison Samilo',
        	'Marissa Ray','Mia Bonifazi','Michelle Baddour','Mikaela Celeste','Natalie Saddic','Natalie Widmer',
        	'Sophia Bruno']

app.layout = html.Div(children=[
	dcc.Dropdown(id='match_dropdown',
    options=[
        {'label': 'Humboldt', 'value': 'Humboldt'},
        {'label': 'Point Loma', 'value': 'Point Loma'},
        {'label': 'Sonoma', 'value': 'Sonoma'},
        {'label': 'Pomona', 'value': 'Pomona'}
    ],
    value = 'Humboldt', #the baseline
    clearable=False
),
	dcc.Checklist(id='player_list',
    options=[
        {'label': 'Amanda Erickson', 'value': 'Amanda Erickson'},
        {'label': 'Ashlyn Kolarik', 'value': 'Ashlyn Kolarik'},
        {'label': 'Caitlin McCarthy', 'value': 'Caitlin McCarthy'},
        {'label': 'Christina Oddone', 'value': 'Christina Oddone'},
        {'label': 'Danielle Satterwhite', 'value': 'Danielle Satterwhite'},
        {'label': 'Delaney Whittet', 'value': 'Delaney Whittet'},
        {'label': 'Emily Killeen', 'value': 'Emily Killeen'},
        {'label': 'Erika Braun', 'value': 'Erika Braun'},
        {'label': 'Hana Law', 'value': 'Hana Law'},
        {'label': 'Jessical Ruggieri', 'value': 'Jessical Ruggieri'},
        {'label': 'Kameryn Hoban', 'value': 'Kameryn Hoban'},
        {'label': 'Katelyn Meyer', 'value': 'Katelyn Meyer'},
        {'label': 'Katherine Hottinger', 'value': 'Katherine Hottinger'},
        {'label': 'Kelsey Kimball', 'value': 'Kelsey Kimball'},
        {'label': 'Kirsten Webb', 'value': 'Kirsten Webb'},
        {'label': 'Lucy Tang', 'value': 'Lucy Tang'},
        {'label': 'Madison Samilo', 'value': 'Madison Samilo'},
        {'label': 'Marissa Ray', 'value': 'Marissa Ray'},
        {'label': 'Mia Bonifazi', 'value': 'Mia Bonifazi'},
        {'label': 'Michelle Baddour', 'value': 'Michelle Baddour'},
        {'label': 'Mikaela Celeste', 'value': 'Mikaela Celeste'},
        {'label': 'Natalie Saddic', 'value': 'Natalie Saddic'},
        {'label': 'Natalie Widmer', 'value': 'Natalie Widmer'},
        {'label': 'Sophia Bruno', 'value': 'Sophia Bruno'},
    ],
    value=['Amanda Erickson', 'Caitlin McCarthy', 'Christina Oddone', 'Danielle Satterwhite', 'Delaney Whittet',
    		'Emily Killeen', 'Erika Braun', 'Hana Law', 'Kameryn Hoban', 'Katelyn Meyer', 'Katherine Hottinger',
    		'Kelsey Kimball', 'Kirsten Webb', 'Lucy Tang', 'Madison Samilo', 'Marissa Ray', 'Mia Bonifazi',
    		'Michelle Baddour', 'Mikaela Celeste', 'Natalie Saddic', 'Natalie Widmer', 'Sophia Bruno'],
    style={'float': 'left', 'margin': 'auto'},
    labelStyle={'display': 'list-item'}
    ),
    dcc.Graph(id="scatter-plot",
    	figure=pitch_fig.pitch_generate('Humboldt',women)[0], #the baseline again
    	style={'float': 'right', 'margin': 'auto'}),


	dcc.Dropdown(id='player_heat',
    options=[
        {'label': 'Amanda Erickson', 'value': 'Amanda Erickson'},
        {'label': 'Ashlyn Kolarik', 'value': 'Ashlyn Kolarik'},
        {'label': 'Caitlin McCarthy', 'value': 'Caitlin McCarthy'},
        {'label': 'Christina Oddone', 'value': 'Christina Oddone'},
        {'label': 'Danielle Satterwhite', 'value': 'Danielle Satterwhite'},
        {'label': 'Delaney Whittet', 'value': 'Delaney Whittet'},
        {'label': 'Emily Killeen', 'value': 'Emily Killeen'},
        {'label': 'Erika Braun', 'value': 'Erika Braun'},
        {'label': 'Hana Law', 'value': 'Hana Law'},
        {'label': 'Jessical Ruggieri', 'value': 'Jessical Ruggieri'},
        {'label': 'Kameryn Hoban', 'value': 'Kameryn Hoban'},
        {'label': 'Katelyn Meyer', 'value': 'Katelyn Meyer'},
        {'label': 'Katherine Hottinger', 'value': 'Katherine Hottinger'},
        {'label': 'Kelsey Kimball', 'value': 'Kelsey Kimball'},
        {'label': 'Kirsten Webb', 'value': 'Kirsten Webb'},
        {'label': 'Lucy Tang', 'value': 'Lucy Tang'},
        {'label': 'Madison Samilo', 'value': 'Madison Samilo'},
        {'label': 'Marissa Ray', 'value': 'Marissa Ray'},
        {'label': 'Mia Bonifazi', 'value': 'Mia Bonifazi'},
        {'label': 'Michelle Baddour', 'value': 'Michelle Baddour'},
        {'label': 'Mikaela Celeste', 'value': 'Mikaela Celeste'},
        {'label': 'Natalie Saddic', 'value': 'Natalie Saddic'},
        {'label': 'Natalie Widmer', 'value': 'Natalie Widmer'},
        {'label': 'Sophia Bruno', 'value': 'Sophia Bruno'},
    ],
   	value = 'Natalie Saddic', #baseline player for the heatmap
    clearable=False,
    style={'float': 'left-bottom', 'margin': 'auto'}
    ),

    dcc.Graph(id="heatmap",
    	figure=tracking.make_heat_map(pitch_fig.pitch_generate('Humboldt',women)[2], 'Michelle Baddour', 'Converted Latitude', 'Converted Longitude'),
    	style={'float': 'left-bottom', 'margin': 'auto'}),


	])

@app.callback(
    [dash.dependencies.Output('scatter-plot', 'figure'),dash.dependencies.Output('player_list', 'value'),
    dash.dependencies.Output('heatmap', 'figure'),
    dash.dependencies.Input('match_dropdown', 'value'), dash.dependencies.Input('player_heat', 'value'), 
    dash.dependencies.State('player_list', 'value')])

def update_output(new_match, player_heat, player_list):
	#if all the players are unchecked, we'll reset it to all checked, since unchecked all has no meaning.
	if (len(player_list) == 0) & (len(new_match) != 0):
		player_list = women

	pitch_output, checklist_players, kimball_df =  pitch_fig.pitch_generate(new_match, player_list)

	player_heatmap = tracking.make_heat_map(kimball_df, player_heat, 'Converted Latitude', 'Converted Longitude')

	return pitch_output,checklist_players,player_heatmap


if __name__ == '__main__':
	app.run_server(debug=True)