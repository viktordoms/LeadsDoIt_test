from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from handler_groups.weather.schema import WeatherSearchResultSchema, WeatherSearchSchema
from libs.errors import error_invalid_data
from libs.weather import WeatherBaseException
import libs.weather.funcs as funcs
from libs.validators import validate_api_key

bp_weather = Blueprint("weather", __name__, url_prefix='/weather')


@bp_weather.route('/history', strict_slashes=False, methods=["GET"])
@validate_api_key()
@use_kwargs(WeatherSearchSchema, location="query")
@marshal_with(WeatherSearchResultSchema)
def get_weather_history(**params):
    try:
        return {
            "success": True,
            "results": funcs.get_weather_history(**params)
        }
    except WeatherBaseException as e:
        return error_invalid_data(str(e))