#we use this script to create a csv file which will store all of our data
import pandas as pd 
import os
def create():
    df = \
    pd.DataFrame(columns=[
        'Name', 
        'AI matches played', 
        'AI wins', 
        'AI losses', 
        'AI ties',
        'PvP matches played',
        'PvP wins',
        'PvP losses',
        'PvP ties'])
    csv_file_name="records.csv"
    csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csv_file_name)
    df.to_csv(csvFileFullPath, index=False)