import sys
import os

sys.path.insert(0, '..')

curr_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

data_folder = '/data/'
games = ['Humboldt', 'Point Loma', 'Pomona', 'Sonoma']

x0 = 32.887890643008
y0 = -117.24008563915
radian_val = 3.0846278020723585

def read_all_games():
    '''
    To cycle through all games and consolidate all player
    files into a single DataFrame for each game
    
    :return: a list of consolidated DataFrames for each game
    '''

    all_games = []

    for game in games:
        game_fp = parent_path + data_folder + game
        os.chdir(game_fp)

        player_files = os.listdir()

        game_df = pd.DataFrame()

        for player_file in player_files:
            curr = pd.read_csv(player_file, skiprows = 8)

            name = ' '.join(player_file.split(' ')[-3:-1])
            curr['Player'] = name
            
            #Take only whole seconds to reduce rows
            curr['Seconds'] = curr['Seconds'].apply(lambda x: int(x))
            curr = curr.groupby('Seconds').tail(1)

            game_df = pd.concat([game_df, curr], ignore_index = True)

        all_games.append(game_df)
        
    return all_games


def convert_latitude(lat):
    '''
    Converts latitude for data visualization
    
    :param lat: latitude value
    :return: converted latitude value
    '''
    
    converted = (lat - x0) * 100000
    
    return converted
        
def convert_longitude(long):
    '''
    Converts longitude for data visualization
    
    :param lat: longitude value
    :return: converted longitude value
    '''
    
    converted = (lat - y0) * 100000
    
    return converted

def rotate(point, radians, origin=(0, 0)):
    """
    Rotates a point around a given point (origin)
    
    :param point: set of x and y values
    :param radians: radian value used for calculations
    :param origin: reference point for rotation
    """
    x, y = point
    ox, oy = origin

    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

    return qx, qy

def get_coordinates(lat, long):
    '''
    Rotates a set of latitude and longitude coordinates around a point
    
    :param lat: latitude value
    :param long: longitude value
    :return: a set of x and y coordinates rotated around the origin
    '''
    new_lat, new_long = rotate((lat, long), radian_val)
    
    return new_lat, new_long

def get_player_coordinates(df, lat_column, long_column):
    '''
    Applies the get_coordinates function to a DataFrame
    
    :param df: DataFrame of tracking data
    :param lat_column: String value indicating latitude column
    :param long_column: String value indicating longitude column
    :return: DataFrame with additional Converted Latitude and
    Longitude columns
    '''
    
    df['Converted Latitude'] = df[lat_column].apply(convert_latitude)
    df['Converted Longitude'] = df[long_column].apply(convert_longitude)
    
    coordinates = df.apply(lambda x: get_coordinates(x['Converted Latitude'],
                                                     x['Converted Longitude']),
                          axis = 1)
    
    return coordinates

def shift_coordinates(df, lat_column, long_column,
                      x_shift = 51.5, y_shift = 33):
    '''
    Shifts x and y coordinates to recenter coordinates
    with (0, 0) as the lower left corner of the pitch
    
    :param df: DataFrame of tracking data with coordinates
    :param lat_column: String value indicating latitude column
    :param long_column: String value indicating longitude column
    :param x_shift: value to shift x by
    :param y_shift: value to shift y by
    :return: DataFrame with shifted latitude and longitude columns
    '''
    
    df[lat_column] = df[lat_column].apply(lambda x: x + x_shift)
    df[long_column] = df[long_column].apply(lambda y: y + y_shift)
    
    return df

def filter_coordinates(df, lat_column, long_column, max_x, max_y)
    '''
    Filters out extreme coordinate values
    
    :param df: DataFrame of tracking data with coordinates
    :param lat_column: String value indicating latitude column
    :param long_column: String value indicating longitude column
    :param max_x: upper bound for x-value
    :param max_y: upper bound for y-value
    :return: DataFrame with filtered latitude and longitude columns
    '''
    
    df[lat_column] = df[lat_column].apply(lambda x: x if (x >= 0) & \
                                         (x <= max_x))
    df[long_column] = df[long_column].apply(lambda y: y if (y >= 0) & \
                                         (y <= max_y))
    
    return df