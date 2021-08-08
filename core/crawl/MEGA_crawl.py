import requests
from bs4 import BeautifulSoup


def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    for movie_no in movie_no_list:
        movies = [item for item in response if item["movieNo"] == movie_no]
        title = movies[0]["movieNm"]
        timetable = get_time_table(movies)
        print(title, timetable, "\n")


def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


def get_time_table(movies):
    tuples = []
    for movie in movies:
        time = movie["playStartTime"]
        seats = movie["restSeatCnt"]
        tuple = (time, seats)
        tuples.append(tuple)
    return tuples


url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
parameters = {"masterType":"brch",
              "detailType":"area",
              "brchNo":"1372",
              "firstAt":"N",
              "brchNo1":"1372",
              "crtDe":"20200315",
              "playDe":"20200315"}
response = requests.post(url, data = parameters).json()

movie_response = response['megaMap']['movieFormList']
split_movies_by_no(movie_response)



