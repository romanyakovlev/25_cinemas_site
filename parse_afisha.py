from flask import safe_join
from bs4 import BeautifulSoup
import requests
import json

def fetch_afisha_page():
    request = requests.get('http://www.afisha.ru/krasnoyarsk/schedule_cinema/')
    return request.content


def parse_afisha_list(raw_html):
    soup_data =  BeautifulSoup(raw_html, 'html.parser')
    movies_list = soup_data.find_all(class_="object")
    movies_info = [[movie.find(class_="m-disp-table").a['href'][2:],
                 len(movie.find_all(class_="b-td-item"))] for movie in movies_list]
    return movies_info


def get_movies_info():
    movies_info = parse_afisha_list(fetch_afisha_page())
    for _, (link, cinema_quantity) in enumerate(movies_info):
        content = requests.get('http://'+link).content
        soup_data =  BeautifulSoup(content, 'html.parser')
        cinema_json = soup_data.find_all(attrs={"type":"application/ld+json"})
        json_1_text = soup_data.find(attrs={"type":"application/ld+json"}).text
        json_1 = json.loads(json_1_text)
        try:
            json_1['aggregateRating']['ratingValue']
        except:
            json_1['aggregateRating'] = {'ratingValue': '0', 'ratingCount': '0'}
        try:
            json_1['image']
        except:
            json_1['image'] = safe_join('static', 'no_image.jpg')
        movies_info[_].append(json_1)
        movies_info[_].append(_)
    return movies_info

if __name__ == '__main__':
    content = requests.get('http://www.afisha.ru/movie/228065/').content
    soup_data =  BeautifulSoup(content, 'html.parser')
    cinema_json = soup_data.find_all(attrs={"type":"application/ld+json"})
    json_1_text = soup_data.find(attrs={"type":"application/ld+json"}).text
    json_1 = json.loads(json_1_text)

    for y, x in enumerate(get_movies_info()):
        print(y, x[-1]['aggregateRating']['ratingValue'], x[-1]['name'])
