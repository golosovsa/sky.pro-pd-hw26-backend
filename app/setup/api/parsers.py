from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(
    name="page",
    type=int,
    location="args",
    required=False,
    help="Номер страницы"
)

status_and_page_parser: RequestParser = page_parser.copy()
status_and_page_parser.add_argument(
    name="status",
    choices=("new", ),
    location="args",
    required=False,
    help="Сортировать по: "
)
