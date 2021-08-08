# DJANGO MOVIE API BACKEND

- This is for make movie ticketing site
- There is 3 movie company datas


### Start
```
$ git fetch && git checkout develop
```
- Use Windows
```
$ sh run_winodws.sh
```
- Use Mac
```
$ sh run_mac.sh
```

### Page
- Inddex
    - http://127.0.0.1:8000/movie/index/
- Rank
    - http://127.0.0.1:8000/movie/rank/
- findeTheater
    - http://127.0.0.1:8000/movie/find-theater/
    
### PROJECT STRUCTURE
```
MOVIE_BACKEND/
└───api/ 
│    │───migragtions/
│    │   __init__.py
│    │   admin.py
│    │   apps.py
│    │   models.py
│    │   test.py
│    │   urls.py
│    │   views.py
└───config/
│      │   __init__.py
│      │   asgi.py
│      │   settings.py
│      │   urls.py
│      │   wsgi.py
└───core/
│     │───crawl/
│     │     │   __init__.py
│     │     │   CGV_crawl.py
│     │     │   LOTTE_crawl.py
│     │     │   make_cgv_theater_list.py
│     │     │   MEGA_crawl.py
│     │───theater/
│     │      │───data/
│     │      │     │     json data in here 
│     │      │   __init__.py
│     │      │   lottecinema.py
│     │      │   cgv.py
│     │   __init__.py
│     │   boxoffice.py
│     │   location.py
│───templates/
│     │   timetable.html
│     │   index.html
│     │   nearTheater.html
│     │   rank.html
│   .gitignore
│   db.sqlite3
│   manage.py
│   README.md
│   requirements.txt
│   run_mac.sh
│   run_window.sh
│   secrets.json 
```

