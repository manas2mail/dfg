# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 12:25:55 2017

@author: 703106491
"""
#from rtnt import fnNewsArticle_RTNT_excel_url

import pythoncom
import win32com.client

def fnMailDraft(bodytxt, subtxt,attachment,genHTML):    
    pythoncom.CoInitialize()
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = subtxt
    
    newMail.To = "manas.kumarghosh@genpact.com"
 
    newMail.HTMLbody = (r"""Hi All, <br><br>
     Please find attached the announcements made by """ + subtxt.partition(' ')[0] + """. I shall upload the documents to the e-room.<br>     
     <br><br> """ + genHTML)
       
    
    newMail.Attachments.Add(attachment[0])
    newMail.Attachments.Add(attachment[1])
    newMail.display()

#a=pythoncom.CoInitialize()
#print(a)
#attachment=[]
#bodytxt="Actualemail"
#subtxt="Subject"
#attachment.append(r"D:\python\Python\Text Mining\Gulrez\ip\pdfs\2017-07-18 Alkane Resources - Quarterly Activities Report to 30 June 2017.pdf")
#attachment.append(r"D:\python\Python\Text Mining\Gulrez\ip\pdfs\2017-07-20 Mineral Deposits Limited – (Presentation) Noosa Mining Conference.pdf")
#
#url=r"D:\webserver\webapp\module\db\Test.xlsm"
#genHTML=fnNewsArticle_RTNT_excel_url(url)  
#    
#fnMailDraft(bodytxt,subtxt,attachment,genHTML)


