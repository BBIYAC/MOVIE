import json
import math
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta


class BoxOffice(object):
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'

    def __init__(self, api_key):
        self.api_key = api_key
        #http://www.kobis.or.kr/kobisopenapi/homepg/apikey/ckUser/findApikeyList.do

    def get_movies(self):
        '''
        :return:
        {'boxOfficeResult': {'boxofficeType': '일별 박스오피스', 'showRange': '20210805~20210805', 'dailyBoxOfficeList': [{'rnum': '1', 'rank': '1', 'rankInten': '0', 'rankOldAndNew': 'OLD', 'movieCd': '20204117', 'movieNm': '모가디슈', 'op1-07-28', 'salesAmt': '870897710', 'salesShare': '45.8', 'salesInten': '-104521190', 'salesChange': '-10.7', 'salesAcc': '11701438070', 'audiCnt': '92348', 'audiInten': '-11759', 'audiChange': '-11.3', 'audiAcc': '1231774', 'scrnCnt': '1592', 'showCnt': '6313'}, {'rnum': '2', 'rank': '2', 'rankInten': '0', 'rankOldAndNew': 'OLD', 'movieCd': '20217845', 'movieNm': '더 수어사이드 스쿼드', 'openDt': '2021-08-04', 'salesAmt': '422473310', 'salesShare': '22.2', 'sa: '-177444000', 'salesChange': '-29.6', 'salesAcc': '1043642620', 'audiCnt': '41996', 'audiInten': '-18408', 'audiChange': '-30.5', 'audiAcc': '103915', 'scrnCnt': '1045', 'showCnt': '3322'}, {'rnum': '3', 'rank': '3', 'rankInten': '0', 'rankOldAndNew': 'OLD', 'movieCd': '20218391', 'movieNm': '보스 베이비 2', 'openDt': '2021-07-21', 'salesAmt': '164322500', 'salesShare': '8.6', 'salesInten': '-62752550', 'salesChange': '-27.6', 'salesAcc': '6778418790', 'audi '19148', 'audiInten': '-7240', 'audiChange': '-27.4', 'audiAcc': '758280', 'scrnCnt': '697', 'showCnt': '1430'}, {'rnum': '4', 'rank': '4', 'rankInten': '0', 'rankOldAndNew': 'OLD', 'movieCd': '20191951', 'movieNm': '블랙 위도우', Dt': '2021-07-07', 'salesAmt': '104842660', 'salesShare': '5.5', 'salesInten': '-25686160', 'salesChange': '-19.7', 'salesAcc': '28924478830', 'audiCnt': '10878', 'audiInten': '-2690', 'audiChange': '-19.8', 'audiAcc': '2857306', 'scrnCnt': '496', 'showCnt': '846'}, {'rnum': '5', 'rank': '5', 'rankInten': '0', 'rankOldAndNew': 'NEW', 'movieCd': '20218875', 'movieNm': '극장판 도라에몽: 진구의 신공룡', 'openDt': '2021-08-05', 'salesAmt': '86601410', 'salesShare'esInten': '86601410', 'salesChange': '100', 'salesAcc': '90516410', 'audiCnt': '10498', 'audiInten': '10498', 'audiChange': '100', 'audiAcc': '10933', 'scrnCnt': '491', 'showCnt': '785'}, {'rnum': '6', 'rank': '6', 'rankInten': '-1', 'rankOldAndNew': 'OLD', 'movieCd': '20218349', 'movieNm': '정글 크루즈', 'openDt': '2021-07-28', 'salesAmt': '63408460', 'salesShare': '3.3', 'salesInten': '-22404690', 'salesChange': '-26.1', 'salesAcc': '1949583660', 'audiCnt': ', 'audiInten': '-2438', 'audiChange': '-25.6', 'audiAcc': '212334', 'scrnCnt': '508', 'showCnt': '762'}, {'rnum': '7', 'rank': '7', 'rankInten': '31', 'rankOldAndNew': 'OLD', 'movieCd': '20218834', 'movieNm': '그린 나이트', 'openDt021-08-05', 'salesAmt': '34786410', 'salesShare': '1.8', 'salesInten': '34459710', 'salesChange': '10547.8', 'salesAcc': '36022110', 'audiCnt': '4072', 'audiInten': '4036', 'audiChange': '11211.1', 'audiAcc': '4209', 'scrnCnt': '235', 'showCnt': '305'}, {'rnum': '8', 'rank': '8', 'rankInten': '-2', 'rankOldAndNew': 'OLD', 'movieCd': '20202185', 'movieNm': '방법: 재차의', 'openDt': '2021-07-28', 'salesAmt': '33662080', 'salesShare': '1.8', 'salesInten': '-14640420', 'salesChange': '-30.3', 'salesAcc': '1334623860', 'audiCnt': '3540', 'audiInten': '-1488', 'audiChange': '-29.6', 'audiAcc': '152039', 'scrnCnt': '380', 'showCnt': '508'}, {'rnum': '9', 'rank': '9', 'rankInten': '2', 'rankOldAndNew': 'OLD', 'movieCd': '20218420', 'movieNm': '은혼 더 파이널', 'openDt': '2021-07-22', 'salesAmt': '17197650', 'salesShare': '0.9', 'salesInten': '13066640', 'salesChange': '316.3', 'salesAcc': '292215290', 'audiCnt': '1953', 'aen': '1547', 'audiChange': '381', 'audiAcc': '30644', 'scrnCnt': '53', 'showCnt': '67'}, {'rnum': '10', 'rank': '10', 'rankInten': '-3', 'rankOldAndNew': 'OLD', 'movieCd': '20218815', 'movieNm': '블랙핑크 더 무비', 'openDt': '2021-0'salesAmt': '23503500', 'salesShare': '1.2', 'salesInten': '-35424000', 'salesChange': '-60.1', 'salesAcc': '82431000', 'audiCnt': '1808', 'audiInten': '-2725', 'audiChange': '-60.1', 'audiAcc': '6341', 'scrnCnt': '101', 'showCnt': '148'}]}}
        '''
        target_dt = datetime.now() - timedelta(days=1)
        target_dt_str = target_dt.strftime('%Y%m%d')
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str)
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        '''
        :return:
        [{'rank': '1', 'name': '모가디슈', 'code': '20204117'},
        {'rank': '2', 'name': '더 수어사이드 스쿼드', 'code': '20217845'},
        {'rank': '3', 'name': '보스 베이비 2', 'code': '20218391'},
        {'rank': '4', 'name': '20191951'},
        {'rank': '5', 'name': '정글 크루즈', 'code': '20218349'},
        {'rank': '6', 'name': '방법: 재차의', 'code': '20202185'},
        {'rank': '7', 'name': '블랙핑크 더 무비', 'code': '20218815'},
        {'rank랑종', 'code': '20218364'},
        {'rank': '9', 'name': '이스케이프 룸 2: 노 웨이 아웃', 'code': '20218348'},
        {'rank': '10', 'name': '크루엘라', 'code': '20216362'}]
        '''
        return [
           {
              'rank': entry.get('rank'),
              'name': entry.get('movieNm'),
              'code': entry.get('movieCd')
           }
           for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]


