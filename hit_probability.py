# This is a script put together to scrap the hit probability website for baseball savant.
# It is going to get the data from the JSON on the website, save the file, and then
# convert it over to a CSV file that you can then manipulate or upload into a database
# of your choosing.
#
# I tried to explain each step along the way and what it was doing with my comments.
# Hopefully that helps out some. I am not done yet, but this first step I thought would
# be a great first upload to my Git.
#
# This was done using Python 3.8.6 and it works really well.
#

import json
import urllib
import requests
import pandas as pd
import os.path
from os import path
import time
import sys

def json_edit(json_data):
    for element in json_data:
        if 'url' in element:
            del element['url']
        if 'rowId' in element:
            del element['rowId']
        if 'bat_team_id' in element:
            del element['bat_team_id']
        if 'brl' in element:
            del element['brl']
        if 'fld_team_id' in element:
            del element['fld_team_id']
        if 'game_pk' in element:
            del element['game_pk']
        if 'hh' in element:
            del element['hh']
        if 'name' in element:
            del element['name']
        if 'play_id' in element:
            del element['play_id']
        if 'pn' in element:
            del element['pn']
        if 'pt' in element:
            del element['pt']
        if 'pull' in element:
            del element['pull']
        if 'so' in element:
            del element['so']
        if 'v' in element:
            del element['v']
        if 'video' in element:
            del element['video']
        if 'xbad' in element:
            del element['xbad']
        if 'xban' in element:
            del element['xban']
        if 'eventPretty' in element:
            del element['eventPretty']

def script_start():
    print("Welcome to my Python Script for baseball stuff.")
    print("Please select one of the following to begin and have some fun!")
    print("  1. Get Park Factors from FanGraphs")
    print("  2. Get Launch Angle and Exit Velocity data from baseball savant exported to CSV")
    print("  3. Create MySQL tables to import the above data to OR populate data via .sql script")
    print("  4. Get a players Statcast play-by-play data")
    print("  5. Exit")
    option = input("Which option did you want?: ")
    
    if option == '1': 
        fg_data()
    elif option == '2':
        ev_data()
    elif option == '3':
        mysql()
    elif option == '4':
        player()
    else:
        print("Thank you!")
        time.sleep(2)
        sys.exit()

def fg_data():
    
    number = 1
    csv_file = '/Users/jerrymckennan/Documents/JSON/park_factor_totals.csv'
    csv_file2 = '/Users/jerrymckennan/Documents/JSON/fg_guts.csv'
    
    # Need  to go through for each team, updating the TeamID
    while number <= 30:
        
        number = str(number)
        url = 'https://www.fangraphs.com/guts.aspx?type=pf&season=2015&teamid='+number
        
        pf = pd.read_html(url, index_col=0)
        pf_list = pf[8]
        pf_list.fillna(0, inplace=True)
        print("Working on the "+pf_list['Team'].iloc[0])
        
        if path.exists(csv_file):
            pf_list.to_csv(csv_file, mode='a', header=False)
        else:
            pf_list.to_csv(csv_file)
        
        number = int(number)
        number = number + 1
       
    # GUTS data is on one website. Would use this to manually calculate WAR, wOBA, and other stats
    print("Now gathering GUTS data to save")
    url2 = "https://www.fangraphs.com/guts.aspx?type=cn"
    
    guts = pd.read_html(url2, index_col = 0)
    guts = guts[7]
    # Found that there was a random final column in this, the next command deletes it.
    guts.drop(guts.tail(1).index, inplace=True)
    # MySQL does not like the / in these two columns, renaming them to remove that before saving to CSV file
    guts..rename(columns={"R/PA":"RPA", "R/W":"RW"},inplace=True)
    
    if path.exists(csv_file2):
        guts.to_csv(csv_file2, mode='a', header=False)
    else:
        guts.to_csv(csv_file2)
        
    script_start()

def ev_data():
    
    year = input("Please specify a year (no earlier than 2015): ")
    start = input("Please specify a start EV: ")
    end = input("Please specify an end EV: ")
    number = int(start)

    # The while is for making sure that on the EV data requested is gathered
    while number <= int(end):

        # Variables for file location and updates.
        number = str(number)
        file = '/Users/jerrymckennan/Documents/JSON/'+number+'_'+year+'.json' # I use '/Volume/target'+number+'_'+year+'.json'
        csv_file = '/Users/jerrymckennan/Documents/JSON/'+year+'total.csv' # I use '/Volume/target'+year+'total.csv'

        # This checks to see if you have saved the file already, just in case you want or need to run it again.
        if os.path.exists(file):
            os.remove(file)

        # This section is for the URL, getting the data, and loading data to save
        url = 'https://baseballsavant.mlb.com/statcast_hit_probability?value='+number+'&type=ev&year='+year
        response = urllib.request.urlopen(url)
        json_data = json.load(response)

        # Checks for empty dataset. If empty, just says "no data" otherwise it will save the JSON file.
        if not json_data:
            print("No data for EV of "+number)
        else:
            # This checks for some unneccesary fields that aren't needed.
            json_edit(json_data)
            
            # Saves the file to location mentioned above in variable file, prints an update of where it is.
            with open(file, 'w') as outfile:
                json.dump(json_data, outfile, sort_keys=True, indent=4)

            print("We have data for EV of "+number)

            # This converts the JSON file into a pandas DataFrame.
            data = pd.read_json(file)

            # Value = launch angle, renaming that column to reflect that. Also adding EV to make connection between them.
            data.rename(columns={'value':'launch_angle'}, inplace=True)
            data['ev'] = number

            # This checks for whether the file exists or not. It will create it if needed then append to from there
            if path.exists(csv_file):
                data.to_csv(csv_file, mode='a', index=False, header=False)
            else:
                data.to_csv (csv_file, index=False, header=True)

            # This deletes the JSON file after use. Comment this section out if you want to keep them.
            os.remove(file)

        number = int(number)

        number = number + 1
        
    script_start()

def mysql():
    path = input("Which directory is your MySQL script located at?: ")
    if os.path.exists(path):
        os.chdir(path)
        os.system('ls -l')
        username = input("Enter MySQL username: ")
        #password = input("Enter MySQL password: ")
        filename = input("Please enter the SQL file name listed above: ")
        if os.path.exists(filename):
            os.system('mysql -u '+username+' -p < '+filename)
            print("Inputing data")
        else:
            print("File does not exist")
    else:
        print("Path does not exist.")
    
    script_start()
    
def player():
    print("Some notes regarding getting every LA and EV for a player:")
    print("  I like to use baseball savant personally, but you can use any place you like.")
    print("  If you use baseball savant, the data is stored as a JSON file")
    print("  To get it, go to the players page, select Game Logs, select Statcast")
    print("  You should get a link that looks similar to ")
    print("  https://baseballsavant.mlb.com/savant-player/nelson-cruz-443558?stats=gamelogs-r-hitting-mlb&season=2019")
    print("  From there you will need to Inspect the website, to go the Network tab, select a new year")
    print("  where you can then see the site needed to pull the JSON data down, which will look something like this")
    print("  https://baseballsavant.mlb.com/player-services/gamelogs?playerId=443558&playerType=10&viewType=statcastGameLogs&season=2019&_=1605907951749")
    print("  This link holds the data you are looking for and is what you will need to supply for the URL input coming up")
    print("  The player input is purely for naming the files. Enjoy!")
    print("  ")
    
    player = input("What is the last name of the player you are looking for?: ")
    get_url = input("Please supply the URL to us: ")
    file = '/Users/jerrymckennan/Documents/JSON/Player_data/'+player+'.json' # I use '/Volume/target'+number+'_'+year+'.json'
    csv_file = '/Users/jerrymckennan/Documents/JSON/Player_data/'+player+'.csv' # I use '/Volume/target'+year+'total.csv'

    # This checks to see if you have saved the file already, just in case you want or need to run it again.
    if os.path.exists(file):
        os.remove(file)
    if os.path.exists(csv_file):
        os.remove(csv_file)

    # This section is for the URL, getting the data, and loading data to save
    url = get_url
    response = urllib.request.urlopen(url)
    json_data = json.load(response)

    if not json_data:
        print("No data available")
    else:
        json_edit(json_data)
        # Saves the file to location mentioned above in variable file, prints an update of where it is.
        with open(file, 'w') as outfile:
            json.dump(json_data, outfile, sort_keys=True, indent=4)

        print("We have data")

        # This converts the JSON file into a pandas DataFrame.
        data = pd.read_json(file)
        data['player_name'] = player
        if path.exists(csv_file):
            data.to_csv(csv_file, mode='a', index=False, header=False)
        else:
            data.to_csv (csv_file, index=False, header=True)

        # This deletes the JSON file after use. Comment this section out if you want to keep them.
        os.remove(file)
        
        script_start()

script_start()
