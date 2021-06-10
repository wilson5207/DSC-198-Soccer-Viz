#tabular formatting + functions and calculations
import pandas as pd
import numpy as np

#web scraping
import requests
from bs4 import BeautifulSoup

home_URL = 'https://ucsdtritons.com/'
schedule_URL = 'https://ucsdtritons.com/sports/womens-soccer/schedule/2019'
box_score_ID = 'sidearm-schedule-game-links-boxscore'

def get_game_info():
    '''
    :return: DataFrame of opponent list, corresponding timestamp, and URL suffix
    '''
    page = requests.get(schedule_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    ### Get opposing team name and URL suffix ###
    box_score_suffixes = []
    game_list = []  
    
    for game in soup.find_all("li", class_ = box_score_ID):
        
        try:
            suffix = game.find('a').get('href')
            game_opp = game.find('a').get('aria-label')
            
            if suffix not in box_score_suffixes:
                box_score_suffixes.append(suffix)
                
            if game_opp not in game_list:
                game_list.append(game_opp)
                
        except:
            continue
    
    ### Get cleaned opponent name and timestamp ###
    timestamps = []
    opponents = []
    
    for game in game_list:
        
        timestamp = game.split(' on ')[1]
        timestamps.append(timestamp)
        
        try:
            opponent = game.split(' on ')[0].split(' vs ')[1]
            opponents.append(opponent)
        
        except:
            opponent = game.split(' on ')[0].split(' at ')[1]
            opponents.append(opponent)
    
    ### Making DataFrame ###
    df = pd.DataFrame()
    
    df['Opponent'] = opponents
    df['Timestamp'] = timestamps
    df['Suffix'] = box_score_suffixes
    
    return df

def get_minutes(timestamp):
    '''
    :param timestamp: timestamp in the form of MM:SS
    :return: minute of event
    '''
    return timestamp.split(':')[0]
        
def get_seconds(timestamp):
    '''
    :param timestamp: timestamp in the form of MM:SS
    :return: second of event
    '''
    return timestamp.split(':')[1]

def get_play_by_play(link):
    '''
    :param link: URL suffix to scrape
    :return: DataFrame of game play by play
    '''
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.DataFrame()
    
    for num in np.arange(1,6):
        period = "period-" + num
        
        timer = True
        timestamps = []
        events = []
        
        if not soup.find(id = period):
            continue
            
        ### Scraping for play by play ###
        for table_entry in soup.find(id = period).find_all("td")
            
            if table_entry.get('aria-hidden'):
                continue
                
            table_text = table_entry.text.strip()
            
            #accounts for goal text
            if len(table_text) > 2:
                
                if timer:
                    timestamps.append(table_text)
                    timer = False
                    
                else:
                    events.append(table_text)
                    timer = True
        
        ### Making the DataFrame ##
        curr_df = pd.DataFrame()
        curr_df['Timestamp'] = timestamps
        curr_df['Event'] = events
        
        curr_df['Minute'] = curr_df['Timestamp'].apply(get_minutes)
        curr_df['Second'] = curr_df['Timestamp'].apply(get_seconds)
        
        curr_df['Period'] = num
        
        ### Add DataFrame to main DataFrame ###
        df = pd.concat([df, curr_df], ignore_index = True)
        
    return df   