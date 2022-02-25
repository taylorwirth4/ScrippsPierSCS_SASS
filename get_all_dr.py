def get_all_dr(path):

    from bs4 import BeautifulSoup
    import requests
    import pandas as pd

    soup = BeautifulSoup(requests.get(path).text,features="html.parser")

    allpath = []
    for link in soup.find_all('a'):
        file = link.get('href')
        if file.startswith('data_') == True:
            allpath.append(path+'/'+file)
    allpath = allpath[1::2]

    alldata = []
    for i in range(0,len(allpath)):
        path = allpath[i]
        response = requests.get(path)
        text = response.text
        data_by_line = text.split('\n')
        alldata.extend(data_by_line)

    col_names = ['internet_datetime','IP','samp_type','samp_num','calib_num','calib_rep',
            'date','time','vbatt','vtherm','vint','vext','isobatt','contemp','pHtemp','press',
            'pHint','pHext','O2_MN','O2_SN','O2con','O2sat','O2temp','a','b','c','d','e','f','g',
            'SBEtemp','SBEcond','SBEsal','SBEday','SBEmon','SBEyear','SBEtime']

    df = pd.DataFrame(columns=col_names)

    for i in range(0,len(alldata)):
        if len(alldata[i]) > 270:
            df.loc[len(df)] = alldata[i].split()
        #df.append(pd.DataFrame((data_by_line[i].split())).T)

    return df