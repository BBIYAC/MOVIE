from django.contrib import admin
from django.urls import path, include
import api.views as view

urlpatterns = [
    path('test/', view.test, name='test'),
    path('movie-rank/', view.movieRank, name='movieRank'),
    path('location/', view.location, name='location'),
    path('near-lottecinema/', view.filter_nearest_lottecinema, name='filter_nearest_lottecinema'),
    path('selected-lottecinema-movie-list/', view.filtered_lottecinema_movie_list, name='filtered_lottecinema_movie_list'),

    path('near-cgv/', view.filter_nearest_cgv, name='filter_nearest_cgv'),
    path('selected-cgv-movie-list/', view.filtered_cgv_movie_list, name='filtered_cgv_movie_list'),
]