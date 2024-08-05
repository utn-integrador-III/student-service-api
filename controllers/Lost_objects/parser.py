from flask_restful import reqparse
from werkzeug.exceptions import BadRequest
import re

class LostObjectParser:
    @staticmethod
    def parse_put_request():
        parser = reqparse.RequestParser()
        
        # Define and add arguments
        parser.add_argument('_id', type=str, required=True, help="ID of the lost object is required", location=['json', 'values'])
        parser.add_argument('name', type=str, required=False, location=['json', 'values'])
        parser.add_argument('description', type=str, required=False, location=['json', 'values'])
        parser.add_argument('status', type=str, required=False, location=['json', 'values'])
        parser.add_argument('attachment_path', type=str, required=False, location=['json', 'values'])
        parser.add_argument('claim_date', type=str, required=False, location=['json', 'values'])
        parser.add_argument('claimer', type=str, required=False, location=['json', 'values'])
        parser.add_argument('safekeeper', type=list, required=False, location='json')
        parser.add_argument('user_email', type=str, required=False, location=['json', 'values'])
        parser.add_argument('category', type=list, required=False, location='json')

        args = parser.parse_args(strict=True)

        # Validate user_email
        if args.get('user_email'):
            if not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr|adm\.utn\.ac\.cr)$", args['user_email']):
                raise BadRequest('Invalid email domain for user_email')

        # Validate safekeeper
        if args.get('safekeeper'):
            if not isinstance(args['safekeeper'], list):
                raise BadRequest('Safekeeper should be a list')
            for sk in args['safekeeper']:
                if not isinstance(sk, dict) or 'user_email' not in sk:
                    raise BadRequest(f'Invalid safekeeper format: {sk}')
                if not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr|adm\.utn\.ac\.cr)$", sk['user_email']):
                    raise BadRequest(f'Invalid safekeeper email domain: {sk.get("user_email", "")}')

        # Validate category
        if args.get('category'):
            if not isinstance(args['category'], list):
                raise BadRequest('Category should be a list')
            if not all(isinstance(cat, str) for cat in args['category']):
                raise BadRequest('All categories should be strings')

        return args
