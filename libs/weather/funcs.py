
import typing as t
from sqlalchemy import and_

from libs.db import TblWeatherHistory
from libs.conf import CITY_WEATHER

def get_weather_history(
    time_from: str,
    time_to: str,
    **kwargs
) -> t.List[TblWeatherHistory]:
    """
    Search weather history from given time range.
    Args:
        time_from (str): start stamp of time range in format YYYY-MM-DD
        time_to (str): end stamp of time range in format YYYY-MM-DD
    Returns:
        t.List[TblWeatherHistory]: weather history list
    """

    results = TblWeatherHistory.query.filter(
        and_(
            TblWeatherHistory.created_at.between(time_from, time_to),
            TblWeatherHistory.city == CITY_WEATHER
        )
    ).order_by(
        TblWeatherHistory.created_at.desc()
    ).all()

    return results