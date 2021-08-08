import requests
from bs4 import BeautifulSoup


def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    for movie_no in movie_no_list:
        movies = [item for item in response if item["MovieCode"] == movie_no]
        title = movies[0]["MovieNameKR"]
        timetable = get_time_table(movies)
        print(title, timetable, "\n")

        
def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["MovieCode"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


def get_time_table(movies):
    tuples = []
    for movie in movies:
        time = movie["StartTime"]
        seats = movie["BookingSeatCount"]
        tuple = (time, seats)
        tuples.append(tuple)
    return tuples


url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
dic = {"MethodName": "GetPlaySequence",
       "channelType": "MA",
       "osType": "",
       "osVersion": "",
       "playDate": "2021-08-08",
       "cinemaID": "1|17|1002",
       "representationMovieCode": ""}
parameters = {"paramList": str(dic)}
response = requests.post(url, data = parameters).json()
movies_response = response['PlaySeqs']['Items']
split_movies_by_no(movies_response)
