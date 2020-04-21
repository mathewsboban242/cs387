from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import pprint

ctr=0

def counter(request):
    global ctr
    html = "<html><body>Squanchy's counter measures %d counts.</body></html>" % ctr
    ctr+=1
    return HttpResponse(html)
