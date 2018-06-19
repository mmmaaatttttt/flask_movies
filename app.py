from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/movies_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

modus = Modus(app)
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)


class Movie(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    runtime = db.Column(db.Integer)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.Text)


db.create_all()


@app.route("/")
def root():
    return "hello rithm 7!"


@app.route("/movies", methods=["GET"])
def index():
    return render_template("index.html", movies=Movie.query.all())


@app.route("/movies/new", methods=["GET"])
def new():
    return render_template("new.html")


@app.route("/movies", methods=["POST"])
def create():
    new_movie = Movie(
        title=request.form['title'],
        runtime=request.form['runtime'],
        release_year=request.form['release_year'],
        rating=request.form['rating'])
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/movies/<int:movie_id>", methods=["GET"])
def show(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    return render_template("show.html", movie=found_movie)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def destroy(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    db.session.delete(found_movie)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/movies/<int:movie_id>/edit", methods=["GET"])
def edit(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    return render_template("edit.html", movie=found_movie)


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def update(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    found_movie.title = request.form['title']
    found_movie.release_year = int(request.form['release_year'])
    found_movie.runtime = int(request.form['runtime'])
    found_movie.rating = request.form['rating']
    db.session.add(found_movie)
    db.session.commit()
    return redirect(url_for('show', movie_id=found_movie.id))