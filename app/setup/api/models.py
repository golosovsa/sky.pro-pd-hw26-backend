from flask_restx import fields, Model

from app.setup.api import api

genre_schema: Model = api.model("Жанр", {
    "id": fields.Integer(required=True, example=1),
    "name": fields.String(required=True, max_length=100, example="Комедия"),
})

director_schema: Model = api.model("Продюсер", {
    "id": fields.Integer(required=True, example=1),
    "name": fields.String(required=True, max_length=100, example="Михалков Никита Сергеевич"),
})

movie_schema: Model = api.model("Фильм", {
    "id": fields.Integer(required=True, example=1),
    "title": fields.String(required=True, example="Утомленные солнцем"),
    "description": fields.String(example="Российско-французская картина 1994 года - лауреат премии 'Оскар' за "
                                         "'Лучший фильм на иностранном языке', также она получила Гран-при 47-го "
                                         "Каннского фестиваля. По российскому телевидению фильм был впервые показан "
                                         "21 октября 1995 года - в 50-летний юбилей Никиты Михалкова. Действие фильма "
                                         "разворачивается в 1936 году, незадолго до начала сталинских репрессий. "
                                         "В картине снимались сам Михалков, Игнеборга Дапкунайте, Олег Меньшиков, "
                                         "Надя Михалкова."),
    "trailer": fields.String(example="https://www.youtube.com/watch?v=6JsFEMUtNM4"),
    "year": fields.Integer(example=1994),
    "rating": fields.Float(example=7.7),
    "genre_id": fields.Integer(example=1),
    "director_id": fields.Integer(example=1),
    "director": fields.Nested(director_schema),
    "genre": fields.Nested(genre_schema),
})

favourite_movie_schema: Model = api.model("Любимые фильмы", {
    "user_id": fields.Integer(required=True, example=1),
    "movie_id": fields.Integer(required=True, example=1),
})

user_schema: Model = api.model("Информация о пользователе", {
    "id": fields.Integer(required=True, example=1),
    "email": fields.String(required=True, example="mail@mail.ru"),
    "name": fields.String(required=True, example="Tom"),
    "surname": fields.String(required=True, example="Ellison"),
    "favourite_genre": fields.Integer(required=True, example=1),
})
