# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:06:48 2017

@author: 703106491
"""
from django.http import HttpResponse

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
import os.path as path
import glob, os
import pandas as pd

#from module.rtnt import fnExcel_Read, get_next_url, fnNewsArticle_RTNT,fnNewsArticle_RTNT_pdf_url,fnNewsArticle_RTNT_excel_url
from module.nas  import find_other_news_sources, fnGenerateHTML_Temp, fnGenerateHTML, fnNewsArticle, is_href
from module.plugins.tests.image_scan import fnMain, fnMain1, LTT_Main  

from module.plugins.tests.email_ph import fnExtractAll 
from module.email import fnMailDraft
from module.Twitter_Senti import fnTwitter_Charts
from module.fptr import fnFPT
from module.FPT import fnFPTMain_Dwnld
from module.aspects_chart import fnChart_ACT



def fnDeleteAllFile():
    d = path.dirname(__file__)
    parent_dir = path.abspath(d )  
    d=path.join(parent_dir,r'static\images\img' )    
    filelist = glob.glob(d + "\*.png")
    for f in filelist:
        os.remove(f)


def test(request):   
    path=request.POST['path'] 
    path=settings.MEDIA_ROOT + "----------------" + path
#    txt,ctxt,lng = fnCreate_Card_Scan(path)    
#    username=(fnGenerateHTML_BCR(txt,ctxt,path,lng))    
    return render(request, 'bcrr.html', {"username" : path})   


#------------------------------START LTT---------------------------------------------------------------------------------------
def ltt(request):   
    path=request.POST['path'] 
    txt,lng = fnMain(path)
    return render(request, 'bcrr.html', {"username" : txt})     
#------------------------------END LTT---------------------------------------------------------------------------------------
    

    
##-------------------------------ACT-------------------------------------------------------------------------------------
def act(request):
    pd.set_option('display.max_colwidth',150)
#    pd.set_option('display.max_colwidth', -1)    
    fnDeleteAllFile()
    hotel_loc=request.POST['hotel_name']  
   
    if 'btnform1' in request.POST:         
        df_smpl, df_wfn, df_ldan, htmn, script3n, div3n, df_wfp,df_ldap, htmp, script3p, div3p, df_all, df_lda, htm, df_wf, script, div,script1, div1,script2, div2,script3, div3=fnChart_ACT(hotel_loc)  
        
        hotel_loc1=hotel_loc.split('.')[0]     
        #"df_smpl" : df_smpl.to_html(index=False)
        dict1={"df_smpl" : hotel_loc1, "df_ldan" : df_ldan.to_html(index=False), "htmn" : htmn, "tblwfn" : df_wfn.to_html(index=False), "div3n" : div3n, "script3n" : script3n, "df_ldap" : df_ldap.to_html(index=False), "htmp" : htmp, "tblwfp" : df_wfp.to_html(index=False), "div3p" : div3p, "script3p" : script3p,"tblwf" : df_wf.to_html(index=False), "tblall" : df_all.to_html(index=False), "div3" : div3, "script3" : script3, "df_lda" : df_lda.to_html(index=False) ,"htm" : htm, "days" : hotel_loc1.upper(), "div1" : div1, "script1" : script1,"div" : div, "script" : script,"div2" : div2, "script2" : script2  }               
        return render(request, 'actr.html', dict1)   
    
    else:        
        dict1=dict({})
        return render(request, 'actr.html', dict1) 
#  dict1=dict({})
#  return render(request, 'actr.html', dict1)   
##-------------------------------ACT-------------------------------------------------------------------------------------


#-------------------------------AFT-------------------------------------------------------------------------------------
def aft(request):
    routes=request.POST['username']          
    days=request.POST['info'] 
    
    if 'btnform2' in request.POST:  
        script1, div1, script2, div2, script3, div3, script4, div4 ,script5, div5, days =fnFPT(routes,days)
        dict1={"div1" : div1,"div2" : div2,  "script1" : script1, "script2" : script2,"div3" : div3,  "script3" : script3,"div4" : div4,  "script4" : script4 ,"div5" : div5,  "script5" : script5 , "days":days}     
        return render(request, 'aftr.html', dict1)     
    else: 
        fnFPTMain_Dwnld(days)
        return HttpResponse("Download completed for all routes with - " + days + " Days Lagging!") 
         
#-------------------------------AFT-------------------------------------------------------------------------------------
    


    
#-------------------------------TSA----------------------------------------------------------------------------------------------------------------------
def tsa(request):
    fnDeleteAllFile()
    stCrit=request.POST['username']        # "cseries"      
  
    pd.set_option('display.max_colwidth',150)
    
    cnt, dtt, df,df2,script, div, script2,div2, df3, script3, div3, script4, div4, script5, div5, df5, script6, div6, df6,htm =fnTwitter_Charts(stCrit)
                                                                                
    dict1={"txt" : df6.to_html() ,"htm" : htm ,"cnt" : cnt ,"dtt" : dtt, "username" : df2.to_html() ,"df2" : df.to_html(),"script" : script,"div" : div,"arln_name" : stCrit,"script2" : script2,"div2" : div2,   "df3" : df3.to_html(),  "script3" : script3,"div3" : div3,  "script4" : script4,"div4" : div4,  "script5" : script5,"div5" : div5, "df5" : df5.to_html(), "script6" : script6,"div6" : div6}                                                           
    
    return render(request, 'tsar.html', dict1)

#-------------------------------TSA----------------------------------------------------------------------------------------------------------------------   
 
        
#-------------------------------NAS----------------------
def login(request):
    url=request.POST['username']
    fnDeleteAllFile()
    if is_href(url)==True:
        username,keyw,senti,titl,dt,txt=fnNewsArticle(url)
        username=(fnGenerateHTML_Temp(username,keyw,senti,titl,url,dt,txt,1))
        return render(request, 'loggedin.html', {"username" : username})
        #return render(request, 'loggedin.html', {"username" : username,"keyw" : keyw,"senti" : senti})     
    else:      
        username=find_other_news_sources(url)  
        key=fnGenerateHTML(username)       
        return render(request, 'loggedin.html', {"username" : key})  
    
def signin(request):
    username = password = ''
    username = request.POST['username']
    password = request.POST['password'] 
    if username=="dfg" and password == "genpact":
        return render(request, 'index.html', context=None)   
    else:
        username="Wrong user id and password! try again"
        return render(request, 'error.html', {"username" : username}) 
   
    
def cid(request):   
    path=request.POST['path']  
    return render(request, 'bcrr.html', {"username" : path})   

def fat(request):   
    path=request.POST['path']  
    return render(request, 'bcrr.html', {"username" : path})   


#-------------------------------BCR----------------------
def fnGenerateHTML_BCR(txt,ctxt,path,lng): 
    strHTML1 = "" 
    strHTML2 ="" 
    strHTML3 =""
    fname=os.path.basename(path)
    if len(txt)>5:          
        strHTML1="<tr><td width='30%' align='left'> Language:- '" + str(lng) + "'&nbsp;<br><br>" + str(txt) + "</td>"
        strHTML2="<td width='40%' align='right'>" +  '<img src=/static/bcard/' + str(fname) + ' width="400" high="300">'  + "</td></tr>"
        strHTML3="<td width='30%' align='right'>" + str(ctxt)  + "</td>"                                                     
    
    return strHTML1  + strHTML3    + strHTML2

def fnCreate_Card_Scan(path):    
    txt,lng=fnMain(path)
    ctxt=fnMain1(txt)
    return txt,ctxt,lng


def bcr(request):   
    path=request.POST['path'] 
    txt,ctxt,lng = fnCreate_Card_Scan(path)
    numbers, emails, names= fnExtractAll(txt)
    
    df1 = pd.DataFrame(list(ctxt.items()), columns=['Entity', 'Value'])    
    dic = dict( PHONE = numbers, EMAILS = emails, NAMES= names)
    df2 = pd.DataFrame(list(dic.items()), columns=['Entity', 'Value'])            

    df=df1.append(df2)   
    ctxt= df.to_html(index=False)

    username=(fnGenerateHTML_BCR(txt,ctxt,path,lng))
    return render(request, 'bcrr.html', {"username" : username})     
#------------------------------END BCR----------------------


# 
##-------------------------------RTNT----------------------
def rtnt(request):
#    url=request.POST['username']    
#    fnDeleteAllFile()
##    fnDeleteAllFile_pdf()
#    if is_href(url)==True:
#        ftype,sterr=get_next_url(url)
#        if ftype == "pdf" :
#            username,keyw,senti,titl,dt,txt=fnNewsArticle_RTNT_pdf_url(url) 
#            username=(fnGenerateHTML_Temp(username,keyw,senti,titl,url,dt,txt,1))
#            return render(request, 'loggedin.html', {"username" : username})
#        else:    
#            username,keyw,senti,titl,dt,txt=fnNewsArticle_RTNT(url)
#            username=(fnGenerateHTML_Temp(username,keyw,senti,titl,url,dt,txt,1))
#            return render(request, 'loggedin.html', {"username" : username})
#    
#    else:          
#        fext=os.path.splitext(url)[1]       
#  
#        if fext == ".xlsm" :
#            titl,key=fnNewsArticle_RTNT_excel_url(url)   
#            attachment=[]
#            bodytxt="Actualemail"
#            subtxt=titl
#            attachment.append(r"D:\dfg\dfg\module\db\temp\SheffieldSignsCornerstoneIlmeniteMOU.pdf")
#            attachment.append(r"D:\dfg\dfg\module\db\temp\TROX_News_2017_5_3_Financial_Releases.pdf")
#
#            fnMailDraft(bodytxt,subtxt,attachment,key)
#            return render(request, 'loggedin.html', {"username" : key})  
#                
#        elif fext == ".pdf" :  
#            username="pdf file:- " + url 
#            return render(request, 'loggedin.html', {"username" : username})
#        else:            
#            username=find_other_news_sources(url)  
#            key=fnGenerateHTML(username) 
#            return render(request, 'loggedin.html', {"username" : key})          

    username="pdf file:- " 
    return render(request, 'loggedin.html', {"username" : username})

#-------------------------------Main function-------------------------------

# Create your views here.
class MainPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'main.html', context=None)
    
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class RTNTpageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'RTNT.html', context=None)    

class BCRpageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'BCR.html', context=None)   

class LTTpageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'LTT.html', context=None)   

class TSApageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'TSA.html', context=None)   

class AFTpageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'AFT.html', context=None)  
        
class FATPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'FAT.html', context=None)    
        
class CIDPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'CID.html', context=None)    
        
class SANPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'SAN.html', context=None)    

class ACTPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'ACT.html', context=None)   

class NATPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)            

class AboutUSPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'AboutUs.html', context=None)   

class submit(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'CID.html', context=None) 
          
    
    
class TestpageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'test.html', context=None)  
        
        
    
    
    
    
    
    
    