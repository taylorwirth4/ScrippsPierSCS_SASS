def get_all_dr(path):
    # this python script looks at a SCCOOS dr path, looks through all the folders and grabs all the files
    # it then reads all the files and concatenates the data lines into a pandas DataFrame

    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import numpy as np

    soup = BeautifulSoup(requests.get(path).text,features="html.parser")

    allfolders = [] # find all folders in the path
    for link in soup.find_all('a'):
        file = link.get('href')
        if file.startswith('202') == True: # find folders that start with a year string
            allfolders.append(path+file) # append a list of all the folders
    allfolders = allfolders[1::2] # removes every other folder as there are duplicates

    allpath = []
    for i in range(0,len(allfolders)): # go thru each folder and find the files
        soup = BeautifulSoup(requests.get(allfolders[i]).text,features="html.parser")
        for link in soup.find_all('a'):
            file = link.get('href')
            if file.startswith('data_') == True: # find the file names that start with 'data_'
                allpath.append(allfolders[i]+file) # append each file name into a list
    allpath = allpath[1::2]

    alldata = [] # go thru each file and append the data
    for i in range(0,len(allpath)):
        path = allpath[i]
        response = requests.get(path) # opens the .dat file
        text = response.text # gets a text format of the .dat file
        data_by_line = text.split('\n') # splits the text by return line
        alldata.extend(data_by_line) # concatenate each data file

    # rename the columns so it's easy to use
    col_names = ['internet_datetime','IP','sensor_name','samp_type','samp_num','calib_num','calib_rep',
            'date','time','vbatt','vtherm','vint','vext','isobatt','contemp','pHtemp','press',
            'pHint','pHext','O2_MN','O2_SN','O2con','O2sat','O2temp',
            'Dphase','Bphase','Rphase','Bamp','Bpot','Ramp','Raw_Temp',
            'SBEtemp','SBEcond','SBEsal','SBEday','SBEmon','SBEyear','SBEtime']

    df = pd.DataFrame(columns=col_names) # create the pandas DataFrame
   
    # there are sometimes random empty rows in the .dat files
    # this goes through each line and removes any data lines less than 270 characters
    for i in range(0,len(alldata)):
        if len(alldata[i]) > 270:
            if len(alldata[i].split()) > 37: # if the data has sensor name in data string
                df.loc[len(df)] = alldata[i].split()
            else: # if data does not have sensor name in string, put NA in string
                datastring = alldata[i].split()
                datastring.insert(2,'SCS002')
                df.loc[len(df)] = datastring
                
        #df.append(pd.DataFrame((data_by_line[i].split())).T)

    # change the data types for important variables
    df = df.astype({'samp_type': int, 'samp_num': int, 'calib_num': int, 'calib_rep': int, 
    'vbatt': float, 'vtherm': float, 'vint': float, 'vext': float, 'isobatt': float,
    'contemp': float, 'pHtemp': float, 'press': float, 'pHint': float, 'pHext': float,
    'O2_MN': int, 'O2_SN': int, 'O2con': float, 'O2sat': float, 'O2temp': float,
    'SBEtemp': float, 'SBEcond': float, 'SBEsal': float, 'SBEday': int, 'SBEyear': int
    })

    return df, col_names