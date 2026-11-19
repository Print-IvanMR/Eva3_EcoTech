import requests
from config.settings import CURRENCY_API_URL, REQUEST_TIMEOUT

class CurrencyService:
    CURRENCIES = ["CLP", "USD", "EUR", "GBP", "ARS", "BRL", "PEN", "MXN", "JPY", "CAD", "AUD", "CHF"]

    def convert(self, amount, origin, destination):
        try:
            amount = float(amount)
        except (TypeError, ValueError) as error:
            raise ValueError("ingrese un monto numerico") from error

        if amount <= 0:
            raise ValueError("el monto debe ser mayor que cero")

        origin = origin.upper()
        destination = destination.upper()
        if origin not in self.CURRENCIES or destination not in self.CURRENCIES:
            raise ValueError("seleccione una moneda disponible")

        if origin == destination:
            return {
                "monto": amount, "origen": origin, "destino": destination,
                "tasa": 1.0, "total": round(amount, 2), "fecha": "Misma moneda"
            }

        try:
            response = requests.get(
                f"{CURRENCY_API_URL}/{origin}/{destination}",
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            rate = float(data["rate"])
            return {
                "monto": amount,
                "origen": origin,
                "destino": destination,
                "tasa": rate,
                "total": round(amount * rate, 2),
                "fecha": data.get("date", "")
            }
        except requests.Timeout as error:
            raise ConnectionError("la consulta de monedas tardo demasiado") from error
        except requests.HTTPError as error:
            raise ConnectionError("el servicio de monedas respondio con un error") from error
        except requests.RequestException as error:
            raise ConnectionError("no fue posible conectar con el servicio de monedas") from error
        except (KeyError, TypeError, ValueError) as error:
            raise ConnectionError("el servicio de monedas entrego una respuesta inesperada") from error
