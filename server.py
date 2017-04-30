from flask import Flask, render_template, jsonify
from parse_afisha import get_movies_info
from werkzeug.contrib.cache import SimpleCache
import os

cache = SimpleCache()
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)
app.secret_key = 'super secret key'

def get_movies_info_cache():
    movies_info = cache.get('movies-info')
    if movies_info is None:
        movies_info = get_movies_info()
        twelve_hours_timeout = 12 * 60 * 60
        cache.set('movies-info', movies_info, timeout=twelve_hours_timeout)
    return movies_info


@app.route('/')
def movies_list():
    movies_info = get_movies_info_cache()
    return render_template('index_template.html', movies_info=movies_info)


@app.route('/api_use')
def api_use():
    return render_template('api_use_template.html')


@app.route('/api/all_movies_info')
def movies_list_json():
    movies_info = get_movies_info_cache()
    return jsonify({'movies_info': movies_info})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
