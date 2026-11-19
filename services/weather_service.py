import requests
from config.settings import WEATHER_GEOCODING_URL, WEATHER_FORECAST_URL, REQUEST_TIMEOUT

class WeatherService:
    def __init__(self):
        self.session = requests.Session()

    def get_weather(self, city):
        city = city.strip()
        if not city:
            raise ValueError("escriba el nombre de una ciudad")

        try:
            response = self.session.get(
                WEATHER_GEOCODING_URL,
                params={"name": city, "count": 1, "language": "es", "format": "json"},
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            places = response.json().get("results", [])
            if not places:
                raise ValueError("no se encontró esa ciudad")

            place = places[0]
            response = self.session.get(
                WEATHER_FORECAST_URL,
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m,relative_humidity_2m,weather_code",
                    "timezone": "auto"
                },
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            current = response.json().get("current", {})

            return {
                "ciudad": place.get("name", city),
                "pais": place.get("country", ""),
                "temperatura": current.get("temperature_2m"),
                "humedad": current.get("relative_humidity_2m"),
                "estado": self._description(current.get("weather_code")),
                "fecha": current.get("time", "")
            }
        except requests.Timeout as error:
            raise ConnectionError("la consulta del clima tardó demasiado") from error
        except requests.HTTPError as error:
            raise ConnectionError("el servicio del clima respondió con un error") from error
        except requests.RequestException as error:
            raise ConnectionError("no fue posible conectar con el servicio de clima") from error
        except (KeyError, TypeError) as error:
            raise ConnectionError("el servicio del clima entrego una respuesta inesperada") from error

    @staticmethod
    def _description(code):
        descriptions = {
            0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
            3: "Nublado", 45: "Niebla", 48: "Niebla con escarcha",
            51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna intensa",
            61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia intensa",
            71: "Nieve ligera", 73: "Nieve moderada", 75: "Nieve intensa",
            80: "Chubascos ligeros", 81: "Chubascos moderados",
            82: "Chubascos fuertes", 95: "Tormenta eléctrica"
        }
        return descriptions.get(code, "Estado no disponible")