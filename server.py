from flask import Flask, render_template
from parse_afisha import get_movies_info

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)
movies_info = get_movies_info()

def grouped(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


@app.route('/')
def films_list():

    return render_template('films_list.html', movies_info=movies_info[:25])

if __name__ == "__main__":
    app.run()
