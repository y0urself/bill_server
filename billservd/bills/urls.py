from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.bills, name='bills'),
    path('new_bill/', views.new_bill, name='new_bill'),
    path('new_bill/submit', views.save_bill, name='save_bill'),
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/$', views.show_bill, name='bill'),
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/edit_bill', views.edit_bill, name='edit_bill'),
    re_path(r'^(?P<bill_id>[1-9][0-9]*)/del_bill', views.del_bill, name='del_bill'),
    path('parts/', views.parts, name='parts'),
    path('parts/<int:part_id>/', views.part, name='part'),
]