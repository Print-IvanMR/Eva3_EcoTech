from database.connection import DatabaseConnection

if __name__ == "__main__":
    print("iniciando prueba")
    connection = DatabaseConnection()
    try:
        connection.connect()
        print("Conectatdo con MongoDB")
    except ConnectionError as error:
        print(error)
    finally:
        connection.close()
        print("prueba finalizada")
