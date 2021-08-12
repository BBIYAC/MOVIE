import os
import json
import math
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.csrf import csrf_exempt

from core.boxoffice import BoxOffice
from core.location import Location
from core.theater.lottecinema import LotteCinema
from core.theater.cgv import CGV
from urllib.request import urlopen
from urllib.request import quote
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
def index(request):
    data = 'index page'
    return render(request, 'movie/index.html', {'data': data})

def location(request):
    return render(request, 'movie/location.html')


def selectseat(request):
    return render(request, 'movie/selectseat.html')


@csrf_exempt
def rank(request):
    
    movie = {}


    box = BoxOffice(BOXOFFICE_API_KEY)
    movies = box.get_movies()
    movie_lists = box.simplify(movies)



    for movie_list in movie_lists:
        rank = movie_list['rank']
        movie[rank] = movie_list

        base_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
        movie_name = movie_list['name'] 
        search_url = base_url + quote(movie_name)
        html = urlopen(search_url)
        soup = BeautifulSoup(html,'html.parser')
        img_url = soup.select_one('#main_pack > div.sc_new.cs_common_module.case_empasis._au_movie_content_wrap > div.cm_content_wrap > div.cm_content_area._cm_content_area_info > div.cm_info_box > div.detail_info > a > img')['src']
        movie[rank]['img'] = img_url

    location = Location(LOCATION_API_KEY)

    if request.POST.get('location'):
        movie_place = request.POST.get('location')
        myadd = location.get_place_location(movie_place)['address']
        address = myadd
        response_data = {'movie': movie, 'address': address}
    else:
        myloc = location.get_location()
        lat = myloc['lat']
        lng = myloc['lng']
        address = location.get_address(lat, lng)['address']
        response_data = {'movie': movie, 'address':address}

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
            distance = math.sqrt(dx**2 + dy**2)
            return distance

        distance_to_theater = []
        for theater in theater_list:
            get_distance = distance(pos_latitude, theater.get('Latitude'), pos_longitude, theater.get('Longitude'))
            distance_to_theater.append((get_distance, theater))

        return [theater for distance, theater in sorted(distance_to_theater, key=lambda x: x[0])[:n]]



@csrf_exempt
def movie_list(request):
    movie_name = request.GET['movie_name']
    img_url = request.GET['img_url']
    
    datas = {
       "movie_name": movie_name,
       "img_url": img_url
    }

    print(datas)

    return render(request, 'movie/timetable.html', {'datas': datas})


def get_movie_poster(movie_name):
    base_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    search_url = base_url + quote(movie_name)
    html = urlopen(search_url)
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.select_one(
        '#main_pack > div.sc_new.cs_common_module.case_empasis._au_movie_content_wrap > div.cm_content_wrap > div.cm_content_area._cm_content_area_info > div.cm_info_box > div.detail_info > a > img')[
        'src']
    return img_url


@csrf_exempt
def timetable(request):

    movie_name = request.GET['movie_name']
    address = request.GET['address']
    img_url = get_movie_poster(movie_name)

    # print(f"name: {movie_name}")
    # print(f"movie_img: {movie_img}")
    # print(f"address: {address}")

    location = Location(LOCATION_API_KEY)

    date = request.POST.get('date')

    findLoc = location.get_place_location(address)['location']
    lat = findLoc['lat']
    lng = findLoc['lng']


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

    # movie_name = request.GET['movie_name']
    # img_url = request.GET['img_url']

    days = ['일', '월', '화', '수', '목', '금', '토']
    weekday = []

    for i in range(0, 7):
        date = {}
        now = datetime.now() + timedelta(days=i)
        d = now.strftime("%w")
        date['text'] = days[int(d)]
        date['day'] = now.day
        weekday.append(date)


    datas = {
        'date': weekday,
        'movie_name': movie_name,
        'movie_place': address,
        'theater_info': theater_info,
        'img_url': img_url
    }

    return render(request, 'movie/timetable.html', {'datas': datas})