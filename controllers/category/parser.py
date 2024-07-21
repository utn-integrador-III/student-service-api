from flask_restful import reqparse


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "category_name", type=str, required=True, help="This field cannot be blank"
    )
    return parser


def query_parser_put():
    parser = reqparse.RequestParser()
    parser.add_argument("_id", type=str, required=True, help="ID is required")
    parser.add_argument(
        "category_name", type=str, required=True, help="This field cannot be blank"
    )
    return parser
