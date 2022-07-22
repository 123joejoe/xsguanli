from django.contrib import admin
from django.urls import re_path,include
from booktest import views

urlpatterns = [
    re_path(r'^index$',views.index),
    re_path(r'^add$',views.add),
    re_path(r'^add_check$',views.add_check),
    re_path(r'^delete$',views.delete),
    re_path(r'^delete_check$',views.delete_check),
    re_path(r'^change$',views.change),
    re_path(r'^change_check$',views.change_check),
    re_path(r'^find$',views.find),
    re_path(r'^find_check$',views.find_check),
    # re_path(r'^excel$',views.excel),
    re_path(r'^weather_check$',views.weather_check),
]
