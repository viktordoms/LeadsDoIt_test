1. Configs:
 - rename `env.local` -> `.env`
 - `WEATHER_API_KEY`. You can use an existing one or get a new one here `https://www.weatherapi.com/my/`
 - `CITY_WEATHER` -> the city you want to get weather
 - `CITY_WEATHER_SCHEDULE_HOUR` -> how often to update weather data

2. Start app
  - `docker compose up --build -d`
  - `docker exec -it api python3 migrations/migrate.py 7156722f` - migration for creating basic table