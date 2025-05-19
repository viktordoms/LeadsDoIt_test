
import typing as t
from flask import request, jsonify
from functools import wraps

def validate_api_key(
    ignore_auth: bool = False,
) -> t.Callable[[t.Callable], t.Callable]:
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):

            x_token = request.headers.get("x-token")
            if x_token is None:
                if ignore_auth:
                    return fn(*args, **kwargs)

                response = jsonify(
                    dict(
                        success=False,
                        message="X-token is missing!"
                    )
                )
                response.status_code = 401
                return response
            try:
                assert len(x_token) == 32, "Invalid x-token"
            except AssertionError:
                response = jsonify(
                    dict(
                        success=False,
                        message="X-token invalid! Auth failed."
                    )
                )
                response.status_code = 401
                return response

            return fn(*args, **kwargs)
        return wrapped
    return wrapper