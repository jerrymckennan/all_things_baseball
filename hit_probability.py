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

year = input("Please specify a year (no earlier than 2015): ")
start = input("Please specify a start EV: ")
end = input("Please specify an end EV: ")
number = int(start)

# The while is for making sure that on the EV data requested is gathered
while number <= int(end):

    # Variables for file location and updates.
    number = str(number)
    file = '/location/target.json' # I use '/Volume/target'+number+'_'+year+'.json'
    csv_file = '/location/target.csv' # I use '/Volume/target'+year+'total.csv'
    
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
        for element in json_data:
            if 'url' in element:
                del element['url']
            if 'rowId' in element:
                del element['rowId']  
                
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
