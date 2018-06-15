from flask import Flask, render_template

app = Flask(__name__)


class Movie:
    count = 1

    def __init__(self, title, runtime, rating):
        self.title = title
        self.runtime = runtime
        self.rating = rating
        self.id = Movie.count
        Movie.count += 1


avengers = Movie("Avengers: Infinity War", 156, "PG-13")
ocean = Movie("Ocean's 8", 110, "PG-13")
solo = Movie("Solo: A Star Wars Story", 135, "PG-13")
movies = [avengers, ocean, solo]


@app.route("/")
def root():
    return "hello rithm 7!"


@app.route("/movies", methods=["GET"])
def index():
    return render_template("index.html", movies=movies)