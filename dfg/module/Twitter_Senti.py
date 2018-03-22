# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 23:02:39 2017

@author: 703106491
https://www.ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-

"""
# For plotting and visualization:
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import Range1d
from bokeh.plotting import output_file, show,figure
from bokeh.charts import Bar, Line, Donut
from os import path
from module.Twitter_Data import twitter_Search
from module.Twtt_LDA import LDA_model, fnCreate_WordCloud
       

def Donut_Pie(df):
    pd.options.html.border=1
    percentage = df.percentage.values.tolist()
    Type= df.Type.values.tolist()
    
    data = pd.Series(percentage, index = Type)
    plot = Donut(data, title="Overall Sentiment % wise")
    
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 



def fnCreate_Chart_HBar(df):   
    pd.options.html.border=1
              
    count = df['count'].tolist()            
    fruits = ['Positve','Neutral', 'Negetive']    
    plot = figure(y_range=fruits, plot_height=400, title="Overall Sentiment", toolbar_location=None, tools="")    
    plot.hbar(y=fruits, right=count, height=0.5, line_width=0.9, color=["green", "navy","red"])    
    plot.ygrid.grid_line_color = None
    plot.x_range.start = 0
     
#    plot = Bar(df, label='Type', values='count', group='Type', title="Overall Sentiment", legend=False, ylabel='Sentiment expressed in tweets')
#    plot.logo=None
    script, div = components(plot,CDN)        
    return script, div  



def fnCreate_Chart_Line(df):   
    pd.options.html.border=1
    
    plot = Line(df, title="Date wise tweet graph",legend=False, xlabel='Date',ylabel='Count')       #, 'green', 'blue']
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div  

def fnCreate_Chart_MultiLine(df): 
    pd.options.html.border=1
    
    plot = Line(df, title="Likes vs retweets visualization", legend="top_left", xlabel='Date',ylabel='Count')
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 


def fnCreate_Pie(df):
    pd.options.html.border=1
  
    Location = df.Location.values.tolist()
    count = df['count'].tolist()
      
    data = pd.Series(count , index = Location)
    plot = Donut(data, title="Top 5 Country-wise tweets")
    
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div 


        
def fnCreate_Chart_Bar(df):   
    pd.options.html.border=1
    
    plot = Bar(df, label='ID', values='Tweet Count', group='ID', title="Top 5 contributors", legend=False,  bar_width=1.8, xlabel='Users',ylabel='Tweets Count')
    plot.logo=None
    script, div = components(plot,CDN)    
    return script, div  


# API's Charts:
def fnTwitter_Charts(stCrit):
    url=r"D:\dfg\dfg\module\data\final.csv"   
    
    twitter_Search(url, stCrit)   
        
    df = pd.read_csv(url, encoding ="utf-8", parse_dates = ['Date'], dayfirst=True) 
    cnt=len(df.index)   
        
    # We construct lists with classified tweets:    
    pos_tweets = [ tweet for index, tweet in enumerate(df['Text']) if df['SA'][index] > 0]
    neu_tweets = [ tweet for index, tweet in enumerate(df['Text']) if df['SA'][index] == 0]
    neg_tweets = [ tweet for index, tweet in enumerate(df['Text']) if df['SA'][index] < 0]

    s = pd.Series([len(pos_tweets), len(neu_tweets), len(neg_tweets)], index=['Positive',  'Neutral', 'Negative'])
    df3 = pd.DataFrame({'Type':s.index, 'count':s.values})    
    script4, div4=fnCreate_Chart_HBar(df3)
    
    
    
    # We print percentages:
    a=len(pos_tweets)*100/len(df['Text'])
    b=len(neu_tweets)*100/len(df['Text'])
    c= len(neg_tweets)*100/len(df['Text'])    
    s = pd.Series([a, b, c], index=['Positive',  'Neutral', 'Negative'])
    s = pd.DataFrame({'Type':s.index, 'percentage':s.values})    
    script5, div5=Donut_Pie(s)
     
    
 
    df1=pd.value_counts(df['ID'].values, sort=True)
    df2 = pd.DataFrame({'ID':df1.index, 'Tweet Count':df1.values})    
#    df2=df1.to_frame()        
    script, div =fnCreate_Chart_Bar(df2[:5])
    
        
    s=pd.value_counts(df['Date'].values, sort=False)    
    df3 = pd.DataFrame({'Date':s.index, 'count':s.values})
    df1 = df3.sort_values(['Date'],ascending=True)
    s = pd.Series(df1['count'].values, index=df1['Date'])  
    script2, div2=fnCreate_Chart_Line(s)

    
    df1['Date'] = df1['Date'].dt.date
    d1=df1.Date.min().strftime('%d-%m-%y')
    d2=df1.Date.max().strftime('%d-%m-%y')
    
    dtt=''.join(["(" , d1, " To " , d2, ")"])     
    
    
    # Likes vs retweets visualization:
    s= pd.DataFrame(df, columns = ['Date', 'Likes','RTs'])
    df4=s.groupby('Date')['Likes','RTs'].sum()
    script3, div3=fnCreate_Chart_MultiLine(df4)
    
    
    s=pd.value_counts(df['location'].values, sort=True)
    df5 = pd.DataFrame({'Location':s.index, 'count':s.values}) 
    script6, div6=fnCreate_Pie(df5[:5])
    
    
    words,df6 =LDA_model()
    fnCreate_WordCloud(2,words)   
    
    htm="<img src=/static/images/img/2.png>"
          
#    htm= '<img src=/static/bcard/1.png'  + ' width="400" high="300">'  
    
    return cnt,dtt, df1,df2[:5],script, div,script2, div2, df4, script3, div3,script4, div4,script5, div5, df5[:5], script6, div6, df6, htm
  
                                         
#stCrit="#CSeries"   
#fnTwitter_Charts(stCrit)                                          





   
















    