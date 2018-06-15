from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus

app = Flask(__name__)
Modus(app)


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


@app.route("/movies/new", methods=["GET"])
def new():
    return render_template("new.html")


@app.route("/movies", methods=["POST"])
def create():
    new_movie = Movie(request.form['title'], request.form['runtime'],
                      request.form['rating'])
    movies.append(new_movie)
    return redirect(url_for("index"))


@app.route("/movies/<int:id>", methods=["GET"])
def show(id):
    found_movie = [movie for movie in movies if movie.id == id][0]
    return render_template("show.html", movie=found_movie)


@app.route("/movies/<int:id>", methods=["DELETE"])
def destroy(id):
    found_movie = [movie for movie in movies if movie.id == id][0]
    movies.remove(found_movie)
    return redirect(url_for("index"))


@app.route("/movies/<int:id>/edit", methods=["GET"])
def edit(id):
    found_movie = [movie for movie in movies if movie.id == id][0]
    return render_template("edit.html", movie=found_movie)


@app.route("/movies/<int:id>", methods=["PATCH"])
def update(id):
    found_movie = [movie for movie in movies if movie.id == id][0]
    found_movie.title = request.form['title']
    found_movie.runtime = request.form['runtime']
    found_movie.rating = request.form['rating']
    return redirect(url_for('show', id=found_movie.id))