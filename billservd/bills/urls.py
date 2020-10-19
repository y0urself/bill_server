from django.urls import path, re_path
from django.conf import settings
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),
    path('login/', views.login_req, name='login'),
    # Bills Views
    path('', views.bills, name='bills'),
    path('new_bill/', views.new_bill, name='new_bill'), # new
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/$', views.show_bill, name='bill'), # show bill
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/edit_bill/$', views.edit_bill, name='edit_bill'), #edit
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/del_bill/$', views.del_bill, name='del_bill'), # delete
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/dl_bill/$', views.dl_bill, name='dl_bill'), # download
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/cp_bill/$', views.create_part_payment_bill, name='create_part_bill'), # download
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/dl_pbill/$', views.dl_part_bill, name='dl_part_bill'), # download
    # Actions
    #re_path(r'^new_bill/choose_customer/$', views.choose_customer, name='choose_customer'), # new
    #re_path(r'^(?P<bill_id>[1-9][0-9]*)/edit_bill/choose_customer/$', views.choose_customer, name='choose_customer'), #edit
    # Customers Views
    path('customers/', views.customers, name='customers'),
    path('customers/new_customer/', views.new_customer, name='new_customer'), # new
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/$', views.customer, name='customer'),
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/edit_customer/$', views.edit_customer, name='edit_customer'),
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/del_customer/$', views.del_customer, name='del_customer'),
    re_path(r'^customers/customer/(?P<customer_id>[1-9][0-9]*)/new_bill/$', views.new_bill, name='new_bill_from_customer'), #edit
    # Parts Views
    path('parts/', views.parts, name='parts'),
    path('parts/<int:part_id>/', views.part, name='part'),
]