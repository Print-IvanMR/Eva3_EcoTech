import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ecotech_es3")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

WEATHER_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
CURRENCY_API_URL = "https://api.frankfurter.dev/v2/rate"
