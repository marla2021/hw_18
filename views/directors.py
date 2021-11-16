from flask_restx import Resource, Namespace

from models import DirectorSchema, Director

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return DirectorSchema(many=True).dump(Director.query.all()), 200


@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id:int):
        genre = Director.query.get(id)
        if not genre:
            directors_ns.abort(404)
        return DirectorSchema().dump(genre), 200