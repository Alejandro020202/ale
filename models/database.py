from database.database_connection import DatabaseConnection

class Database:
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def connect(self):
        """Verifica la conexión a la base de datos"""
        try:
            # Obtener una conexión del pool para verificar
            connection = self.db_connection.get_connection()
            if connection.is_connected():
                connection.close()
                print("✓ Conexión a MySQL establecida")
                return True
            return False
        except Exception as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            return False
    
    def disconnect(self):
        """No es necesario cerrar conexiones explícitamente con el pool"""
        pass
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL que no devuelve resultados"""
        try:
            return self.db_connection.execute_query(query, params=params, commit=True)
        except Exception as e:
            print(f"✗ Error al ejecutar la consulta: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve todos los resultados"""
        try:
            print(f"Ejecutando consulta: {query}")
            print(f"Parámetros: {params}")
            result = self.db_connection.execute_query(query, params=params, fetch_all=True)
            print(f"Resultados obtenidos: {len(result) if result else 0}")
            return result
        except Exception as e:
            print(f"✗ Error al ejecutar la consulta fetch_all: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve un solo resultado"""
        try:
            return self.db_connection.execute_query(query, params=params, fetch_one=True)
        except Exception as e:
            print(f"✗ Error al ejecutar la consulta: {e}")
            return None
    
    def call_procedure(self, procedure, params=None, fetch_all=False, fetch_one=False):
        """Ejecuta un procedimiento almacenado"""
        try:
            return self.db_connection.execute_procedure(
                procedure, params=params, fetch_all=fetch_all, fetch_one=fetch_one
            )
        except Exception as e:
            print(f"✗ Error al ejecutar el procedimiento: {e}")
            if fetch_all:
                return []
            elif fetch_one:
                return None
            else:
                return False
