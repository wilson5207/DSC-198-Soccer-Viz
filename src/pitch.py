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

import glob
def pitch_generate(match, possible_players):

    '''
    Creates the pitch + player movements through coordinates
    
    :param match: String value indicating match opponent
    :param possible_players: list value indicating the participated UCSD players during the game
    :return: figure, the player names that are in the dataframe kimball, and dataframe kimball
    '''


    #I used manual for this os.chdir because there were some problems with the code --Wilson
    os.chdir(r'C:\Users\16413\Desktop\website' + '/data/' + str(match))


    player_files = os.listdir()
    player_files



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

        '''
        Estimates the starting kickoff time for a certain periods of time (usually  0-45, 45-90 minutes)
        
        :param barebones: DataFrame value with player information
        :param time_range1: int value of kickoff time
        :param time_range2: int value of the end of the period (so 45minutes + break)
        :param st1: String value of the lower position's Striker value
        :param st2: String value of the upper position's Striker value
        :param minutes: int value of the desire minutes output
        :return: a DataFrame with correct starting time from given minutes, excluding warmups and halftime breaks.
        '''

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
            #print(str(kick1) + ' is the correct kickoff time for Triton soccer')
            return barebones[(barebones['Seconds'] >= kick1) & (barebones['Seconds'] <= kick1+(minutes*60))]
        else:
            #print(str(kick2) + ' is the correct kickoff second for Triton soccer')
            return barebones[(barebones['Seconds'] >= kick2) & (barebones['Seconds'] <= kick2+(minutes*60))]


    #apply the kickoff_estimation function to find the first&second halves' start&end
    first_h = kickoff_estimation(barebones, 420, 800, 'Kameryn Hoban', 'Caitlin McCarthy', 45)
    second_h = kickoff_estimation(barebones, 4000, 5000, 'Michelle Baddour', 'Kameryn Hoban', 45)

    min_sec = first_h.Seconds.min()
    min_sec2 = second_h.Seconds.min()
    #helper function to reset the seconds from previous dataframe (ie. instead of starting the game at 500 seconds, it will start at 1 seconds)
    def sec_to_min(val):
        return (val - min_sec)/60
    def sec_to_min2(val):
        return (val - min_sec2)/60 + 45

    first_h.Seconds = first_h.Seconds.apply(sec_to_min)
    second_h.Seconds = second_h.Seconds.apply(sec_to_min2)

    #combine first half and second half correct kickoff time dataframe
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
            "prefix": "Minute:",
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
    return fig, player_names, kimball