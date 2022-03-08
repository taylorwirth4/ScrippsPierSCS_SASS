def get_recent_dr(path):
   # this python script looks at a SCCOOS dr path, looks through all the folders and grabs all the files
    # from the last time SIOpier_SCS_dr_liveipynb was run.
    # It then reads all files from the last data file and concatenates the data lines into a pandas DataFrame

    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import numpy as np
    import os
    import glob


    # read the latest download date from the last downloaded file
    txt = glob.glob('*.txt')
    df = pd.read_csv(' '.join(txt),sep='\t')
    
    # find the datetime of the last sample
    date = df.iloc[-1]['date']
    year = date[:4]
    mon = date[5:-3]
    day = date[-2:]
    time = df.iloc[-1]['internet_datetime']
    last_path = path+year+'-'+mon+'/data_'+year+mon+day+'.dat'
    last_folder = path+year+'-'+mon+'/'

    # find the last download location in the SCCOOS dr
    soup = BeautifulSoup(requests.get(last_path).text,features="html.parser")
    response = requests.get(last_path) # opens the .dat file
    text = response.text # gets a text format of the .dat file
    data_by_line = text.split('\n') # splits the text by return line

    # search the last downloaded file for the last data time
    last = [data_by_line.index(l) for l in data_by_line if l.startswith(time)]
    lastdata = data_by_line[last[0]] # this is the last data line in the download file

    # download data starting from that last datetime of the same file 
    for i in range(last[0]+1,len(data_by_line)):
        if len(data_by_line[i]) > 270:
                df.loc[len(df)] = data_by_line[i].split() #appends to the dataframe

    # find the rest of the files and append the data
    soup = BeautifulSoup(requests.get(path).text,features="html.parser")
    allfolders = [] # find all folders in the path
    for link in soup.find_all('a'):
        file = link.get('href')
        if file.startswith('202') == True: # find folders that start with a year string
            allfolders.append(path+file) # append a list of all the folders
    allfolders = allfolders[1::2] # removes every other folder as there are duplicates

    findex = allfolders.index(last_folder) # find the folder index of the last data download 
    allnewfolders = allfolders[findex:] # create new list of new data folders

    allnewpath = []
    for i in range(0,len(allnewfolders)): # go thru each folder and find the files
        soup = BeautifulSoup(requests.get(allnewfolders[i]).text,features="html.parser")
        for link in soup.find_all('a'):
            file = link.get('href')
            if file.startswith('data_') == True: # find the file names that start with 'data_'
                allnewpath.append(allnewfolders[i]+file) # append each file name into a list
    allnewpath = allnewpath[1::2]
    findex = allnewpath.index(last_path) # find the folder index of the last data download 
    allnewpath = allnewpath[findex+1:] # create new list of new data folders

    allnewdata = [] # go thru each file and append the data
    for i in range(0,len(allnewpath)):
        path = allnewpath[i]
        response = requests.get(path) # opens the .dat file
        text = response.text # gets a text format of the .dat file
        data_by_line = text.split('\n') # splits the text by return line
        allnewdata.extend(data_by_line) # concatenate each data file
    allnewdata

    # append the newly download data to the data frame
    # there are sometimes random empty rows in the .dat files
    # this goes through each line and removes any data lines less than 270 characters
    for i in range(0,len(allnewdata)):
        if len(allnewdata[i]) > 270:
            df.loc[len(df)] = allnewdata[i].split()
        #df.append(pd.DataFrame((data_by_line[i].split())).T)

    # change the data types for important variables
    df = df.astype({'samp_type': int, 'samp_num': int, 'calib_num': int, 'calib_rep': int, 
    'vbatt': float, 'vtherm': float, 'vint': float, 'vext': float, 'isobatt': float,
    'contemp': float, 'pHtemp': float, 'press': float, 'pHint': float, 'pHext': float,
    'O2_MN': int, 'O2_SN': int, 'O2con': float, 'O2sat': float, 'O2temp': float,
    'SBEtemp': float, 'SBEcond': float, 'SBEsal': float, 'SBEday': int, 'SBEyear': int
    })

    # drop data rows if SBE salinity is outside the standard deviation
    df = df[np.abs(df['SBEsal']-df['SBEsal'].mean()) <= (2*df['SBEsal'].std())]
    # remove pressure outliers
    df['press']=df['press'][~(np.abs(df['press']-df['press'].mean()) > (3*df['press'].std()))]
    col_names = df.columns

    return df, col_names