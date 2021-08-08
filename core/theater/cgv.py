import os
import json
import math
import requests
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode
from pathlib import Path
from bs4 import BeautifulSoup


def get_timetable(movie):
    # dict = {}
    # timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    # for timetable in timetables:
    #     print(timetable)
    #     if timetable.select_one('a > em'):
    #         time = timetable.select_one('a > em')
    #         time = time.get_text()
    #     else:
    #         pass
    #     seat = timetable.select_one('a > span').get_text()
    #     seat = seat[4:-1]
    #     dict['StartTime'] = time
    #     dict['RemainingSeat'] = seat
    #
    # return dict
    tuples = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    for timetable in timetables:
        # print(timetable)
        time = timetable.select_one('a > em')
        if time is None:
            continue
        else:
            time = time.get_text()
        seat = timetable.select_one('a > span').get_text()
        tuple = (time, seat)
        tuples.append(tuple)
    return tuples

class CGV():
    base_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx'

    def get_region_list(self, areaName):
        '''
        To get Region list

        ---
        :parameter:
        areaName='서울'
        :return:
        01
        '''

        BASE_DIR = Path(__file__).resolve().parent.parent
        areaCodes_file = os.path.join(BASE_DIR, 'theater/data/AreaCodes.json')

        with open(areaCodes_file) as json_file:
            data = json.load(json_file)

        data = data.get('areaCode')

        if areaName:
            areaCode = data.get(areaName)
        else:
            areaCode = '999'
        return areaCode

    def get_theater_list(self):
        '''
        To get theater list

        ---
        :parameter:
        areaCode = 01
        :return:

        '''

        BASE_DIR = Path(__file__).resolve().parent.parent
        areaCodes_file = os.path.join(BASE_DIR, 'theater/data/TheaterCodesRegion.json')

        with open(areaCodes_file) as json_file:
            data = json.load(json_file)

        theaterLists = data
        return theaterLists

    def distance(self, x1, x2, y1, y2):
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

    def filter_nearest_theater(self, theater_list, pos_latitude, pos_longitude, n=3):
        '''
        To filter by location to get nearest theater count 3
        :param theater_list:
        :param pos_latitude:
        :param pos_longitude:
        :param n:
        :return:
        '''
        distance_to_theater = []
        for theater in theater_list:
            distance = self.distance(pos_latitude, theater.get('Latitude'), pos_longitude, theater.get('Longitude'))
            distance_to_theater.append((distance, theater))

        return [theater for distance, theater in sorted(distance_to_theater, key=lambda x: x[0])[:n]]


    def get_movie_list(self, areacode, theatercode, date):
        '''
        To get moive list by theater_id
        :param theater_id:
        :return:
        '''
        url = self.base_url
        if date:
            date = datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%Y%m%d')
        else:
            target_dt = datetime.now()
            date = target_dt.strftime('%Y%m%d')
        url = url + str("?") + str("areacode") + "=" + areacode + str("&theatercode") + "=" + theatercode + str("&date") + "=" + date
        # print(url)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, headers=headers)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        movies = soup.select('body > div > div.sect-showtimes > ul > li')

        movie_id_to_info={}
        count = 0
        for movie in movies:
            title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
            timetable = get_timetable(movie)
            # print(title, timetable, '\n')
            movie_id_to_info[count]= {'Name': title, 'Schedules': [timetable]}
            count += 1
        # print(movie_id_to_info)
        return movie_id_to_info

# cgv = CGV()
# areacode = '01'
# theatercode = '0010'
# date = '2021-08-08'
# # print(cgv.get_movie_list(theatercode, date))
# print(cgv.get_movie_list(areacode, theatercode, date))