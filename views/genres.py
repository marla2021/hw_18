from flask_restx import Resource, Namespace

from models import GenreSchema, Genre

genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return GenreSchema(many=True).dump(Genre.query.all()), 200


@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id:int):
        genre = Genre.query.get(id)
        if not genre:
            genres_ns.abort(404)
        return GenreSchema().dump(genre), 200
