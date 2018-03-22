# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:32:19 2016

@author: 703106491
"""

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os


def login_cappa(Username,Password,url):
    browser = RoboBrowser(history=True,parser="lxml")
    browser.open(url)

    form = browser.get_form(id='signin')
    form['username'].value = Username
    form['password'].value = Password
    browser.submit_form(form)
    return browser


def soup_data(browser,url):
    browser.open(url)
    if browser.response.ok==True:
        try:
            tabs = browser.get_link('financial')
            browser.follow_link(tabs)
            i=1
        except Exception:
            pass
            i=0
        return i,browser
    else:
        i=0
        return i,browser

def soup_data_main(browser,arln_name,main_name):
    soup = BeautifulSoup(browser.response.text, "lxml")
    right_table=soup.find('table', id='financialdefaulttable')

    if not right_table is None:

        A=[]
        B=[]
        C=[]
        D=[]
        E=[]
        F=[]

        pv=0
        for row in right_table.findAll("tr"):
            cells = row.findAll('td')
            #header=row.findAll('th') #To store second column data
            if len(cells)==5:
                A.append(main_name)
                B.append(pv)
                C.append(cells[1].find(text=True).replace(',',''))

                if not cells[2].find(text=True) is None:
                    D.append(cells[2].find(text=True)[:len(cells[2].find(text=True))-1].replace(',',''))
                else:
                    D.append("")

                if not cells[3].find(text=True) is None:
                    E.append(cells[3].find(text=True)[:len(cells[3].find(text=True))-1].replace(',',''))
                else:
                    E.append("")

                if not cells[4].find(text=True) is None:
                    F.append(cells[4].find(text=True)[:len(cells[4].find(text=True))-1].replace(',',''))
                else:
                    F.append("")



            elif len(cells)==4:
                A.append(main_name)
                B.append(cells[0].find(text=True).replace(',',''))
                C.append(cells[0].find(text=True).replace(',',''))

                if not cells[1].find(text=True) is None:
                    D.append(cells[1].find(text=True)[:len(cells[1].find(text=True))-1].replace(',',''))
                else:
                    D.append("")

                if not cells[2].find(text=True) is None:
                    E.append(cells[2].find(text=True)[:len(cells[2].find(text=True))-1].replace(',',''))
                else:
                    E.append("")

                if not cells[3].find(text=True) is None:
                    F.append(cells[3].find(text=True)[:len(cells[3].find(text=True))-1].replace(',',''))
                else:
                    F.append("")

                pv=cells[0].find(text=True).replace(',','')

        pd.options.html.border=0
        df=pd.DataFrame(A,columns=['OpName'])
        df['Attbt']=B
        df['Sub_Attbt']=C
        df['FY2013']=D
        df['FY2014']=E
        df['FY2015']=F

#        filepath=os.path.abspath(os.path.dirname(__file__)) + '\data\Cappa_Data1.csv'
#        df.to_csv(filepath,header=False, mode = 'a')

        return df





def fnAirline_Value(arln_name):
    Username= 'sankha.ganguli@aero.bombardier.com'         #'sankha.ganguli@aero.bombardier.com'     #'
    Password= 'Capa123'      #Capa123'                             #'
    
    url = 'http://centreforaviation.com/profiles/airlines/' #+ arln_name
    browser= login_cappa(Username,Password,url)
    k=1

    if browser.response.ok==True:
        filepath=os.path.abspath(os.path.dirname(__file__)) + '\data\Airlines_Data.csv'
        f= open(filepath, 'rb')
        df = pd.read_csv(f,encoding = "latin1",engine='c',low_memory=False)
        sources_airline=df.loc[df['Airlines Name'] == arln_name,'Airlines Value']
        if len(sources_airline) > 0:
            sources_airline=sources_airline.item()
            url = 'http://centreforaviation.com/profiles/airlines/' + sources_airline
            j,browser=soup_data(browser,url)
            if j>0:
                k=1
                df=soup_data_main(browser,sources_airline,arln_name)
                return k,df
            else:
                k=0
                df="This Airlines doesn't have any financial data"
                return k,df
        else:
            df="This Airlines name is not founded in our database"
            k=0
            return df
    else:
        k=0
        df="Airlines Not Found"
        return df




def fnClean_DF(df):
    df['que'] = np.where((df['Attbt'] == df['Sub_Attbt']), df['Attbt'], np.nan)
    df=df[pd.notnull(df['que'])]


    #df = df.drop('Attbt', 1)
    #df.set_index('Sub_Attr', inplace=True)
    #df = df.rename_axis(None)
    df = df.drop('OpName', 1)
    df = df.drop('que', 1)
    df[['FY2013', 'FY2014', 'FY2015']] = df[['FY2013', 'FY2014', 'FY2015']].apply(pd.to_numeric)
    return df


#arln_name='Lufthansa'
#k,sources_airline=fnAirline_Value(arln_name)
#print(sources_airline)
###