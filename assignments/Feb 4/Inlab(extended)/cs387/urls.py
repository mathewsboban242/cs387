"""cs387 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:python3 manage.py startapp badlu

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import datetime
import pprint
from . import counterview
from . import orders
from django.urls import include, path


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>Shoney's India %s.</body></html>" % now
    return HttpResponse(html)

def dict1(request):
    dict1=pprint.pformat(request.__dict__)
    html = "<html><body><pre>"+str(dict1)+"</pre></body></html>"
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/time', current_datetime),
    path('admin/counter', counterview.counter),
    path('admin/dict1', dict1),
    path('badlu/', include('badlu.urls')),
]
