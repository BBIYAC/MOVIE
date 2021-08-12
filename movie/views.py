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
        search_url = base_url + quote(movie_name + '영화')
        html = urlopen(search_url)
        soup = BeautifulSoup(html,'html.parser')
        img_url = soup.select_one(
            '#main_pack > div.sc_new._au_movie_content_wrap > div.cm_content_wrap > div > div.cm_info_box > div.detail_info img')['src']
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

    # print(datas)

    return render(request, 'movie/timetable.html', {'datas': datas})


def get_movie_poster(movie_name):
    base_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    search_url = base_url + quote(movie_name + '영화')
    html = urlopen(search_url)
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.select_one(
        '#main_pack > div.sc_new._au_movie_content_wrap > div.cm_content_wrap > div > div.cm_info_box > div.detail_info img')['src']
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

    findLoc = location.get_place_location(address)['location']
    lat = findLoc['lat']
    lng = findLoc['lng']

    days = ['일', '월', '화', '수', '목', '금', '토']
    weekday = []

    for i in range(0, 7):
        date = {}
        now = datetime.now() + timedelta(days=i)
        d = now.strftime("%w")
        month_day = now.strftime("%m%d")
        day = now.strftime("%d")
        date['text'] = days[int(d)]
        date['month_day'] = month_day
        date['day'] = day
        weekday.append(date)

    datas = {
        'date': weekday,
        'movie_name': movie_name,
        'movie_place': address,
        'img_url': img_url,
        'lat': lat,
        'lng': lng
    }

    return render(request, 'movie/timetable.html', {'datas': datas})
