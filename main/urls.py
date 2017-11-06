from django.conf.urls import url

from django.views.generic import RedirectView
from django.contrib.staticfiles.views import serve

from . import views




urlpatterns = [

    url(r'^$', serve,kwargs={'path': 'index.html'}),    
    url(r'^houses/(?P<lat>\d+\.\d+)/(?P<longitude>\d+\.\d+)/$', views.house, name='house'),
    url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
    RedirectView.as_view(url='/static/%(path)s', permanent=False)),

    

]