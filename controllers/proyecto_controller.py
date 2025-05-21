from models.proyecto_model import ProyectoModel
from utils.security import sanitize_input
from utils.certificate_generator import CertificateGenerator
from PIL import Image, ImageDraw, ImageFont
import os

class ProyectoController:
    def __init__(self):
        self.proyecto_model = ProyectoModel()
        self.certificate_generator = CertificateGenerator()
    
    def generar_certificado(self, cedula):
        """
        Genera un certificado para un participante
        
        Args:
            cedula (str): Número de cédula del participante
            
        Returns:
            tuple: (bool, str/dict) - (éxito, mensaje de error/datos del certificado)
        """
        # Sanitizar entrada
        cedula = sanitize_input(cedula)
        
        # Obtener información del certificado
        info = self.proyecto_model.get_certificado_info(cedula)
        if not info:
            return False, "No se encontró un proyecto aprobado para generar el certificado"
            
        # Obtener firmantes
        firmantes = self.proyecto_model.get_firmantes()
        
        # Datos para el certificado
        data = {
            'participante': info['nombre'],
            'cedula': info['cedula'],
            'proyecto': info['proyecto'],
            'fecha': info['fecha'],
            'firmantes': firmantes
        }
        
        try:
            # Generar el certificado visual
            certificate_path = self.certificate_generator.generate(data)
            data['certificate_path'] = certificate_path
            return True, data
        except Exception as e:
            return False, f"Error al generar el certificado: {str(e)}"

    # ... (resto de métodos existentes) ...