from datetime import datetime, timezone

class HistoryRepository:
    def __init__(self, database):
        self.collection = database["historial"]

    def save_weather(self, correo, data):
        self.collection.insert_one({
            "usuario": correo,
            "tipo": "clima",
            "resultado": data,
            "fecha": datetime.now(timezone.utc)
        })

    def save_currency(self, correo, data):
        self.collection.insert_one({
            "usuario": correo,
            "tipo": "moneda",
            "resultado": data,
            "fecha": datetime.now(timezone.utc)
        })

    def get_history(self, correo):
        return list(
            self.collection.find({"usuario": correo}, {"_id": 0})
            .sort("fecha", -1)
            .limit(100)
        )
