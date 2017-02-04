from flask import safe_join
from bs4 import BeautifulSoup
import requests
import json
import re


def fetch_afisha_page():
    request = requests.get('http://www.afisha.ru/krasnoyarsk/schedule_cinema/')
    return request.content


def parse_afisha_list(raw_html):
    soup_data = BeautifulSoup(raw_html, 'html.parser')
    movies_list = soup_data.find_all(class_="object")
    movies_info_list = [movie.find(class_="m-disp-table").a['href'][2:]
                        for movie in movies_list]
    return movies_info_list


def get_movie_info_dict(afisha_link):
    response_content = requests.get('http://{}'.format(afisha_link)).content
    soup_data = BeautifulSoup(response_content, 'html.parser')
    response_json = soup_data.find(attrs={"type": "application/ld+json"}).text
    movie_info_dict = json.loads(response_json)
    return movie_info_dict


def check_for_empty_value(movie_info_dict):
    if 'text' not in movie_info_dict.keys():
        movie_info_dict['text'] = 'Нет описания'
    if 'aggregateRating' not in movie_info_dict.keys():
        movie_info_dict['aggregateRating'] = {'ratingValue': '0',
                                              'ratingCount': '0'}
    if 'image' not in movie_info_dict.keys():
        movie_info_dict['image'] = safe_join('static', 'no_image.jpg')
    return movie_info_dict


def get_movie_info(afisha_link, movie_id, keys_set):
    movie_info_dict = get_movie_info_dict(afisha_link)
    movie_info_dict = check_for_empty_value(movie_info_dict)
    filtered_movie_dict = {key: movie_info_dict[key] for key in keys_set}
    filtered_movie_dict['id'] = movie_id
    re.sub(r'$http://', r'$https://', filtered_movie_dict['image'])
    return filtered_movie_dict


def get_movies_info():
    keys_set = {'text', 'url', 'name', 'aggregateRating', 'description',
                'image', 'alternativeHeadline', 'genre'}
    movies_info_list = parse_afisha_list(fetch_afisha_page())
    info_from_movie_page_list = []
    for movie_id, afisha_link in enumerate(movies_info_list):
        movie_info_dict = get_movie_info(afisha_link, movie_id, keys_set)
        info_from_movie_page_list.append(movie_info_dict)
    return info_from_movie_page_list
