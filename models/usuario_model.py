from models.database import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def get_by_email(self, email):
        """Obtiene un usuario por su email"""
        query = """
        SELECT * FROM Usuarias 
        WHERE email = %s
        """
        return self.db.fetch_one(query, (email,))
    
    def get_by_id(self, user_id):
        """Obtiene un usuario por su ID"""
        query = """
        SELECT * FROM Usuarias 
        WHERE id = %s
        """
        return self.db.fetch_one(query, (user_id,))
    
    def get_all(self):
        """Obtiene todos los usuarios"""
        query = """
        SELECT id, nombre, rol, email, materia_asignada 
        FROM Usuarias
        """
        return self.db.fetch_all(query)
    
    def create(self, nombre, rol, email, password_hash, materia_asignada):
        """Crea un nuevo usuario"""
        query = """
        INSERT INTO Usuarias (nombre, rol, email, password_hash, materia_asignada)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (nombre, rol, email, password_hash, materia_asignada)
        return self.db.execute_query(query, params)
    
    def update(self, user_id, nombre, rol, email, materia_asignada):
        """Actualiza un usuario existente"""
        query = """
        UPDATE Usuarias 
        SET nombre = %s, rol = %s, email = %s, materia_asignada = %s
        WHERE id = %s
        """
        params = (nombre, rol, email, materia_asignada, user_id)
        return self.db.execute_query(query, params)
    
    def update_password(self, user_id, password_hash):
        """Actualiza la contraseña de un usuario"""
        query = """
        UPDATE Usuarias 
        SET password_hash = %s
        WHERE id = %s
        """
        params = (password_hash, user_id)
        return self.db.execute_query(query, params)
    
    def delete(self, user_id):
        """Elimina un usuario"""
        query = """
        DELETE FROM Usuarias 
        WHERE id = %s
        """
        return self.db.execute_query(query, (user_id,))
