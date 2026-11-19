from pymongo import MongoClient
import certifi
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from config.settings import MONGO_URI, DATABASE_NAME

class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.database = None

    def connect(self):
        if not MONGO_URI or "TU_USUARIO" in MONGO_URI or "TU_PASSWORD" in MONGO_URI:
            raise ConnectionError("configurar la dirección de MongoDB Atlas en el archivo .env")

        try:
            self.client = MongoClient(
                MONGO_URI,
                server_api=ServerApi("1"),
                tlsCAFile=certifi.where(),
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
                "no se pudo conectar con mongo. revise la contraseña y el acceso de red configurado en Atlas."
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