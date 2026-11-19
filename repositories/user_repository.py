from pymongo.errors import DuplicateKeyError

class UserRepository:
    def __init__(self, database):
        self.collection = database["usuarios"]

    def count_users(self):
        return self.collection.count_documents({})

    def create_user(self, nombre, correo, password_hash):
        usuario = {
            "nombre": nombre.strip(),
            "correo": correo.strip().lower(),
            "password": password_hash,
            "rol": "Administrador"
        }
        try:
            result = self.collection.insert_one(usuario)
            usuario["_id"] = result.inserted_id
            return usuario
        except DuplicateKeyError as error:
            raise ValueError("ya existe una cuenta con ese correo") from error

    def find_by_email(self, correo):
        return self.collection.find_one({"correo": correo.strip().lower()})
