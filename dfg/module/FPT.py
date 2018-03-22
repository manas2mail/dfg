# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 14:09:43 2018

@author: 703106491
"""
import json
import requests
from lxml import html
from collections import OrderedDict
import pandas as pd
from datetime import date, timedelta, datetime
import os.path as path
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getAirline_Data(source,destination,date,cur_date):    
#    source,destination,date="BOM","CCU","05/02/2018"
    head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
    url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source,destination,date)
    
    print(url)
    response = requests.get(url, headers=head, verify=False)
    
    parser = html.fromstring(response.text)
    json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
    
    if len(json_data_xpath)==0:
        return json_data_xpath  
    else:
        raw_json =json.loads(json_data_xpath[0])
        flight_data = json.loads(raw_json["content"])
                        
        flight_info  = OrderedDict() 
        lists=[]
        my_df=[]
        
        for i in flight_data['legs'].keys():     
            airline_name=flight_data['legs'][i]['carrierSummary']['airlineName']
            departure_city=flight_data['legs'][i]['departureLocation']['airportCity']
            departure=flight_data['legs'][i]['departureLocation']['airportCode']
            arrival_city=flight_data['legs'][i]['arrivalLocation']['airportCode']
            arrival=flight_data['legs'][i]['arrivalLocation']['airportCity']    
            formatted_price=flight_data['legs'][i]['price']['totalPriceAsDecimal']
        
            flight_info={
                         'Current Date':cur_date,
                         'Travel Date':date,
        					'Airline':airline_name,
                         'Departure City':departure_city,
        					'Departure':departure,
                         'Aarrival City':arrival_city,   
        					'Arrival':arrival,
        #					'flight duration':total_flight_duration,					
                         'Ticket Price':formatted_price,
        				}
            lists.append(flight_info)
                        
            sortedlist = sorted(lists, key=lambda k: k['Ticket Price'],reverse=False)
            my_df = pd.DataFrame(sortedlist)           
        return my_df
    

def fngetData(filepath,filedata, intI):      
    travel_date = (date.today()+timedelta(days=intI)).isoformat()
    df = pd.read_csv(filepath)
    df = df.dropna(how='any',axis=0) 
    my_df=[]
    for index, row in df.iterrows():
        org=row['Org'] 
        dest=row['Dest']
        dt = datetime.strptime(travel_date,"%Y-%m-%d").strftime("%m/%d/%Y")
        
        my_df=getAirline_Data(org,dest,dt,date.today())     
        time.sleep(1)     
        if len(my_df)>0: 
            my_df.to_csv(filedata, mode='a', header=False)
            time.sleep(1) 


def fnFPT(filepath, days):
    cur_dir = path.dirname(__file__)
    cur_dir = path.abspath(cur_dir+ "/../")  
    parent_dir=path.join(cur_dir,r'module\data\aft' )      
    filepath=path.join(parent_dir,r'Routes.csv' )    
    filedata="Price" + str(days) + ".csv"
    filedata=path.join(parent_dir,filedata )        
    fngetData(filepath,filedata,days)    

   
def fnFPTMain_Dwnld(stDay):
    if stDay== "All":
        for i in range(5, 25, 5): 
            fnFPT("",i)    
#            print(i)
    else:
       fnFPT("",int(stDay))       
#       print(int(stDay))




    
#if __name__== "__main__":
#    fnFPTMain_Dwnld("All")
    

















