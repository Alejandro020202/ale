import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import os
from config import DB_CONFIG

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Inicializa el pool de conexiones"""
        self.host = DB_CONFIG['host']
        self.user = DB_CONFIG['user']
        self.password = DB_CONFIG['password']
        self.database = DB_CONFIG['database']
        self.pool_name = "proyectos_academicos_pool"
        self.pool_size = 5
        self.connection_pool = None
        self.create_pool()
    
    def create_pool(self):
        """Crea un pool de conexiones a la base de datos"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("✓ Pool de conexiones creado exitosamente")
        except Error as e:
            print(f"✗ Error al crear el pool de conexiones: {e}")
            raise
    
    def get_connection(self):
        """Obtiene una conexión del pool"""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            print(f"✗ Error al obtener conexión del pool: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """
        Ejecuta una consulta SQL
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            fetch_one (bool, optional): Si se debe devolver un solo resultado
            fetch_all (bool, optional): Si se deben devolver todos los resultados
            commit (bool, optional): Si se debe hacer commit después de la consulta
            
        Returns:
            dict/list/int: Resultado de la consulta según los parámetros
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if commit:
                connection.commit()
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            elif fetch_one:
                result = cursor.fetchone()
                return result
            elif fetch_all:
                result = cursor.fetchall()
                return result
            else:
                return None
                
        except Error as e:
            print(f"✗ Error al ejecutar consulta: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            if connection and commit:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_procedure(self, procedure, params=None, fetch_one=False, fetch_all=False):
        """
        Ejecuta un procedimiento almacenado
        
        Args:
            procedure (str): Nombre del procedimiento
            params (tuple, optional): Parámetros para el procedimiento
            fetch_one (bool, optional): Si se debe devolver un solo resultado
            fetch_all (bool, optional): Si se deben devolver todos los resultados
            
        Returns:
            dict/list: Resultado del procedimiento según los parámetros
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.callproc(procedure, params or ())
            
            results = []
            for result in cursor.stored_results():
                if fetch_one:
                    return result.fetchone()
                elif fetch_all:
                    results.extend(result.fetchall())
            
            return results if fetch_all else None
                
        except Error as e:
            print(f"✗ Error al ejecutar procedimiento: {e}")
            print(f"Procedure: {procedure}")
            print(f"Params: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
