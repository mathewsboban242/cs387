"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
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
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import render,redirect
from django.db import connection 
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
def login_handler(request):
	if request.method == 'GET' :
		return render(request,'orders/login.html')
	elif request.method == 'POST' :
		username=request.POST['username']
		password=request.POST['password']
		with connection.cursor() as cursor:
			cursor.execute("select * from addausers where loginname = %s and password = %s",(username,password))
			header=[i[0] for i in cursor.description]
			rows=cursor.fetchall()
			if(rows):#rows is not empty
				request.session['loginname']=str(rows[0][0])
				request.method="GET"
				return redirect(order_handler)
			else:
				return render(request,'orders/login.html')

@csrf_exempt
def order_handler(request):
	if request.method == 'GET' :
		with connection.cursor() as cursor:
			sql = "select orderId,item,itemQuantity,dateTime from public.order natural join orderitem where loginname = '{0}' order by datetime DESC".format(request.session['loginname'])
			cursor.execute(sql)
			header=[i[0] for i in cursor.description]
			rows=cursor.fetchall()
			table_html="<table> <tr><th>Order Id</th><th>Item</th><th>Quantity</th><th>Date & Time</th> </tr>"
			for i in range(0,min(5,len(rows))):
				table_html+="<tr>"
				table_html+="<td>"+str(rows[i][0])+"</td>"
				table_html+="<td>"+str(rows[i][1])+"</td>"
				table_html+="<td>"+str(rows[i][2])+"</td>"
				table_html+="<td>"+str(rows[i][3])+"</td>"
				table_html+="</tr>"
			table_html+="</table>"
		d1={'table':table_html}
		return render(request,'orders/order_handler.html',d1)
	elif request.method == 'POST' :
		st1=""
		with connection.cursor() as cursor:
			idli_no=request.POST['idli']
			if(not idli_no):
				idli_no=0
			samosa_no=request.POST['samosa']
			if(not samosa_no):
				samosa_no=0
			chai_no=request.POST['chai']
			if(not chai_no):
				chai_no=0

			now = datetime.datetime.now()
			err=0
			st1="""<div id="status" style="color:green"> Success! Your Order Ids are"""

			# try:
			if(int(idli_no)>0):
				sql1 = "insert into public.order values (DEFAULT,'{}','{}') returning orderId".format(request.session['loginname'],now)
				cursor.execute(sql1)
				rows1=cursor.fetchall()
				# print(rows1)
				sql2="insert into orderitem values (DEFAULT,'idli','{}')".format(idli_no)
				cursor.execute(sql2)
				st1+=" "+str(rows1[0][0])


			if(int(samosa_no)>0):
				sql1 = "insert into public.order values (DEFAULT,'{}','{}') returning orderId".format(request.session['loginname'],now)
				cursor.execute(sql1)
				rows2=cursor.fetchall()
				# print(rows2)
				sql2="insert into orderitem values (DEFAULT,'samosa','{}')".format(samosa_no)
				cursor.execute(sql2)
				st1+=" "+str(rows2[0][0])


			if(int(chai_no)>0):
				sql1 = "insert into public.order values (DEFAULT,'{}','{}') returning orderId".format(request.session['loginname'],now)
				cursor.execute(sql1)
				rows3=cursor.fetchall()
				# print(rows)
				sql2="insert into orderitem values (DEFAULT,'chai','{}')".format(chai_no)
				cursor.execute(sql2)
				st1+=" "+str(rows3[0][0])
			st1+="""</div>"""

			# except:
				# err=1
			sql = "select orderId,item,itemQuantity,dateTime from public.order natural join orderitem where loginname = '{0}' order by orderId DESC".format(request.session['loginname'])
			cursor.execute(sql)
			header=[i[0] for i in cursor.description]
			rows=cursor.fetchall()
			table_html="<table> <tr><th>Order Id</th><th>Item</th><th>Quantity</th><th>Date & Time</th> </tr>"
			for i in range(0,min(5,len(rows))):
				table_html+="<tr>"
				table_html+="<td>"+str(rows[i][0])+"</td>"
				table_html+="<td>"+str(rows[i][1])+"</td>"
				table_html+="<td>"+str(rows[i][2])+"</td>"
				table_html+="<td>"+str(rows[i][3])+"</td>"
				table_html+="</tr>"
			table_html+="</table>"
			if(err==0):
				# st1="""<div id="status" style="color:green"> Success! Your Order Ids are {},{} and {} </div>""".format(str(rows1[0][0]),str(rows2[0][0]),str(rows3[0][0]))
				x=1
			else:
				st1="""<div id="status" style="color:red">Error!</div>"""
				err=0	
		d1={'table':table_html,'st1':st1}
		return render(request,'orders/order_handler.html',d1)
		
		

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_handler),
    path('add', order_handler),
    path('orders/', order_handler),
]
