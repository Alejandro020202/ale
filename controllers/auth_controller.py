from models.usuario_model import UsuarioModel
from utils.security import check_password

class AuthController:
    def __init__(self):
        self.usuario_model = UsuarioModel()
    
    def login(self, email, password):
        """Autentica a un usuario por email y contraseña"""
        # Obtener usuario por email
        user = self.usuario_model.get_by_email(email)
        
        # Verificar si el usuario existe
        if not user:
            return None, "Usuario no encontrado"
        
        # Verificar la contraseña
        if not check_password(password, user['password_hash']):
            return None, "Contraseña incorrecta"
        
        # Autenticación exitosa
        return user, "Autenticación exitosa"
    
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID"""
        return self.usuario_model.get_by_id(user_id)
