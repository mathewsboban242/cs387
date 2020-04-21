from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from urllib.parse import parse_qs

def orders(request):
	r = parse_qs(request.__dict__['META']['QUERY_STRING'])
	html = "<html><body>Your order:<br/>samosas = "+r['samosas'][0]+"<br/>chai = "+r['chai'][0]+"<br/>idli vada = "+r['idli vada'][0]+"</body></html>"
	return HttpResponse(html)
