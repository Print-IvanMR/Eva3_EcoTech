from database.connection import DatabaseConnection
from repositories.user_repository import UserRepository
from repositories.history_repository import HistoryRepository
from services.auth_service import AuthService
from services.weather_service import WeatherService
from services.currency_service import CurrencyService
from ui.login_window import LoginWindow
from ui.dashboard import Dashboard

class EcoTechApplication:
    def __init__(self):
        self.database_connection = DatabaseConnection()
        self.database = self.database_connection.connect()
        self.user_repository = UserRepository(self.database)
        self.history_repository = HistoryRepository(self.database)
        self.auth_service = AuthService(self.user_repository)
        self.weather_service = WeatherService()
        self.currency_service = CurrencyService()

    def open_dashboard(self, usuario):
        dashboard = Dashboard(
            usuario,
            self.auth_service,
            self.weather_service,
            self.currency_service,
            self.history_repository,
            self.show_login
        )
        dashboard.run()

    def show_login(self):
        login = LoginWindow(self.auth_service, self.open_dashboard)
        login.run()

    def run(self):
        try:
            self.show_login()
        finally:
            self.database_connection.close()

if __name__ == "__main__":
    try:
        app = EcoTechApplication()
        app.run()
    except ConnectionError as error:
        print(error)
    except Exception:
        print("ocurrio un error al iniciar el sistema")
