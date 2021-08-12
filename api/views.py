import ast
import os
import json
import math
from pathlib import Path
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from core.boxoffice import BoxOffice
from core.location import Location
from core.theater.lottecinema import LotteCinema
from core.theater.cgv import CGV
from drf_yasg import openapi
from urllib.request import urlopen
from bs4 import BeautifulSoup



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
@api_view(['GET', 'POST'])
def test(request):
    """
    TEST POST

    ---
    """
    if request.method == 'POST':
        response_data = {}
        response_data['result'] = 'POST test'
        response_data['message'] = 'Some test message'

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    elif request.method == 'GET':
        response_data = {}
        response_data['result'] = 'GET test'
        response_data['message'] = 'Some test message'

        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@api_view(['POST', 'GET'])
def movieRank(request):
    '''
    To get movie rank

    ---
    :param request:
    :return:
    {
        "api": "POST Movie Rank",
        "response": "200",
        "1": {
            "rank": "1",
            "name": "모가디슈",
            "code": "20204117"
        },
        "2": {
            "rank": "2",
            "name": "더 수어사이드 스쿼드",
            "code": "20217845"
        },
        "3": {
            "rank": "3",
            "name": "보스 베이비 2",
            "code": "20218391"
        },
        ...
    }

    '''
    response_data = {}
    response_data['api'] = 'POST Movie Rank'

    if request.method == 'POST' or 'GET':
        box = BoxOffice(BOXOFFICE_API_KEY)
        movies = box.get_movies()
        movie_lists = box.simplify(movies)
        response_data['response'] = '200'

        html = urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%95%EC%8A%A4+%EC%98%A4%ED%94%BC%EC%8A%A4+%EC%88%9C%EC%9C%84')
        soup = BeautifulSoup(html,'html.parser')
        movies = soup.find('ul', {'class':'_panel'})
        movieImgs = movies.find_all('li')

        for i, movie_list in enumerate(movie_lists):
            rank = movie_list['rank']
            response_data[rank] = movie_list
            response_data[rank]['img'] = movieImgs[i].find('img')['src']
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@api_view(['POST'])
def location(request):
    '''
    To get my location

    ---
    :param request:
    :return:
    {
        "api": "POST my location",
        "response": "200",
        "location": {
            "lat": 37.5160832,
            "lng": 126.9071872
        }
    }
    '''
    response_data = {}
    response_data['api'] = 'POST my location'

    if request.method == 'POST':
        location = Location(LOCATION_API_KEY)
        myloc = location.get_location()
        response_data['response'] = '200'
        response_data['location'] = myloc
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@api_view(['POST'])
def filter_nearest_lottecinema(request):
    '''
    TO get filtered nearest 3 lottecinema

    ---
    :param request:
    :return:
    {
        "api": "POST lottecinema fileter by location",
        "response": "200",
        "near_theater_lists": [
            {
                "TheaterName": "영등포 롯데시네마",
                "TheaterID": "1|17|1002",
                "Longitude": "126.907755",
                "Latitude": "37.516369"
            },
            {
                "TheaterName": "신도림 롯데시네마",
                "TheaterID": "1|14|1015",
                "Longitude": "126.8889387",
                "Latitude": "37.5086097"
            },
            {
                "TheaterName": "합정 롯데시네마",
                "TheaterID": "1|24|1010",
                "Longitude": "126.9134333",
                "Latitude": "37.5504586"
            }
        ]
    }
    '''
    response_data = {}
    response_data['api'] = 'POST lottecinema fileter by location'

    if request.method == 'POST':
        cinema = LotteCinema()
        location = Location(LOCATION_API_KEY)
        myloc = location.get_location()
        lat = myloc['lat']
        lng = myloc['lng']

        theater_lists = cinema.filter_nearest_theater(cinema.get_theater_list(), lat, lng)

        response_data['response'] = '200'
        response_data['near_theater_lists'] = theater_lists
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@api_view(['POST'])
def filtered_lottecinema_movie_list(request):
    '''
    To get movie list by filtered lottecinema

    ---
    :param request:
    {
        "TheaterID": "1|17|1002"
    }
    :return:
    {
    "api": "POST filetered lottecinema movie list",
    "response": "200",
    "movie_lists": {
            "17616": {
                "Name": "모가디슈",
                "Schedules": [
                    {
                        "StartTime": "14:10",
                        "RemainingSeat": 134
                    },
                    {
                        "StartTime": "16:35",
                        "RemainingSeat": 120
                    },
                    ...
                ]
            },
            "17652": {
                "Name": "더 수어사이드 스쿼드",
                "Schedules": [
                    {
                        "StartTime": "14:10",
                        "RemainingSeat": 91
                    },
                    {
                        "StartTime": "16:50",
                        "RemainingSeat": 86
                    },
                    ...
                ]
            },
            "17623": {
                "Name": "보스 베이비 2",
                "Schedules": [
                    {
                        "StartTime": "17:50",
                        "RemainingSeat": 57
                    }
                ]
            },
            ...
        }
    }
    '''
    response_data = {}
    response_data['api'] = 'POST filetered lottecinema movie list'

    if request.method == 'POST':
        data = json.loads(request.body)
        TheaterID = data.get('TheaterID')
        date = ''
        cinema = LotteCinema()
        movie_list = cinema.get_movie_list(TheaterID, date)

        response_data['response'] = '200'
        response_data['movie_lists'] = movie_list
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# ---------------------------
# CGV

@csrf_exempt
@api_view(['POST'])
def filter_nearest_cgv(request):
    '''
    TO get filtered nearest 3 cgv

    ---
    :param request:
    :return:
    {
        "api": "POST cgv fileter by location",
        "response": "200",
        "near_theater_lists": [
            {
                "TheaterCode": "0059",
                "TheaterName": "CGV영등포",
                "Longitude": 126.9031758,
                "Latitude": 37.5171639,
                "RegionCode": "01"
            },
            {
                "TheaterCode": "0112",
                "TheaterName": "CGV여의도",
                "Longitude": 126.9254109,
                "Latitude": 37.5254692,
                "RegionCode": "01"
            },
            {
                "TheaterCode": "0010",
                "TheaterName": "CGV구로",
                "Longitude": 126.8825372,
                "Latitude": 37.5013174,
                "RegionCode": "01"
            }
        ]
    }
    '''
    response_data = {}
    response_data['api'] = 'POST cgv fileter by location'

    if request.method == 'POST':
        cinema = CGV()
        location = Location(LOCATION_API_KEY)
        myloc = location.get_location()
        lat = myloc['lat']
        lng = myloc['lng']

        theater_lists = cinema.filter_nearest_theater(cinema.get_theater_list(), lat, lng)

        response_data['response'] = '200'
        response_data['near_theater_lists'] = theater_lists
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@api_view(['POST'])
def filtered_cgv_movie_list(request):
    '''
    To get movie list by filtered cgv

    ---
    :param request:
    {
        "areaCode": "01",
        "theatercode": "0001"
    }
    :return:
    {
        "api": "POST filetered cgv movie list",
        "response": "200",
        "movie_lists": {
            "0": {
                "Name": "모가디슈",
                "Schedules": [
                    {
                        "StartTime": "19:30",
                        "RemainingSeat": "27"
                    }
                ]
            },
            "1": {
                "Name": "블랙핑크 더 무비",
                "Schedules": [
                    {
                        "StartTime": "20:00",
                        "RemainingSeat": "110"
                    }
                ]
            },
            "2": {
                "Name": "더 수어사이드 스쿼드",
                "Schedules": [
                    {
                        "StartTime": "19:30",
                        "RemainingSeat": "47"
                    }
                ]
            }
        }
    }
    '''
    response_data = {}
    response_data['api'] = 'POST filetered cgv movie list'

    if request.method == 'POST':
        data = json.loads(request.body)
        areaCode = data.get('areaCode')
        theatercode = data.get('theatercode')
        cinema = CGV()
        movie_list = cinema.get_movie_list(areaCode, theatercode)

        response_data['response'] = '200'
        response_data['movie_lists'] = movie_list
    else:
        response_data['errorr_msg'] = 'you should request POST'
        response_data['response'] = '400'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def filter_nearest_theater(theater_list, pos_latitude, pos_longitude, n=3):
    '''
    To filter by location to get nearest theater count 3
    :param theater_list:
    :param pos_latitude:
    :param pos_longitude:
    :param n:
    :return:
    '''

    def distance(x1, x2, y1, y2):
        '''
        TO get distance (x1, x2) ~ (y1, y2)
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :return:
        '''
        dx = float(x1) - float(x2)
        dy = float(y1) - float(y2)
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance

    distance_to_theater = []
    for theater in theater_list:
        get_distance = distance(pos_latitude, theater.get('Latitude'), pos_longitude, theater.get('Longitude'))
        distance_to_theater.append((get_distance, theater))

    return [theater for distance, theater in sorted(distance_to_theater, key=lambda x: x[0])[:n]]


@csrf_exempt
@api_view(['GET'])
def find_moive_theater(request):
    #location
    lat_string = request.GET['lat']
    lat = float(ast.literal_eval(lat_string))
    lng_string = request.GET['lng']
    lng = float(ast.literal_eval(lng_string))

    #date
    date = request.GET['date']
    date = str(ast.literal_eval(date))

    #movie
    movie_name = request.GET['movie_name']
    movie_name = str(ast.literal_eval(movie_name))

    # print(lat, lng, date, movie_name)
    # print(type(lat), type(lng), type(date), type(movie_name))

    theater_list = []

    # LOTTE
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

        theater_list.append({
            'TheaterID': theaterID,
            'TheaterName': theaterName,
            'Longitude': theaterLng,
            'Latitude': theaterLat,
            'MoiveLists': lotte_movie_schedules
        })
        # print("---")
    # print(lotte_theater_info)

    # CGV
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

        theater_list.append({
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

    theater_info = []
    theater_lists = filter_nearest_theater(theater_list, lat, lng, 3)

    for theater in theater_lists:
        theater_info.append(theater)

    datas = {
        'date': date,
        'theater_info': theater_info,
    }

    return HttpResponse(json.dumps(datas), content_type="application/json")