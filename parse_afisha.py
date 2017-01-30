from bs4 import BeautifulSoup
import requests

def fetch_afisha_page():
    request = requests.get('http://www.afisha.ru/krasnoyarsk/schedule_cinema/')
    return request.content


def parse_afisha_list(raw_html):
    soup_data =  BeautifulSoup(raw_html, 'html.parser')
    movies_list = soup_data.find_all(class_="object")
    movies_info = [[movie.find(class_="m-disp-table").a.text, movie.find(class_="m-disp-table").a['href'][2:],
                 len(movie.find_all(class_="b-td-item"))] for movie in movies_list]
    return movies_info


def get_movies_info():
    movies_info = parse_afisha_list(fetch_afisha_page())
    movies_img_links = []
    for _, (name, link, cinema_quantity) in enumerate(movies_info):
        request = requests.get('http://'+link+'photo/').content
        soup_data = BeautifulSoup(request,'html.parser')
        try:
            movies_info[_].append(soup_data.find(class_='current-photo').img['src'])
        except:
            movies_info[_].append(None)
    return movies_info
