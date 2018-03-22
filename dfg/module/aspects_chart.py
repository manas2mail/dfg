# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 03:19:34 2018

@author: 703106491
https://nycdatascience.com/blog/student-works/scraping-tripadvisor-airlines-customer-reviews/
"""
from time import time
start_time = time()


#from aspects import fnMain_ACT
#from LDA_Htl_Rev import LDA_model, fnWord_Freq, fnCreate_WordCloud

from module.LDA_Htl_Rev import LDA_model, fnWord_Freq, fnCreate_WordCloud
from module.aspects import fnMain_ACT

from bokeh.plotting import output_file, show,figure
from bkcharts.attributes import CatAttr
from bokeh.charts import Bar, Line, Donut
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool
import pandas as pd
import numpy as np



def fnCreate_Chart_Bar(df):    
    plot = Bar(df, label='Aspects', values='Count',group='Polarity',
               title="Average Sentiment for various Aspects", legend='top_left', 
               bar_width=0.9,color=["green","red"],
               xlabel='Aspects',ylabel='Count')
 
    plot.logo=None
    plot.legend.label_text_font_size = "7pt"
    plot.legend.orientation = "horizontal"
#    plot.legend.click_policy="hide"

    script, div = components(plot,CDN)    
    return script, div


def fnCreate_Stacked_Bar(df): 
#    label1=CatAttr(columns=['Aspects'], sort=True)   
    tmp=df
    plot = Bar(tmp, stack=tmp.columns[0], 
               label=tmp.columns[1], values=tmp.columns[2], 
               legend=True,title="Sentiment segmentation based on top 7 Aspects",
               xlabel='Polarity',ylabel='Count')
    plot.logo=None
    plot.legend.label_text_font_size = "7pt"
    plot.legend.orientation = "horizontal"
    
    script, div = components(plot,CDN)    
    return script, div



def fnCreate_Chart_Bar_wf(df,stS= "all type reviews"):
    label1=CatAttr(columns=['word'], sort=False)    
    plot = Bar(df, label=label1, values='freq',group='word',
               title="Top 10 Frequent Words for " + stS, legend=None, 
               bar_width=0.9,xlabel='word',ylabel='freq')  #,plot_width=450, plot_height=450
    
    
    
    plot.logo=None
    plot.legend.label_text_font_size = "7pt"
    plot.legend.orientation = "horizontal"

    script, div = components(plot,CDN)    
    return script, div
    

def Donut_Pie(df,stS):
    pd.options.html.border=1
    percentage = df.Count.values.tolist()
    Type= df.Aspects.values.tolist()
    
    data = pd.Series(percentage, index = Type)
    plot = Donut(data, title= stS +" Sentiment Aspects segmentation")
    
    plot.logo=None
    
#    show(plot)
    script, div = components(plot,CDN)    
    return script, div 
 

    
def fnChart_ACT(hotel_loc): 
    pd.options.html.border=1
        
    df=fnMain_ACT(hotel_loc)     
#    df =pd.read_csv('ACT.csv')   #, delimiter='\t', index_col=0)
    
    print(df[:7])
        
    df1= pd.DataFrame(df, columns = ['Aspects', 'Polarity'])      
    df1['Polarity'] = np.where(df1['Polarity']>0, '+ve', '-ve')
    df_grouped=df1.groupby(['Aspects','Polarity'])['Polarity'].count().reset_index(name='Count') #.reset_index() 
    
    
    #------------------All Aspect Chart ------------------
    script, div=fnCreate_Chart_Bar(df_grouped) 
    
     #    ----New ---# We print percentages:  +ve --------   
    dfp=df_grouped[df_grouped['Polarity']== "+ve"]
    df2= pd.DataFrame(dfp, columns = ['Aspects', 'Count'])  
    script1, div1=Donut_Pie(df2,"+ve")    
         
    #    ----- -ve -----------    
    dfn=df_grouped[df_grouped['Polarity']== "-ve"]
    df2= pd.DataFrame(dfn, columns = ['Aspects', 'Count'])  
    script2, div2=Donut_Pie(df2,"-ve")      
    
   #    script1, div1=fnCreate_Stacked_Bar(df2) 
#    #------------------end All Aspect Chart ------------------
#    
#    
#    
#    #---------------- start All topics & Word Chart----------------    
    texts= df["Sentence"].tolist()    
    words, df_lda =LDA_model(df,texts)
    
    wrds=' '.join(words)
    fnCreate_WordCloud(8,wrds)
    htm="<img src=/static/images/img/8.png>"
    
    
    df_wf=fnWord_Freq(words,10)
    script3, div3=fnCreate_Chart_Bar_wf(df_wf) 
#    #----------------end All topics & Word Chart---------------- 


    #--------------- +Ve charts --------------- 
    dfp=df[df['Polarity']== 1]
    textsp= dfp["Sentence"].tolist()    
    wordsp, df_ldap =LDA_model(dfp,textsp)
    
    
    wrdsp=' '.join(wordsp)
    fnCreate_WordCloud(9,wrdsp)
    htmp="<img src=/static/images/img/9.png>"
    
    df_wfp=fnWord_Freq(wordsp,10)
    script3p, div3p=fnCreate_Chart_Bar_wf(df_wfp, "+ve type reviews")     
    #--------------- +Ve charts --------------- 
    
    
    
    #--------------- -Ve charts --------------- 
    dfn=df[df['Polarity']== 0]
    textsn= dfn["Sentence"].tolist()    
    wordsn, df_ldan =LDA_model(dfn,textsn)
    
    
    wrdsn=' '.join(wordsn)
    fnCreate_WordCloud(7,wrdsn)
    htmn="<img src=/static/images/img/7.png>"
    
    df_wfn=fnWord_Freq(wordsn,10)
    script3n, div3n=fnCreate_Chart_Bar_wf(df_wfn, "-ve type reviews")  
    #--------------- -Ve charts --------------- 
 
    
    #--------------- Some Snapshot Data ---------------     
    
    df_smpl=df.loc[24:40]
    df_smpl= pd.DataFrame(df_smpl, columns = ['Sentence', 'Aspects', 'Polarity'])      
#    print(df_smpl)
  
    #--------------- Some Snapshot Data--------------- 
    
    
    return  df_smpl, df_wfn, df_ldan, htmn, script3n, div3n, df_wfp, df_ldap, htmp, script3p, div3p, df_grouped, df_lda, htm, df_wf, script, div,script1, div1,script2, div2,script3, div3

    
    
#fnChart_ACT()    

    
  
    





#
#df=fnMain_ACT() 
#    
#df.to_csv("ACT.csv", encoding='utf-8', index= False)
#df = pd.read_csv("ACT.csv") 
#
#print(df.head(10))  
##
#
#
#print("---processing time: %s seconds ---" % (time() - start_time)) 
#
#




    
    
