# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 14:09:43 2018

@author: 703106491
"""
#import json
#import requests
#from lxml import html
#from collections import OrderedDict
# For plotting and visualization:


#from bokeh.models import Range1d
from bokeh.plotting import output_file, show,figure
from bkcharts.attributes import CatAttr
from bokeh.charts import Bar, Line, Donut
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd
from os import path
 

def fnCreate_Chart_Bar(df):   
    pd.options.html.border=1  
#    pd.options.display.html.border=1  
    
    label1=CatAttr(columns=['Routes'], sort=False)
    plot = Bar(df, label=label1, values='Ticket Price',group='Routes', title="Average of Ticket Price- Routes wise", legend=False,  bar_width=50, xlabel='Routes',ylabel='Average Ticket Price')
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 
 
    
def fnCreate_Chart_Bar1(df,strS):   
    pd.options.html.border=1 
    label1=CatAttr(columns=['Airline'], sort=False)
    plot = Bar(df, label=label1, values='Ticket Price',group='Airline', title="Average of Ticket Price- Airline wise"  + strS, legend=False,  bar_width=100, xlabel='Airlines',ylabel='Average Ticket Price')
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 

#label='Travel Date',values='Ticket Price',
def fnCreate_Chart_MultiLine(df,strS,j=1): 
    pd.options.html.border=1    
    
    sL=False
    if j ==1:     
        sL="top_center" 
        
    plot = Line(df, title="Average of Ticket Price Date wise" + strS, legend=sL, xlabel='Travel Date',ylabel='Average Ticket Price')
    plot.legend.label_text_font_size = "7pt"
    plot.legend.orientation = "horizontal"
    plot.legend.click_policy="hide"
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 



def fngetData(org, dest, filepath, intI):    
    df = pd.read_csv(filepath)
#    df = df.dropna(how='any',axis=0) 
    df['Routes'] = df['Departure'] +'-'+ df['Aarrival City']
    routs=org  +'-'+ dest
    
#    #--------------------------'Routes avg Ticket Price'-----------------------
    s= pd.DataFrame(df, columns = ['Routes', 'Ticket Price'])    
    df1 = s.groupby(['Routes'])['Ticket Price'].mean().reset_index()
    df1 = df1.sort_values(['Ticket Price'],ascending=True)
    script3, div3 =fnCreate_Chart_Bar(df1)
#    #--------------------------------------------------------------------------

    
    #-------------------------------Ticket Price by Travel Date----------------
    s= pd.DataFrame(df, columns = ['Routes', 'Travel Date', 'Ticket Price'])      
    df1=s.groupby(['Travel Date','Routes'])['Ticket Price'].mean().reset_index() 
    df1['Travel Date']=pd.to_datetime(df1['Travel Date'])  
    df1 = df1.sort_values(['Travel Date'],ascending=True)
    df2 = df1.pivot_table('Ticket Price', [ 'Travel Date'], 'Routes').reset_index()    
    df2.set_index('Travel Date', inplace=True)  
        
    script1, div1 =fnCreate_Chart_MultiLine(df2," for All routes")
   
    
#    s= pd.DataFrame(df, columns = ['Travel Date', 'Ticket Price'])    
#    df1 = s.groupby(['Travel Date'])['Ticket Price'].mean().reset_index()    
#    df1['Travel Date']=pd.to_datetime(df1['Travel Date'])    
#    df2 = df1.sort_values(['Travel Date'],ascending=True)
#    df1 = pd.Series(df2['Ticket Price'].values, index=df2['Travel Date']) 
#    script1, div1 =fnCreate_Chart_MultiLine(df1," for All routes")
    
 #-------------------------------Ticket Price by Travel Date----------------  
    s=df[df.Routes == routs]
    s= pd.DataFrame(s, columns = ['Travel Date', 'Ticket Price'])    
    df1 = s.groupby(['Travel Date'])['Ticket Price'].mean().reset_index()    
    df1['Travel Date']=pd.to_datetime(df1['Travel Date'])    
    df2 = df1.sort_values(['Travel Date'],ascending=True)
    df1 = pd.Series(df2['Ticket Price'].values, index=df2['Travel Date']) 
    script2, div2 =fnCreate_Chart_MultiLine(df1," for "+ routs,0)
    
    #--------------------------------------------------------------------------
    
    
    #-------------------------------Ticket Price by Airline Wise---------------
    s=df[df.Routes == routs]    
    s= pd.DataFrame(df, columns = ['Airline', 'Ticket Price','Travel Date'])  
    s = s.dropna(how='any',axis=0)         
    df1 = s.groupby(['Airline'])['Ticket Price'].mean().reset_index()  
    df1 = df1.sort_values(['Ticket Price'],ascending=True)    
    script4, div4 =fnCreate_Chart_Bar1(df1[:12]," for "+ routs)
    #--------------------------------------------------------------------------


    #-------------------------------Ticket Price by Travel Date and Airline----
    s= pd.DataFrame(df, columns = ['Routes', 'Travel Date', 'Ticket Price','Airline'])     
    s=s[s.Routes == routs]  
    df1=s.groupby(['Travel Date','Airline'])['Ticket Price'].mean().reset_index() 
    df1['Travel Date']=pd.to_datetime(df1['Travel Date'])  
    df1 = df1.sort_values(['Travel Date'],ascending=True)
    df2 = df1.pivot_table('Ticket Price', [ 'Travel Date'], 'Airline').reset_index()    
    df2.set_index('Travel Date', inplace=True)    
    script5, div5 =fnCreate_Chart_MultiLine(df2," for "+ routs,1)
    return script1, div1, script2, div2,script3, div3,script4, div4,script5, div5       





def fnFPT(routs, days):
    cur_dir = path.dirname(__file__)
    cur_dir = path.abspath(cur_dir+ "/../")  
    parent_dir=path.join(cur_dir,r'module\data\aft' )            
    filedata="Price" + str(days) + ".csv"
    filepath=path.join(parent_dir,filedata )   
    org, dest = routs[7:10], routs[11:14]     
#    fngetData(org,dest, filepath,days)  
    script1, div1, script2, div2,script3, div3,script4, div4,script5, div5  =fngetData(org,dest, filepath,days)     
    return script1, div1, script2, div2,script3, div3, script4, div4, script5, div5  , days 


#routs='Routes-ACK-DCA --- Nantucket(ACK)-Washington(DCA)'
#days=5
#fnFPT(routs,days)

















