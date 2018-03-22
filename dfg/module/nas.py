# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:32:19 2016

@author: 703106491
"""
import datetime
import requests
import re
from newspaper import Article
from textblob import TextBlob
from dateutil.parser import parse
from lxml import html
from os import path
from wordcloud import WordCloud, STOPWORDS
from datetime import date

def fnCreate_WordCloud(i,text):
    if len(text)>5:
        stopwords = set(STOPWORDS)
        stopwords.add("said")
        
        d = path.dirname(__file__)
        parent_dir = path.abspath(d + "/../")  
        d=path.join(parent_dir,r'nlp\static\images\img' )
    
        # lower max_font_size        
        wordcloud = WordCloud(background_color="white", max_font_size=40, stopwords=stopwords).generate(text)
    
        ## The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
    
        # store default colored image
        filename=  str(i) + '.png'
        image.save( path.join(d, filename), "PNG" )
#        image.show()


def find_other_news_sources(url=None, title=None):
    # Google forwards the url using <google_domain>/url?q=    <actual_link>. This might change over time
    forwarding_identifier = '/url?q='    
    #google_news_search_url = 'http://www.google.com/search?q=' + urllib.parse.quote(title) + '&tbm=nws'
    google_news_search_tree = fnNewsKeywords(url)
    other_news_sources_links = [a_link.replace(forwarding_identifier, '').split('&')[0] for a_link in
                            google_news_search_tree.xpath('//a//@href') if forwarding_identifier in a_link]    
    return other_news_sources_links
    
def fnGenerateHTML(other_news_sources_links):
    genHTML=""
    i=1
    other_news_sources_links=set(other_news_sources_links)   
    other_news_sources_links=list(other_news_sources_links)  
        
    for item in other_news_sources_links[:4]:
        username,keyw,senti,titl,dt,txt=fnNewsArticle(item) 
        if len(username) > 1:
            genHTML=genHTML + fnGenerateHTML_Temp(username,keyw,senti,titl,item,dt,txt,i)
            i=i+1
        
    return genHTML
    
    
def fnGenerateHTML_Temp(username,keyw,senti,titl,item,dt,txt,i): 
    strHTML1 = "" 
    strHTML2 ="" 
    strHTML3 =""
    if len(username)>100:
        fnCreate_WordCloud(i,txt)   
        strHTML1="<tr><td width='50%' align='justify'><a href=" + str(item) + ">" + str(titl) + "</a> &nbsp;&nbsp;&nbsp;" + str(dt) + "<br>" + str(username) + "</td>"
        strHTML2="<td width='35%' align='right'>" +  '<img src=/static/images/img/' + str(i) + '.png>'  + "</td></tr>"
        strHTML3="<td width='15%' align='right'>" + str(senti)  + "</td>"                                                     
    
    return strHTML1  + strHTML3    + strHTML2
    
   
 
        
def fnNewsKeywords(url):      
    year, month, day = datetime.date.today().timetuple()[:3]
    dayP=1
    if day>5:
        dayP=day-5      
    key=NewsDetails(query=url, month=month, from_day=dayP, to_day=day, year=16)
    return key 
    

def fnNewsArticle(url):       
        article=Article(url)
        article.download()
        article.parse()
        titl=article.title  
        txt=article.text
        
        if "Subscribe" in titl or "Sign In" in txt or "redirected" in txt:
            username, keyw,senti,titl,dt,txt="","","",titl,"",""   
            return  username, keyw,senti,titl,dt,txt
        
        else:            
            article.nlp()        
            username=article.summary        
            keyw=article.keywords                            
            t = TextBlob(username)
            senti=t.sentiment.polarity
            dt=article.publish_date            
            try:
                now = parse(str(dt))
                dt = now.date()
            except Exception:
#                dt=date.today()
                pass       
            return  username, keyw,senti,titl,dt,txt
    
    
            

def is_href(url):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    if len(urls)>0 :
        return True
    else:
        return False 
        
        
def NewsDetails(**params):
    #keywrds = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A3%2F1%2F13%2Ccd_max%3A3%2F2%2F13&as_nsrc=Gulf%20Times&authuser=0'
    keywrds="https://www.google.com/search?q={query}&tbs=cdr%3A1%2Ccd_min%3A01%2F{month}%2F{year}%2Ccd_max%3A{to_day}%2F{month}%2F{year}&tbm=nws"
    page = requests.get(keywrds.format(**params))
    return html.fromstring(page.text)





#      
#username=find_other_news_sources('Bombardier  Airbus')  
#key=fnGenerateHTML(username) 


      







      
#username=find_other_news_sources('rio tinto')  
#key=fnGenerateHTML(username) 
