# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import output_file, show
from bokeh.charts import Bar
import pandas as pd 
import numpy as np

def fnCreate_Chart_Bar(df):   
    pd.options.html.border=0
    
    plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div  
    
def fnCreate_Chart_Column(df):     
    pd.options.html.border=0    
    plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div  

    
def fnCreate_Chart_Bar_Full(df):   
    pd.options.html.border=0    
    plot = Bar(df, label='Attbt', values='FY2013', agg='sum', group='Attbt',
        title="Total Sum, grouped by Attribute", legend='top_left')
    
   # plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    script, div = components(plot,CDN)     
    return script, div 
    
    
def fnCreate_Chart_Bar_Full1(df):   
    pd.options.html.border=0
    
    plot = Bar(df, label='Attbt', values='FY2013', agg='sum', stack='Sub_Attbt',
        title="Total Sum, grouped by Attribute", legend='top_left')
    
   # plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    script, div = components(plot,CDN)     
    return script, div 
    
    
    
    
    

def fnAirline_Value2(arln_name):
    path='D:/Users/703106491/Desktop/Python/Tool/Extreme Analytics Tool/'
    filepath=path+'Cappa_Data1.csv'    
    
    names = ['OpName', 'Attbt', 'Sub_Attbt', 'FY2013', 'FY2014', 'FY2015']
    f= open(filepath, 'rb') 
    df = pd.read_csv(f,encoding = "latin1",engine='c',low_memory=False, names=names)  
    pd.options.html.border=0
    #df['que'] = np.where((df['Attbt'] == df['Sub_Attbt'])  , df['Attbt'], np.nan)
    #df=df[pd.notnull(df['que'])]
   

    #df = df.drop('Attbt', 1)
    #df.set_index('Sub_Attr', inplace=True)
    #df = df.rename_axis(None)
    df = df.drop('OpName', 1)
    #df = df.drop('que', 1)
    df[['FY2013', 'FY2014', 'FY2015']] = df[['FY2013', 'FY2014', 'FY2015']].apply(pd.to_numeric)
    #df = df.sort(['FY2013', 'FY2014'], ascending=[1, 0])    
    k=1      
    return k, df    
    
def fnCreate_Chart_Bar2(df):   
    output_file("line_bar.html") 
    pd.options.html.border=0    
    plot = Bar(df, label='Attbt', values='FY2013', agg='sum', group='Attbt',
        title="Total Sum, grouped by Attribute", legend='top_left')
    
   # plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    show(plot) 
    return True
    
def fnCreate_Chart_Bar1(df):   
    pd.options.html.border=0
    output_file("line_bar.html") 
    
    #Now make a pie chart
    plot=df.country.value_counts().plot(kind='pie')
    plot.axis('equal')
    plot.title('Number of appearances in dataset')
    
    #plot = Bar(df, 'Sub_Attbt', values='FY2013', title="Total DISPL by Attribute", bar_width=0.4)
    plot.logo=None
    show(plot)    
    return True



def fnClean_DF(df):
    #df = df.drop('OpName', 1)
    df['que'] = np.where((df['Attbt'] == df['Sub_Attbt']), df['Attbt'], np.nan)
    df=df[pd.notnull(df['que'])]
        

#    df = df.drop('Attbt', 1)
#    
#    #df = df.rename_axis(None)
#    
    df = df.drop('que', 1)
    print(df)
#    df.set_index('Sub_Attbt', inplace=True)
#    df[['FY2013', 'FY2014', 'FY2015']] = df[['FY2013', 'FY2014', 'FY2015']].apply(pd.to_numeric)
    return df  

    
#k,sources_airline=fnAirline_Value2("")
#print(sources_airline)
#sources_airline=fnClean_DF(sources_airline)  





#sources_airline[['FY2013', 'FY2014', 'FY2015']] = sources_airline[['FY2013', 'FY2014', 'FY2015']].apply(pd.to_numeric)
   
#df2=sources_airline.head(3)
#script=fnCreate_Chart_Bar2(df2)        #1st Chart
        
#    
###output_file("line_bar.html")    
#k,df=fnAirline_Value1("manas")
#print(df2)
##a=fnCreate_Chart_Bar2(df)  

#from bokeh.sampledata.autompg import autompg as df
##output_file("line_bar.html")    
#k,df=fnAirline_Value1("manas")
#
#print(df)
#plot = Bar(df, 'Sub_Attr', values='Y1', title="Total DISPL by YR", bar_width=0.4)
#script, div = components(plot,CDN)
#
#print(div)

    #output_file("D:/Users/703106491/Desktop/Python/Code/Chart/test.html")     
#    x = range(1, 6)
#    y = [10, 5, 7, 1, 6]
#    plot = figure(title='Line example', x_axis_label='x', y_axis_label='y')
#    plot.line(x, y, legend='Test', line_width=4)
    #show(plot)
    #print(fnCreate_Chart(''))