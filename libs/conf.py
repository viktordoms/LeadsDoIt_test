
import os
from dotenv import load_dotenv
load_dotenv()

DB = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_DATABASE"),
}

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY_WEATHER = os.getenv("CITY_WEATHER")
CITY_WEATHER_SCHEDULE_HOUR = os.getenv("CITY_WEATHER_SCHEDULE_HOUR")