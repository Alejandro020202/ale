import mysql.connector
from mysql.connector import Error
import os
import sys

class DatabaseInitializer:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = "proyectos_academicos"
        self.connection = None
    
    def initialize_database(self):
        """Inicializa la base de datos ejecutando el script SQL"""
        try:
            # Primero conectar sin especificar la base de datos
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            if self.connection.is_connected():
                print("Conexión a MySQL establecida")
                
                # Leer el script SQL
                script_path = os.path.join(os.path.dirname(__file__), 'create_database.sql')
                
                with open(script_path, 'r') as file:
                    sql_script = file.read()
                
                # Ejecutar el script SQL
                cursor = self.connection.cursor()
                
                # Dividir el script en comandos individuales
                # Esto es necesario porque execute() no puede ejecutar múltiples comandos a la vez
                commands = sql_script.split(';')
                
                for command in commands:
                    # Ignorar líneas vacías y comentarios
                    if command.strip() and not command.strip().startswith('--'):
                        cursor.execute(command)
                
                self.connection.commit()
                cursor.close()
                
                print("Base de datos inicializada correctamente")
                return True
                
        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            return False
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    # Si se ejecuta directamente, usar argumentos de línea de comandos o valores por defecto
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    user = sys.argv[2] if len(sys.argv) > 2 else "root"
    password = sys.argv[3] if len(sys.argv) > 3 else "password"
    
    initializer = DatabaseInitializer(host, user, password)
    initializer.initialize_database()
