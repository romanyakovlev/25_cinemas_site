from flask import Flask, render_template
from parse_afisha import get_movies_info

app = Flask(__name__)
movies_info = get_movies_info()

@app.route('/')
def films_list():

    return render_template('films_list.html', movies_info=movies_info)

if __name__ == "__main__":
    app.run()
