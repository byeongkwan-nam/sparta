import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 타겟 URL을 읽어서 HTML를 받아오고,
target_url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20191212"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(target_url, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

movie_table = soup.select('table.list_ranking')[0]
movie_info = movie_table.select('tbody > tr')

rank = 0
for movie in movie_info:
    temp = movie.select('.title a')
    if (len(temp) == 0):
        continue

    rank += 1
    title = temp[0].text
    point = movie.select('.point')[0].text

    doc = {
        'rank': rank,
        'title': title,
        'point': point
    }

    db.movies.insert_one(doc)
