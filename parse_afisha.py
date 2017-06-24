from flask import safe_join
from bs4 import BeautifulSoup
import requests
import json


movie_options_list = ['text', 'url', 'name', 'aggregateRating', 'description',
                      'image', 'alternativeHeadline', 'genre']


def fetch_afisha_page():
    request = requests.get('http://www.afisha.ru/krasnoyarsk/schedule_cinema/')
    return request.content


def parse_afisha_list(raw_html):
    soup_data = BeautifulSoup(raw_html, 'html.parser')
    movies_list = soup_data.find_all(class_="object")
    movies_info_list = [{'href': movie.find(class_="m-disp-table").a['href'],
                         'id': num} for num, movie in enumerate(movies_list)]
    return movies_info_list[:10]


def get_movie_info_dict(afisha_link):
    response_content = requests.get(afisha_link).content
    soup_data = BeautifulSoup(response_content, 'html.parser')
    response_json = soup_data.find(attrs={"type": "application/ld+json"}).text
    movie_info_dict = json.loads(response_json)
    return movie_info_dict


def get_movie_info(afisha_link, movie_id, keys_set):
    movie_info_dict = get_movie_info_dict(afisha_link)
    movie_info_dict.setdefault('text')
    movie_info_dict.setdefault('aggregateRating', {'ratingValue': '0', 'ratingCount': '0'})
    movie_info_dict.setdefault('image', safe_join('static', 'no_image.jpg'))
    filtered_movie_dict = {key: movie_info_dict[key] for key in keys_set}
    link_without_scheme = filtered_movie_dict['image'][6:]
    filtered_movie_dict['image'] = link_without_scheme
    filtered_movie_dict['id'] = movie_id
    return filtered_movie_dict


def get_movies_info():
    movies_info_list = parse_afisha_list(fetch_afisha_page())
    info_from_movie_page_list = [get_movie_info(afisha_link['href'], movie_id, movie_options_list)
                                 for movie_id, afisha_link in enumerate(movies_info_list[:10])]
    return info_from_movie_page_list
