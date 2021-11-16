from flask_restx import Resource, Namespace
from flask import request
from models import MovieSchema, Movie
from setup_db import db

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        return MovieSchema(many=True).dump(Movie.query.all()), 200


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id:int):
        genre = Movie.query.get(id)
        if not genre:
            movies_ns.abort(404)
        return MovieSchema().dump(genre), 200

    def delete(self,id:int):
        movie = Movie.query.get(id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return '', 204
    def put(self, id:int):
        mov = Movie.query.get(id)
        req_json = request.json
        mov.name = req_json.get("name")
        db.session.add(mov)
        db.session.commit()
        return "", 204

@movies_ns.route('/')
class Movie_filtrView(Resource):
    def get(self):
        dir_id = request.args.get("director_id")
        gen_id = request.args.get("genre_id")
        year = request.args.get("year")
        if dir_id is not None:
            mov = Movie.query.filter(Movie.director_id == dir_id)
        if gen_id is not None:
            mov = Movie.query.filter(Movie.genre_id == gen_id)
        if gen_id is not None:
            mov = Movie.query.filter(Movie.year == year)
        movies = mov.all()
        return MovieSchema().dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return MovieSchema().dump(new_movie), 201