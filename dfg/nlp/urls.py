"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# MyApp/urls.py
from django.conf.urls import url, include
from nlp import views
#from . import views
from django.views.generic import TemplateView

urlpatterns = [#'MyApp.views',
    
    url(r'^signin/$', views.signin, name = 'signin'),
    
    url(r'^LTT/$', views.LTTpageView.as_view()),  
    url(r'^BCR/$', views.BCRpageView.as_view()),            
    url(r'^RTNT/$', views.RTNTpageView.as_view()),                
    url(r'^$', views.MainPageView.as_view()),
    url(r'^TSA/$', views.TSApageView.as_view()),  
    url(r'^AFT/$', views.AFTpageView.as_view()),  
    url(r'^ACT/$', views.ACTPageView.as_view()), # Add this /about/ route
    
#    url(r'^$', views.HomePageView.as_view()),
    url(r'^CID/$', views.CIDPageView.as_view()), # Add this /about/ route
    url(r'^login/$', views.NATPageView.as_view(template_name = 'login.html')), # Add this /about/ route
    url(r'^home/$', views.HomePageView.as_view(template_name = 'index.html')), # Add this /about/ route
    url(r'^aboutus/$', views.AboutUSPageView.as_view(template_name = 'AboutUs.html')), # Add this /about/ route
    url(r'^SAN/$', views.SANPageView.as_view()), # Add this /about/ route
    url(r'^FAT/$', views.FATPageView.as_view()), # Add this /about/ route
    
    url(r'^act/act/$', views.act, name = 'act'),
    url(r'^aft/aft/$', views.aft, name = 'aft'),
    url(r'^bcr/bcr/$', views.bcr, name = 'bcr'),   
    url(r'^ltt/ltt/$', views.ltt, name = 'ltt'), 
    url(r'^rtnt/rtnt/$', views.rtnt, name = 'rtnt'),   
    url(r'^login/login/$', views.login, name = 'login'),
    url(r'^cid/cid/$', views.cid, name = 'cid'),
    url(r'^fat/fat/$', views.fat, name = 'fat'),
    url(r'^tsa/tsa/$', views.tsa, name = 'tsa'),
    

    url(r'^test/$', views.TestpageView.as_view()), 
    url(r'^test/test/$', views.test, name = 'test'),
    
       
]   


