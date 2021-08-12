from os import name
from django.contrib import admin
from django.urls import path, include
import movie.views as view

urlpatterns = [
    path('index/', view.index, name='index'),
    path('', view.rank, name='rank'),
    path('near-theater/', view.nearTheater, name='nearTheater'),
    path('timetable/', view.timetable, name='timetable'),
    path('location/', view.location, name='location'),
    path('selectseat/', view.selectseat, name='selectseat'),
]