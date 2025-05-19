import json
import typing as t
import requests

from libs.conf import WEATHER_API_KEY, CITY_WEATHER

class WeatherApiException(Exception):
    pass


class WeatherRestClient:

    """
    Weather REST API Client
    https://www.weatherapi.com/docs/
    """

    def __init__(self):
        self.api_url = "http://api.weatherapi.com"
        self.api_key = WEATHER_API_KEY
        self.city = CITY_WEATHER


    def _send_request(
        self,
        method:str,
        endpoint: str,
        params: t.Optional[dict] = None,
        data: t.Optional[dict] = None,
        headers: t.Optional[dict] = None,
        **kwargs
    ) -> dict:
        """
        Send request to Weather API.
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint (without base URL)
            params (t.Optional[t.Dict]): request params
            data (t.Optional[t.Dict]): request data
            headers (t.Optional[t.Dict]): request headers
            **kwargs: additional arguments
        Returns:
            dict: response data
        """

        headers: dict = headers or {}
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        url = f"{self.api_url}{endpoint}"

        response = requests.request(
            method,
            url,
            params=params,
            data=json.dumps(data),
            headers=headers,
            **kwargs,
        )
        if response.status_code not in [200, 201]:
            data = response.json()
            message = data.get("error").get("message")
            raise WeatherApiException(message or data)

        return response.json()

    def get_current_weather(self) -> dict:

        params = {
            "key": self.api_key,
            "q": self.city,
        }
        return self._send_request(
            method="get",
            endpoint="/v1/current.json",
            params=params,
        )
