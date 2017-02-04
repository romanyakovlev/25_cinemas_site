from flask import Flask, render_template, jsonify, redirect, request
from parse_afisha import get_movies_info
from werkzeug.contrib.cache import SimpleCache
import os

cache = SimpleCache()
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)


def get_movies_info_cache(get_cache=False):
    movies_info = cache.get('movies-info')
    if movies_info is None:
        movies_info = get_movies_info()
        twelve_hours_timeout = 12 * 60 * 60
        cache.set('movies-info', movies_info, timeout=twelve_hours_timeout)
    if get_cache is False:
        return jsonify({"response": "ok"})
    else:
        return movies_info


@app.route('/')
def movies_list():
    movies_info = cache.get('movies-info')
    if movies_info is None:
        return redirect('/make_cache')
    return render_template('index_template.html', movies_info=movies_info)


@app.route('/make_cache', methods=['GET', 'POST'])
def make_cache():
    if request.method == "GET":
        return render_template('make_cache_template.html')
    if request.method == "POST":
        return get_movies_info_cache()


@app.route('/api_use')
def api_use():
    return render_template('api_use_template.html')


@app.route('/api/all_movies_info')
def movies_list_json():
    movies_info = get_movies_info_cache(get_cache=True)
    return jsonify({'movies_info': movies_info})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
