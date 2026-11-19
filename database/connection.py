from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from config.settings import MONGO_URI, DATABASE_NAME

class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.database = None

    def connect(self):
        if not MONGO_URI or "ivanmartinezrd14_db_user" in MONGO_URI or "cluster0" in MONGO_URI:
            raise ConnectionError("configurar la dirección de mongodb Atlas en el archivo .env")

        try:
            self.client = MongoClient(
                MONGO_URI,
                server_api=ServerApi("1"),
                serverSelectionTimeoutMS=8000
            )
            self.client.admin.command("ping")
            self.database = self.client[DATABASE_NAME]
            self.database.usuarios.create_index("correo", unique=True)
            self.database.historial.create_index("fecha")
            return self.database
        except PyMongoError as error:
            self.close()
            raise ConnectionError(
                "no se pudo conectar con mongodb atlas"
                "la contraseña y el acceso de red configurado en atlas"
            ) from error

    def get_database(self):
        if self.database is None:
            return self.connect()
        return self.database

    def close(self):
        if self.client is not None:
            self.client.close()
        self.client = None
        self.database = None
