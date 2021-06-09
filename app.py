import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


#import notebooks.pitch as pitch_fig

import pandas as pd
import numpy as np
import math
import datetime

import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot as plt
import plotly
import os

import src.viz as viz

import warnings
warnings.filterwarnings("ignore")



# os.getcwd()

# main_folder = '../'
# game_folder = '../website/data/'

# games = ['Humboldt', 'Point Loma', 'Pomona', 'Sonoma']

# humboldt_games = game_folder + games[0]
# pointloma_games = game_folder + games[1]
# pomona_games = game_folder + games[2]
# sonoma_games = game_folder + games[3]

# path = os.getcwd()
# print("Current Directory", path)
  
# # prints parent directory
# pr_path = os.path.abspath(os.path.join(path, os.pardir))
# print(os.path.abspath(os.path.join(path, os.pardir)))

# os.chdir(path + '\data\Humboldt')

# os.getcwd()

# #os.chdir()
def pitch_generate(match, possible_players):
	os.chdir('C:\\Users\\16413\\Desktop\\website\\data\\' + str(match))
	player_files = os.listdir()
	#print(player_files)
	print('asdddddddddddddddddddddddd')



	def lat_con(lat):
	    #y0 = 32.887444
	    #y0 = 32.887423
	    y0 = 32.887890643008
	    output = ((lat - y0)*100000)
	    return output

	def long_con(long):
	    #x0 = -117.2403311
	    x0 = -117.24008563915
	    #x0 = -117.240433
	    
	    output = (long - x0)*100000
	    return output

	def convert_latitude(lat):
	    x = 32.887890643008
	    converted = (lat - x) * 100000
	    
	    return converted

	def convert_longitude(long):
	    y = -117.24008563915
	    converted = (long - y) * 100000
	    
	    return converted
	    
	def rotate(point, radians, origin=(0, 0)):
	    """Rotate a point around a given point.
	    
	    I call this the "low performance" version since it's recalculating
	    the same values more than once [cos(radians), sin(radians), x-ox, y-oy).
	    It's more readable than the next function, though.
	    """
	    x, y = point
	    ox, oy = origin

	    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
	    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

	    return qx, qy

	radian_val = 3.0846278020723585

	game_df = pd.DataFrame()

	for player_file in player_files:
	    curr = pd.read_csv(player_file, skiprows = 8)
	    
	    name = ' '.join(player_file.split(' ')[-3:-1])
	    curr['Player'] = name
	    
	    curr['Seconds'] = curr['Seconds'].apply(lambda x: int(x))
	    curr = curr.groupby('Seconds').tail(1)
	    
	    game_df = pd.concat([game_df, curr], ignore_index = True)

	

	def get_coordinates(lat, long):
	    new_lat, new_long = rotate((lat, long), radian_val)
	    
	    return new_lat, new_long

	def get_player_coordinates(df):
	    df['Converted Latitude'] = df['Latitude'].apply(convert_latitude)
	    df['Converted Longitude'] = df['Longitude'].apply(convert_longitude)
	    
	    coordinates = df.apply(lambda x: get_coordinates(x['Converted Latitude'],
	                                                     x['Converted Longitude']),
	                           axis = 1)
	    
	    return df

	coord_df = get_player_coordinates(game_df)
	coord_df.head()

	coord_df['Converted Latitude'] = coord_df['Converted Latitude'].apply(lambda x: x + 51.5)
	coord_df['Converted Longitude'] = coord_df['Converted Longitude'].apply(lambda x: x + 33)

	barebones = coord_df[['Player', 'Seconds', 'Converted Latitude', 'Converted Longitude']]

	barebones['Converted Latitude'] = barebones['Converted Latitude'].apply(lambda x: x if (x >= -1) & (x <= 105) else np.nan)
	barebones['Converted Longitude'] = barebones['Converted Longitude'].apply(lambda x: x if (x >= -1) & (x <= 68) else np.nan)

	barebones = barebones.dropna()
	barebones.head()



	def kickoff_estimation(barebones, time_range1, time_range2, st1, st2, minutes): #st1 is the player with lower position, st2 is higher

	    kickoff1 = barebones[((barebones['Player'] == st1) | (barebones['Player'] == st2))
	              & (barebones['Converted Latitude'] >= 48)
	             & (barebones['Converted Latitude'] <= 53)
	              & (barebones['Converted Longitude'] >= 31)
	             & (barebones['Converted Longitude'] <= 35)]

	    kickoff_time1 = kickoff1[((kickoff1['Seconds'] >= time_range1) & (kickoff1['Seconds'] <= time_range2))]


	    kickoff2 = barebones[((barebones['Player'] == st1) & (barebones['Converted Latitude'] >= 45) & (barebones['Converted Latitude'] <= 53) & (barebones['Converted Longitude'] >= 16) & (barebones['Converted Longitude'] <= 23))
	                         | ((barebones['Player'] == st2) & (barebones['Converted Latitude'] >= 45) & (barebones['Converted Latitude'] <= 53) & (barebones['Converted Longitude'] >= 40) & (barebones['Converted Longitude'] <= 43))
	                        ]

	    kickoff_time2 = kickoff2[((kickoff2['Seconds'] >= time_range1) & (kickoff2['Seconds'] <= time_range2))]


	    #First player
	    possible_kickoff1 = kickoff_time1.Seconds.tolist()
	    max_freq1 = pd.DataFrame()
	    for i in possible_kickoff1:
	        max_freq1 = max_freq1.append([[i, possible_kickoff1.count(i)]])

	    #Second player
	    possible_kickoff2 = kickoff_time2.Seconds.tolist()
	    max_freq2 = pd.DataFrame()
	    for i in possible_kickoff2:
	        max_freq2 = max_freq2.append([[i, possible_kickoff2.count(i)]])

	    #Precise    
	    kick1 = max_freq1.sort_values(by=[1,0]).tail(1).values[0][0] #First half kickoff second
	    kick2 = max_freq2.sort_values(by=[1,0]).tail(1).values[0][0] #First half kickoff second

	    #Solution
	    if len(kickoff_time1) > len(kickoff_time2):
	        print(str(kick1) + ' is the correct kickoff time for Triton soccer')
	        return barebones[(barebones['Seconds'] >= kick1) & (barebones['Seconds'] <= kick1+(minutes*60))]
	    else:
	        print(str(kick2) + ' is the correct kickoff second for Triton soccer')
	        return barebones[(barebones['Seconds'] >= kick2) & (barebones['Seconds'] <= kick2+(minutes*60))]



	first_h = kickoff_estimation(barebones, 420, 800, 'Kameryn Hoban', 'Caitlin McCarthy', 45)
	second_h = kickoff_estimation(barebones, 4000, 5000, 'Michelle Baddour', 'Kameryn Hoban', 45)

	min_sec = first_h.Seconds.min()
	min_sec2 = second_h.Seconds.min()

	def sec_to_min(val):
	    return (val - min_sec)/60
	def sec_to_min2(val):
	    return (val - min_sec2)/60 + 45

	first_h.Seconds = first_h.Seconds.apply(sec_to_min)
	second_h.Seconds = second_h.Seconds.apply(sec_to_min2)

	kimball = first_h.append(second_h)

	kimball = kimball[kimball['Player'].isin(possible_players)]

	seconds = [i for i in range(0, 120, 1)] #0,9360,60

	# make list of players
	player_names = []
	for player in kimball["Player"]:
	    if player not in player_names:
	        player_names.append(player)
	# make figure
	fig_dict = {
	    "data": [],
	    "layout": {},
	    "frames": []
	}

	# fill in most of layout
	fig_dict["layout"]["xaxis"] = {"range": [0, 103], "title": "Latitude"}
	fig_dict["layout"]["yaxis"] = {"range": [0, 66], "title": "Longitude", }
	fig_dict["layout"]["hovermode"] = "closest"


	fig_dict["layout"]["updatemenus"] = [
	    {
	        "buttons": [
	            {
	                "args": [None, {"frame": {"duration": 500, "redraw": False},
	                                "fromcurrent": True, "transition": {"duration": 300,
	                                                                    "easing": "quadratic-in-out"}}],
	                "label": "Play",
	                "method": "animate"
	            },
	            {
	                "args": [[None], {"frame": {"duration": 0, "redraw": False},
	                                  "mode": "immediate",
	                                  "transition": {"duration": 0}}],
	                "label": "Pause",
	                "method": "animate"
	            }
	        ],
	        "direction": "left",
	        "pad": {"r": 10, "t": 87},
	        "showactive": False,
	        "type": "buttons",
	        "x": 0.1,
	        "xanchor": "right",
	        "y": 0,
	        "yanchor": "top"
	    }
	]

	sliders_dict = {
	    "active": 0,
	    "yanchor": "top",
	    "xanchor": "left",
	    "currentvalue": {
	        "font": {"size": 20},
	        "prefix": "Second:",
	        "visible": True,
	        "xanchor": "right"
	    },
	    "transition": {"duration": 300, "easing": "cubic-in-out"},
	    "pad": {"b": 10, "t": 50},
	    "len": 0.9,
	    "x": 0.1,
	    "y": 0,
	    "steps": []
	}

	# make data
	second = 0
	for player in player_names:
	    player_by_second = kimball[kimball["Seconds"] == second]
	    player_by_second_and_name = player_by_second[
	        player_by_second["Player"] == player]
	# make dictionary for the player's scatter point    
	    data_dict = {
	        "x": list(player_by_second["Converted Latitude"]),
	        "y": list(player_by_second["Converted Longitude"]),
	        "mode": "markers+text",
	        "text": list(player_by_second["Player"].str.split().str.get(1)),
	        'textposition':"bottom center",
	        "marker_color": "darkblue",
	        "marker": {
	            "sizemode": "area",
	            "sizeref": 200000,
	            
	        },
	        "name": player
	    }
	    fig_dict["data"].append(data_dict)
	    
	    a = (player_by_second["Converted Latitude"]).tolist()
	    b = (player_by_second["Converted Longitude"]).tolist()
	# check if the player's GPS is empty(outside of the pitch)    
	    if len(a) == 0:
	        a = None
	    if len(b) == 0:
	        b = None
	    else:
	        a.append(a[0])
	        b.append(b[0])
	    
	# make lines/shape that connect the players together
	    line_dict = {
	        "x": a,
	        "y": b,
	        "mode": "lines",
	        'fill':"toself",
	    }
	    fig_dict['data'].append(line_dict)

	# make frames
	for second in seconds:
	    frame = {"data": [], "name": str(second)}
	    for player in player_names:
	        player_by_second = kimball[kimball["Seconds"] == int(second)]
	        player_by_second_and_name = player_by_second[
	            player_by_second["Player"] == player]

	        data_dict = {
	        "x": list(player_by_second["Converted Latitude"]),
	        "y": list(player_by_second["Converted Longitude"]),
	            "mode": "markers+text",
	            "text": list(player_by_second["Player"].str.split().str.get(1)),
	            'textposition':"bottom center",
	            "marker_color": "darkblue",
	            "marker": {
	                "sizemode": "area",
	                "sizeref": 200000,
	                
	            },
	            "name": player
	        }
	        frame["data"].append(data_dict)
	        
	        a = (player_by_second["Converted Latitude"]).tolist()
	        b = (player_by_second["Converted Longitude"]).tolist()
	        
	        if len(a) == 0:
	            a = None
	        if len(b) == 0:
	            b = None
	        else:
	            a.append(a[0])
	            b.append(b[0])
	        
	        line_dict = {
	            "x": a,
	            "y": b,
	            "mode": "lines",
	            'fill':"toself",
	        }
	        frame['data'].append(line_dict)

	    fig_dict["frames"].append(frame)
	    slider_step = {"args": [
	        [second],
	        {"frame": {"duration": 300, "redraw": False},
	         "mode": "immediate",
	         "transition": {"duration": 300}}
	    ],
	        "label": second,
	        "method": "animate"}
	    sliders_dict["steps"].append(slider_step)


	fig_dict["layout"]["sliders"] = [sliders_dict]


	fig = go.Figure(fig_dict)


	fig.update_layout(
	                images= [dict(
	                    source=r'C:\\Users\\16413\\Desktop\\website\\newplot2.png',
	                    xref="paper", yref="paper",
	                    x=0, y=0,
	                    sizex=1, sizey=1,
	                    xanchor="left",
	                    yanchor="bottom",
	                    sizing="stretch",
	                    layer="below")])

	fig.update_xaxes(showgrid=False, zeroline=False)
	fig.update_yaxes(showgrid=False, zeroline=False)
	return fig, player_names

#current_game = 'Humboldt'

app = dash.Dash()

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
    value = 'Humboldt',
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
    	figure=pitch_generate('Humboldt',women)[0],
    	style={'float': 'right', 'margin': 'auto'})
	])

@app.callback(
    [dash.dependencies.Output('scatter-plot', 'figure'),dash.dependencies.Output('player_list', 'value'),
    dash.dependencies.Input('match_dropdown', 'value'), dash.dependencies.State('player_list', 'value')])
def update_output(new_match, player_list):

	if (len(player_list) == 0) & (len(new_match) != 0):
		player_list = women

	a,b =  pitch_generate(new_match, player_list)

	return a,b


if __name__ == '__main__':
	app.run_server(debug=True)