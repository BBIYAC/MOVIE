import os
import json
from pathlib import Path
from datetime import datetime
from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.csrf import csrf_exempt

from core.boxoffice import BoxOffice
from core.location import Location
from core.theater.lottecinema import LotteCinema
from core.theater.cgv import CGV


BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_boxOffice_api(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} boxoffice api variable".format(setting)
        raise ImproperlyConfigured(error_msg)


def get_location_api(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} location api variable".format(setting)
        raise ImproperlyConfigured(error_msg)


BOXOFFICE_API_KEY = get_boxOffice_api("BOXOFFICE_API_KEY")
LOCATION_API_KEY = get_location_api("LOCATION_API_KEY")


@csrf_exempt
def index(request):
    data = 'index page'
    return render(request, 'movie/index.html', {'data': data})


@csrf_exempt
def rank(request):
    response_data = {}

    box = BoxOffice(BOXOFFICE_API_KEY)
    movies = box.get_movies()
    movie_lists = box.simplify(movies)

    for movie_list in movie_lists:
        rank = movie_list['rank']
        response_data[rank] = movie_list

    return render(request, 'movie/rank.html', {'datas': response_data})


@csrf_exempt
def nearTheater(request):
    cinema = LotteCinema()
    location = Location(LOCATION_API_KEY)
    myloc = location.get_location()
    lat = myloc['lat']
    lng = myloc['lng']

    theater_lists = cinema.filter_nearest_theater(cinema.get_theater_list(), lat, lng)

    return render(request, 'movie/nearTheater.html', {'datas': theater_lists})


@csrf_exempt
def timetable(request):
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%m')
    location = Location(LOCATION_API_KEY)
    movie_name = request.POST.get('selected_movie')
    date = request.POST.get('date')
    if request.POST.get('moviePlace'):
        movie_place = request.POST.get('moviePlace')
        findLoc = location.get_place_location(movie_place)
        lat = findLoc['lat']
        lng = findLoc['lng']
    else:
        movie_place = 'here'
        myloc = location.get_location()
        lat = myloc['lat']
        lng = myloc['lng']

    # LOTTE
    lotte_theater_info = []
    Lcinema = LotteCinema()
    lotte_theater_lists = Lcinema.filter_nearest_theater(Lcinema.get_theater_list(), lat, lng)

    for lotte_theater in lotte_theater_lists:
        lotte_movie_schedules = []
        theaterID = lotte_theater.get('TheaterID')
        theaterName = lotte_theater.get('TheaterName')
        theaterLng = lotte_theater.get('Longitude')
        theaterLat = lotte_theater.get('Latitude')
        movie_lists = Lcinema.get_movie_list(theaterID, date)
        # print(f"theaterID: {theaterID}, theaterName: {theaterName}, theaterLng: {theaterLng}, movie_lists: {movie_lists}")

        for key, value in movie_lists.items():
            # print(key, value)
            if value.get('Name') == movie_name:
                # print(key, value)
                schedules = value.get('Schedules')
                # print(schedules)
                lotte_movie_schedules.append(schedules)

        if not lotte_movie_schedules:
            lotte_movie_schedules.append({'StartTime': 'None', 'RemainingSeat': 'None'})

        # print(lotte_movie_schedules)
        # print(type(lotte_movie_schedules))

        lotte_theater_info.append({
            'TheaterID': theaterID,
            'TheaterName': theaterName,
            'Longitude': theaterLng,
            'Latitude': theaterLat,
            'MoiveLists': lotte_movie_schedules
        })
        # print("---")
    # print(lotte_theater_info)

    # CGV
    cgv_theater_info = []
    Ccinema = CGV()
    cgv_theater_lists = Ccinema.filter_nearest_theater(Ccinema.get_theater_list(), lat, lng)

    for cgv_theater in cgv_theater_lists:
        # print(cgv_theater)
        cgv_movie_schedules = []
        theaterID = cgv_theater.get('TheaterCode')
        theaterName = cgv_theater.get('TheaterName')
        theaterLng = cgv_theater.get('Longitude')
        theaterLat = cgv_theater.get('Latitude')
        areacode = cgv_theater.get('RegionCode')
        movie_lists = Ccinema.get_movie_list(areacode, theaterID, date)
        # print(f"theaterID: {theaterID}, theaterName: {theaterName}, theaterLng: {theaterLng}, movie_lists: {movie_lists}")

        for key, value in movie_lists.items():
            # print(key, value)
            if value.get('Name') == movie_name:
                # print(key, value)
                schedules = value.get('Schedules')
                # print('---')
                schedules = schedules[0]
                # print(schedules)
                # print(type(schedules))
                for schedule in schedules:
                    handle_scedule_data = []
                    # print(f"schedule: {schedule}")
                    startTime = schedule[0]
                    remainingSeat = schedule[1][4:-1]
                    handle_scedule_data.append({
                        'StartTime': startTime,
                        'RemainingSeat': remainingSeat
                    })
                    # print(handle_scedule_data)
                    cgv_movie_schedules.append(handle_scedule_data)


        if not cgv_movie_schedules:
            cgv_movie_schedules.append({'StartTime': 'None', 'RemainingSeat': 'None'})

        # print(f"cgv_movie_schedules: {cgv_movie_schedules}")
        # print(f"cgv_movie_schedules: {type(cgv_movie_schedules)}")

        cgv_theater_info.append({
            'TheaterID': theaterID,
            'TheaterName': theaterName,
            'Longitude': theaterLng,
            'Latitude': theaterLat,
            'MoiveLists': cgv_movie_schedules
        })
        # print("---")

    # print(lotte_theater_info)
    # print("---")
    # print(cgv_theater_info)

    datas = {
        'now': now,
        'movie_name': movie_name,
        'movie_place': movie_place,
        'lotte_theater_info': lotte_theater_info,
        'cgv_theater_info': cgv_theater_info
    }

    return render(request, 'movie/timetable.html', {'datas': datas})