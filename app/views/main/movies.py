from flask_restx import Namespace, Resource

from app.container import movie_service
from app.setup.api.models import movie_schema
from app.setup.api.parsers import status_and_page_parser

api = Namespace('movies', description="Фильмы")


@api.route('/')
class MoviesView(Resource):
    @api.expect(status_and_page_parser)
    @api.marshal_with(movie_schema, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        return movie_service.get_all(**status_and_page_parser.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie_schema, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(movie_id)
