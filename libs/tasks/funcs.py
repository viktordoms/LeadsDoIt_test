
from libs.tasks.celery import celery
from libs.apis.weather_api.rest import WeatherRestClient, WeatherApiException
from libs.db import TblWeatherHistory, db_session
from libs.conf import CITY_WEATHER

@celery.task
def fill_weather_history():
    try:
        client: WeatherRestClient = WeatherRestClient()
        response: dict = client.get_current_weather()

        city = response.get("location").get("name") or CITY_WEATHER
        temperature = response.get("current").get("temp_c") or 0.0

        db_session.add(
            TblWeatherHistory(
                city=city,
                temperature=temperature
            )
        )
        db_session.commit()

    except KeyError as e:
        print(f"Missing key in Weather API response: {str(e)}")

    except WeatherApiException as e:
        print(f"Any error occurred during sending request to Weather API: {str(e)}")

    finally:
        return None
