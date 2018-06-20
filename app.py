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


class Studio(db.Model):

    __tablename__ = "studios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    movies = db.relationship("Movie", backref="studio")


class Movie(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    runtime = db.Column(db.Integer)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.Text)
    studio_id = db.Column(db.Integer,
                          db.ForeignKey('studios.id', ondelete="CASCADE"))


roles = db.Table("roles", db.Column('id', db.Integer, primary_key=True),
                 db.Column('movie_id', db.Integer,
                           db.ForeignKey('movies.id', ondelete="CASCADE")),
                 db.Column('star_id', db.Integer,
                           db.ForeignKey('stars.id', ondelete="CASCADE")))


class Star(db.Model):

    __tablename__ = "stars"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text)
    birth_date = db.Column(db.DateTime, nullable=False)
    movies = db.relationship("Movie", secondary="roles", backref="stars")


db.create_all()


@app.route("/")
def root():
    return "hello rithm 7!"


# Movie routes
@app.route("/studios/<int:studio_id>/movies", methods=["GET"])
def movies_index(studio_id):
    studio = Studio.query.get(studio_id)
    return render_template("movies/index.html", studio=studio)


@app.route("/studios/<int:studio_id>/movies/new", methods=["GET"])
def movies_new(studio_id):
    studio = Studio.query.get(studio_id)
    return render_template(
        "movies/new.html", studio=studio, stars=Star.query.all())


@app.route("/studios/<int:studio_id>/movies", methods=["POST"])
def movies_create(studio_id):
    new_movie = Movie(
        title=request.form['title'],
        runtime=request.form['runtime'],
        release_year=request.form['release_year'],
        rating=request.form['rating'],
        studio_id=studio_id)
    star_ids = request.form.getlist('stars')
    new_movie.stars = Star.query.filter(Star.id.in_(star_ids)).all()
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("movies_index", studio_id=studio_id))


@app.route("/movies/<int:movie_id>", methods=["GET"])
def movies_show(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    return render_template("movies/show.html", movie=found_movie)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def movies_destroy(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    studio = found_movie.studio
    db.session.delete(found_movie)
    db.session.commit()
    return redirect(url_for("movies_index", studio_id=studio.id))


@app.route("/movies/<int:movie_id>/edit", methods=["GET"])
def movies_edit(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    return render_template("movies/edit.html", movie=found_movie)


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def movies_update(movie_id):
    found_movie = Movie.query.get_or_404(movie_id)
    found_movie.title = request.form['title']
    found_movie.release_year = int(request.form['release_year'])
    found_movie.runtime = int(request.form['runtime'])
    found_movie.rating = request.form['rating']
    db.session.add(found_movie)
    db.session.commit()
    return redirect(url_for('movies_show', movie_id=found_movie.id))


# studio routes
@app.route("/studios", methods=["GET"])
def studios_index():
    return render_template("studios/index.html", studios=Studio.query.all())


@app.route("/studios/new", methods=["GET"])
def studios_new():
    return render_template("studios/new.html")


@app.route("/studios", methods=["POST"])
def studios_create():
    new_studio = Studio(
        name=request.form["name"], start_date=request.form["start_date"])
    db.session.add(new_studio)
    db.session.commit()
    return redirect(url_for("studios_index"))
