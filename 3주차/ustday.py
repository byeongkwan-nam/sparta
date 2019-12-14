#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS
import pprint
import pandas
import re
import json

def get_news(url):
    resp = requests.get(url)
    bs = BS(resp.text, "lxml")

    ps = bs.select("div.asset-double-wide.double-wide.p402_premium > p.p-text")
    news = [p.text for p in ps]
    news = " ".join(news)
    
    return news.lower()

def get_freq(news):
    freq = {}

    # 단어들 중 4글자 이상 15단어 이하 선별
    match_words = re.findall(r'\b[a-z]{4,15}\b', news)

    # 단어별 빈도수 계산
    for word in match_words:
        cnt = freq.get(word, 0)
        freq[word] = cnt + 1
    
    return freq

def translate(word):
    url = "https://ac.dict.naver.com/enendict/ac?q={}&q_enc=utf-8&st=11001&r_enc=utf-8".format(word)
    resp = requests.get(url)
    j = json.loads(resp.text)
    try:
        return (j["items"][0][0][1][0])
    except:
        return None

def get_quiz():
    url = "https://www.usatoday.com/"
    resp = requests.get(url)
    bs = BS(resp.text, "lxml")
    links = bs.select("ul.hfwmm-list.hfwmm-4uphp-list.hfwmm-light-list > li > a")

    
    # 1. 기사 내용을 긁어온다.
    news = ""
    for link in links:
        news += get_news(url + link["href"])
    
    # 2. 각 단어의 빈도수를 세고 내림차순 정렬
    freq = get_freq(news)
    sorted_keys = sorted(freq, key=freq.get, reverse=True)
    quiz = []

    # 3. 단어 번역
    for sorted_key in sorted_keys:
        if (freq[sorted_key] < 3):
            break
        kor = translate(sorted_key)
        quiz.append([sorted_key, kor, freq[sorted_key]])

    return quiz


quiz = get_quiz()

columns = ["영단어", "한글", "횟수"]

df = pandas.DataFrame(quiz, columns=columns)
df.to_excel("en_quiz.xlsx",
            sheet_name="US TODAY",
            header=True,
            startrow=0)
