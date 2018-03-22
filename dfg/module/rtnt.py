# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:32:19 2016

@author: 703106491
"""
#from six.moves.urllib.request import urlopen as pdfweb
#from bs4 import BeautifulSoup
from dateutil.parser import parse
from newspaper import Article
from textblob import TextBlob
import xlwings as xw
import urllib.request
import urllib.error
import os
import re
import io
import os.path as path
import glob
import wget
#import PyPDF2
from gensim.summarization import summarize
from wordcloud import WordCloud, STOPWORDS
import datetime as dt   

#
from module.tf_idf_final import fnMainModel
from module.pdf_mine import fnPdf_Extract
#from tf_idf_final import fnMainModel
#from pdf_mine import fnPdf_Extract

#
#def fnGet_Text_pdf(url):
#    remote_file = pdfweb(url).read()
#    memory_file = io.BytesIO(remote_file)
#    pdf = PyPDF2.PdfFileReader(memory_file)       
#    txt = pdf.getPage(0).extractText()
#    ttle=pdf.getDocumentInfo().title 
#    return ttle, txt

def fnNewsArticle_RTNT(url):       
        article=Article(url)
        article.download()
        article.parse()
        txt=article.text
        article.nlp()  
        keyw=article.keywords
        titl=article.title  
        
        username=fnMainModel(titl, txt)       #        username=article.summary  
               
        t = TextBlob(username)
        senti=t.sentiment.polarity
        dt=article.publish_date
        try:
            now = parse(str(dt))
            dt = now.date()
        except Exception:
            pass       
        return  username, keyw,senti,titl,dt,txt
    
             
def get_next_url(url):
    stErr =''
    
    try:   
        req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req,timeout=10).read().decode('utf8')

    except (UnicodeDecodeError, urllib.error.URLError, urllib.error.HTTPError) as e:
#        print(e)
        str1=str(e)
        if str1.find("decode")> 0:
            stErr='pdf'  
        else:  
            if e.code == 406:
                stErr='pdf'  
            elif e.code == 401:
                stErr='not authorized'
            elif e.code == 404:
                stErr= 'not found'
            elif e.code == 503:
                stErr= 'service unavailable'
            else:
                stErr='unknown error: '
    else:        
        stErr ='success'  
#        
    if stErr =='success': 
        file_type="html"
        
    elif stErr=='pdf':
       file_type="pdf"
       
    else:     
       file_type=""
   
    return file_type,stErr  

def is_href(url):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    if len(urls)>0 :
        return True
    else:
        return False 
    
def fnLinks_Type(url):
    fext=os.path.splitext(url)[1]  
    
    if is_href(url)==True:
        return "url"    
    elif fext == ".xlsm" :  
        return ".xlsm"       
    else: 
        return "pdf"

def fnExcel_Read(file):
    wkb = xw.Book(file) 
    sh = wkb.sheets['Links']   #if wkb.sheet_by_index(0).name=="Link":
    i=2  
    a="1"
    while sh.range((i,2)).value !=None:
        url = sh.range((i,2)).value 
        fext=fnLinks_Type(url)              
        if fext =="url":
            a,b=get_next_url(url) 
        elif fext == ".xlsm" : 
            a="Excel File"              
        else:              
           a="None"                    
               
        sh.range((i,3)).value=a       
        i=i+1     
        return 


#
def fnCPath():
    d = path.dirname(__file__)
    parent_dir = path.abspath(d )  
    return parent_dir

def fnDeleteAllFile_pdf():   
    parent_dir =  fnCPath()
    d=path.join(parent_dir,r'db\temp' )    
    filelist = glob.glob(d + "\*.pdf")
    for f in filelist:
        os.remove(f)
        
def fnDownloadFile(file_url):   
    parent_dir =  fnCPath()
    d=path.join(parent_dir,r'db\temp' ) 
    file_name = wget.download(file_url,d)     
#    pdf = PyPDF2.PdfFileReader(file_name)       
#    txt = pdf.getPage(0).extractText()
#    ttle=pdf.getDocumentInfo().title 
                            
    return file_name


def fnNewsArticle_RTNT_pdf_url(url):   
    file_name=fnDownloadFile(url)
    txt=fnPdf_Extract(file_name)
    txt=txt.split("$ (cid", 1)[0]
    titl=summarize(txt, word_count=10)
    username=fnMainModel(titl, txt)     
    t = TextBlob(username)
    senti=t.sentiment.polarity
    dtt = dt.datetime.today().strftime("%m/%d/%Y")
    keyw=""    
    return  username, keyw,senti,titl,dtt,txt

    
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

    
def fnGenerateHTML_Temp(username,keyw,senti,titl,item,dt,txt,i): 
    strHTML1 = "" 
    strHTML2 ="" 
    strHTML3 =""
    if len(username)>100:  
        strHTML1="<tr><td width='50%' align='justify'><a href=" + str(item) + ">" + str(titl) + "</a> &nbsp;&nbsp;&nbsp;" + str(dt) + "<br>" + str(username) + "</td>"
        strHTML2="<td width='35%' align='right'>" +  " "  + "</td></tr>"
        strHTML3="<td width='15%' align='right'>" + " "  + "</td>"                                                     
    
    return strHTML1  + strHTML3    + strHTML2

def fnNewsArticle_RTNT_excel_url(file): 
    wkb = xw.Book(file) 
    sh = wkb.sheets['Links']   #if wkb.sheet_by_index(0).name=="Link":
    i=2 
    genHTML=""
    while sh.range((i,1)).value !=None:
        url = sh.range((i,1)).value  
        if is_href(url)==True:
            ftype,sterr=get_next_url(url)
            if ftype == "pdf" :             
                username,keyw,senti,titl,dt,txt=fnNewsArticle_RTNT_pdf_url(url) 
                genHTML=genHTML + fnGenerateHTML_Temp(username,keyw,senti,titl,url,dt,txt,i)
                                        
            else:                  
                username,keyw,senti,titl,dt,txt=fnNewsArticle_RTNT(url)
                genHTML=genHTML + fnGenerateHTML_Temp(username,keyw,senti,titl,url,dt,txt,i)
                       
        sh.range((i,2)).value=i       
        i=i+1                           
    return titl, genHTML                      

    
#f=r"D:\webserver\webapp\module\db\Test.xlsm"    
#fnNewsArticle_RTNT_excel_url(f)    
    
    
#attachment=[]
#bodytxt="Actualemail"
#subtxt="Subject"
#attachment.append(r"D:\python\Python\Text Mining\Gulrez\ip\pdfs\2017-07-18 Alkane Resources - Quarterly Activities Report to 30 June 2017.pdf")
#attachment.append(r"D:\python\Python\Text Mining\Gulrez\ip\pdfs\2017-07-20 Mineral Deposits Limited – (Presentation) Noosa Mining Conference.pdf")

#fnNewsArticle_RTNT_pdf_url
    
#fnMailDraft(bodytxt,subtxt,attachment)


    

#url = 'http://files.shareholder.com/downloads/TRX/4050984638x0x940911/52A3802E-EB1C-4E26-9CA9-B4CEC3B29ED3/TROX_News_2017_5_3_Financial_Releases.pdf'
#url='http://www.sheffieldresources.com.au/irm/PDF/2858_0/SheffieldSignsCornerstoneIlmeniteMOU'
#




  
