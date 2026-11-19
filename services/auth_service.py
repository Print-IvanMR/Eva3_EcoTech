import re
import bcrypt

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.usuario_actual = None

    def register_admin(self, nombre, correo, password):
        if self.user_repository.count_users() > 0:
            raise ValueError("ya existe un usuario")
        if not nombre.strip():
            raise ValueError("ingresa tu nombre")
        correo = correo.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            raise ValueError("ingresa un correo")
        if len(password) < 8:
            raise ValueError("la contraseña debe tener al menos 8 caracteres")
        if len(password.encode("utf-8")) > 72:
            raise ValueError("la contraseña es demasiado larga")

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return self.user_repository.create_user(nombre, correo, password_hash)

    def login(self, correo, password):
        if not correo.strip() or not password:
            raise ValueError("completa el correo y la contraseña")

        usuario = self.user_repository.find_by_email(correo)
        if usuario is None:
            raise ValueError("correo o contraseña incorrectos")

        correcto = bcrypt.checkpw(
            password.encode("utf-8"),
            usuario["password"].encode("utf-8")
        )
        if not correcto:
            raise ValueError("correo o contraseña incorrectos")

        self.usuario_actual = usuario
        return usuario

    def logout(self):
        self.usuario_actual = None
