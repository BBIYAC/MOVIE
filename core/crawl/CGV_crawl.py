import json
import requests
from bs4 import BeautifulSoup


def get_timetable(movie):
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


url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx"
data = {"areacode": "01",
       "theatercode": "0010",
       "date": "20210808"}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

html = response.text
soup = BeautifulSoup(html,'html.parser')

movies = soup.select('body > div > div.sect-showtimes > ul > li')

for movie in movies:
    title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
    timetable = get_timetable(movie)
    # print("--")
    print(title, timetable, '\n')




