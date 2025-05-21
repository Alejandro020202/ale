from models.proyecto_model import ProyectoModel
from utils.security import sanitize_input

class ProyectoController:
    def __init__(self):
        self.proyecto_model = ProyectoModel()
    
    # ... (mantener todos los métodos existentes) ...

    def generar_certificado(self, cedula):
        """
        Genera un certificado para un participante
        """
        # Sanitizar entrada
        cedula = sanitize_input(cedula)
        
        # Obtener información del certificado
        info = self.proyecto_model.get_certificado_info(cedula)
        if not info:
            return False, "No se encontró un proyecto aprobado para generar el certificado"
            
        # Obtener firmantes
        firmantes = self.proyecto_model.get_firmantes()
        
        return True, {
            'participante': info['nombre'],
            'cedula': info['cedula'],
            'proyecto': info['proyecto'],
            'fecha': info['fecha'],
            'firmantes': firmantes
        }