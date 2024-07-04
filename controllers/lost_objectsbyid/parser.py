from flask_restful import reqparse


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "id", type=int, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument("description", type=str, required=False)
    parser.add_argument("status", type=str, required=False)
    parser.add_argument("creation_date", type=str, required=False)
    parser.add_argument("attachment_path", type=str, required=False)
    parser.add_argument("claim_date", type=str, required=False)
    parser.add_argument("claimer", type=str, required=False)
    parser.add_argument("safekeeper", type=str, required=False)
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be blank"
    )
    return parser
