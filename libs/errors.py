import json
from flask import Response
import typing as t

def throw_validation_error(
        message: str = "Invalid input", code: int = 400, errors: t.Optional[t.List] = None
    ) -> Response:
    """Returns valid Flask Response in case of input error"""

    response = {
        'success': False,
        'message': message,
        'code': code,
        'errors': errors,
    }
    return Response(
        response=json.dumps(response),
        status=code,
        mimetype='application/json',
        headers={"Access-Control-Allow-Origin": "*"}
    )


def error_invalid_data(message, custom_code=None, code=400, errors=None):
    response = {
        'success': 0,
        'message': message
    }
    if custom_code is not None:
        response['code'] = custom_code
    if errors and type(errors) is list:
        response['errors'] = errors
    return Response(response=json.dumps(response), status=code, mimetype='application/json', headers={"Access-Control-Allow-Origin": "*"})