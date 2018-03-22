"""dfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


"""## Important : Import the views from the demo folder
## to get the index action"""

#from nlp import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('nlp.urls')), 
]

  
#    url(r'^BCR/$', views.BCRpageView.as_view()),            
#    url(r'^RTNT/$', views.RTNTpageView.as_view()),                
#    url(r'^$', views.HomePageView.as_view()),
#    url(r'^CID/$', views.CIDPageView.as_view()), # Add this /about/ route
#    url(r'^login/$', views.NATPageView.as_view(template_name = 'login.html')), # Add this /about/ route
#    url(r'^SAN/$', views.SANPageView.as_view()), # Add this /about/ route
#    url(r'^FAT/$', views.FATPageView.as_view()), # Add this /about/ route
#    
#    url(r'^bcr/bcr/$', views.bcr, name = 'bcr'),   
#    url(r'^rtnt/rtnt/$', views.rtnt, name = 'rtnt'),   
#    url(r'^login/login/$', views.login, name = 'login'),
#    url(r'^cid/cid/$', views.cid, name = 'cid'),
#    url(r'^fat/fat/$', views.fat, name = 'fat'),
    
#    url(r'', views.index),
#    url(r'', views.HomePageView.as_view()),
#    url(r'^$', TemplateView.as_view(template_name='main.html')),
#    url(r'^$', TemplateView.as_view(template_name='login.html'),name='login'),
#    url(r'^$main', TemplateView.as_view(template_name='index.html'), name='main'),
#    url(r'^login/$', TemplateView.as_view(template_name = 'login.html'), name='nas'),
     





