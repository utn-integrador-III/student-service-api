from flask_restful import reqparse
import re

class LostObjectParser:
    @staticmethod
    def parse_put_request():
        parser = reqparse.RequestParser()

        parser.add_argument('_id', type=str, required=True, help="ID of the lost object is required")
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('status', type=str, required=False)
        parser.add_argument('attachment_path', type=str, required=False)
        parser.add_argument('claim_date', type=str, required=False)
        parser.add_argument('claimer', type=str, required=False)
        parser.add_argument('safekeeper', type=list, location='json', required=False)
        parser.add_argument('user_email', type=str, required=False)

        args = parser.parse_args()

        # Validate user_email if provided
        if args['user_email'] and not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr)$", args['user_email']):
            parser.error('Invalid email domain for user_email')

        # Validate safekeeper if provided
        if args['safekeeper']:
            for sk in args['safekeeper']:
                if not isinstance(sk, dict) or 'user_email' not in sk or not re.match(r"^[\w\.-]+@utn\.ac\.cr$", sk['user_email']):
                    parser.error(f'Invalid safekeeper email: {sk.get("user_email", "")}')

        return args
