from models.usuario_model import UsuarioModel
from utils.security import hash_password, sanitize_input

class UsuarioController:
    def __init__(self):
        self.usuario_model = UsuarioModel()
    
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        return self.usuario_model.get_all()
    
    def create_user(self, nombre, rol, email, password, materia_asignada):
        """Crea un nuevo usuario"""
        # Sanitizar entradas
        nombre = sanitize_input(nombre)
        email = sanitize_input(email)
        materia_asignada = sanitize_input(materia_asignada)
        
        # Verificar si el email ya existe
        existing_user = self.usuario_model.get_by_email(email)
        if existing_user:
            return False, "El email ya está registrado"
        
        # Hashear la contraseña
        password_hash = hash_password(password)
        
        # Crear el usuario
        user_id = self.usuario_model.create(nombre, rol, email, password_hash, materia_asignada)
        if user_id:
            return True, "Usuario creado exitosamente"
        else:
            return False, "Error al crear el usuario"
    
    def update_user(self, user_id, nombre, rol, email, materia_asignada):
        """Actualiza un usuario existente"""
        # Sanitizar entradas
        nombre = sanitize_input(nombre)
        email = sanitize_input(email)
        materia_asignada = sanitize_input(materia_asignada)
        
        # Verificar si el email ya existe en otro usuario
        existing_user = self.usuario_model.get_by_email(email)
        if existing_user and existing_user['id'] != user_id:
            return False, "El email ya está registrado por otro usuario"
        
        # Actualizar el usuario
        result = self.usuario_model.update(user_id, nombre, rol, email, materia_asignada)
        if result:
            return True, "Usuario actualizado exitosamente"
        else:
            return False, "Error al actualizar el usuario"
    
    def change_password(self, user_id, new_password):
        """Cambia la contraseña de un usuario"""
        # Hashear la nueva contraseña
        password_hash = hash_password(new_password)
        
        # Actualizar la contraseña
        result = self.usuario_model.update_password(user_id, password_hash)
        if result:
            return True, "Contraseña actualizada exitosamente"
        else:
            return False, "Error al actualizar la contraseña"
    
    def delete_user(self, user_id):
        """Elimina un usuario"""
        result = self.usuario_model.delete(user_id)
        if result:
            return True, "Usuario eliminado exitosamente"
        else:
            return False, "Error al eliminar el usuario"
