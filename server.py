from flask import Flask, render_template, jsonify, request
from parse_afisha import get_movies_info, parse_afisha_list, fetch_afisha_page,\
    get_movie_info, movie_options_list

from werkzeug.contrib.cache import SimpleCache
import os

cache = SimpleCache()
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)
app.secret_key = 'super secret key'

afisha_arr = parse_afisha_list(fetch_afisha_page())


def get_movies_info_cache():
    movies_info = cache.get('movies-info')
    if movies_info is None:
        movies_info = get_movies_info()
        twelve_hours_timeout = 12 * 60 * 60
        cache.set('movies-info', movies_info, timeout=twelve_hours_timeout)
    return movies_info


def create_cache(json_dict):
    movies_info = cache.get('movies-info')
    if movies_info is None:
        movies_info = []
    if json_dict not in movies_info:
        movies_info.append(json_dict)
    twelve_hours_timeout = 12 * 60 * 60
    cache.set('movies-info', movies_info, timeout=twelve_hours_timeout)
    return json_dict


@app.route('/')
def movies_list():
    movies_info = cache.get('movies-info')
    if movies_info is not None:
        if len(movies_info) is 10:
            return render_template('index_template.html', movies_info=movies_info)
    return render_template('create_cache_template.html', movies_info=afisha_arr)


@app.route('/get_movie_info')
def movies_list1():
    movie_id  = int(request.args.get('id'))
    json_arr = get_movie_info(afisha_arr[movie_id]['href'], movie_id, movie_options_list)
    json_arr = create_cache(json_arr)
    return jsonify(json_arr)


@app.route('/api_use')
def api_use():
    return render_template('api_use_template.html')


@app.route('/api/all_movies_info')
def movies_list_json():
    movies_info = get_movies_info_cache()
    return jsonify({'movies_info': movies_info})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
