from django.urls import path, re_path

from . import views

urlpatterns = [
    # Bills Views
    path('', views.bills, name='bills'),
    path('new_bill/', views.new_bill, name='new_bill'), # new
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/$', views.show_bill, name='bill'), # show bill
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/edit_bill', views.edit_bill, name='edit_bill'), #edit
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/del_bill', views.del_bill, name='del_bill'), # delete
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/dl_bill', views.dl_bill, name='dl_bill'), # download
    # Customers Views
    path('customers/', views.customers, name='customers'),
    path('customers/new_customer/', views.new_customer, name='new_customer'), # new
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/$', views.customer, name='customer'),
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/edit_customer', views.edit_customer, name='edit_customer'),
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/del_customer', views.del_customer, name='del_customer'),
    # Parts Views
    path('parts/', views.parts, name='parts'),
    path('parts/<int:part_id>/', views.part, name='part'),
]