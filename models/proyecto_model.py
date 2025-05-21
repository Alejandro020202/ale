from models.database import Database
from datetime import datetime

class ProyectoModel:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def get_certificado_info(self, cedula):
        """
        Obtiene la información para generar el certificado de un participante.
        Solo considera proyectos que tengan las 3 aprobaciones requeridas.
        """
        query = """
        SELECT DISTINCT 
            part.nombre as participante_nombre,
            part.cedula,
            p.nombre as proyecto_nombre,
            p.fecha_creacion,
            (
                SELECT COUNT(*)
                FROM Aprobaciones a
                WHERE a.proyecto_id = p.id
            ) as num_aprobaciones
        FROM Participantes part
        JOIN Proyectos p ON part.proyecto_id = p.id
        WHERE part.cedula = %s
        AND p.estado = 'Aprobado'
        AND EXISTS (
            SELECT 1 
            FROM Aprobaciones a 
            WHERE a.proyecto_id = p.id 
            GROUP BY a.proyecto_id 
            HAVING COUNT(*) >= 3
        )
        ORDER BY p.fecha_creacion ASC
        LIMIT 1
        """
        
        result = self.db.fetch_one(query, (cedula,))
        
        if not result:
            return None
            
        # Formatear la fecha
        fecha = result['fecha_creacion'].strftime('%d de %B del %Y')
        
        # Convertir el mes a español
        meses = {
            'January': 'enero',
            'February': 'febrero',
            'March': 'marzo',
            'April': 'abril',
            'May': 'mayo',
            'June': 'junio',
            'July': 'julio',
            'August': 'agosto',
            'September': 'septiembre',
            'October': 'octubre',
            'November': 'noviembre',
            'December': 'diciembre'
        }
        
        for mes_en, mes_es in meses.items():
            fecha = fecha.replace(mes_en, mes_es)
        
        return {
            'nombre': result['participante_nombre'],
            'cedula': result['cedula'],
            'proyecto': result['proyecto_nombre'],
            'fecha': fecha
        }

    def get_firmantes(self):
        """
        Obtiene la información de los firmantes del certificado
        """
        query = """
        SELECT nombre, rol 
        FROM Usuarias 
        WHERE rol IN ('Directora', 'Coordinadora')
        """
        return self.db.fetch_all(query)

    # ... (resto de métodos existentes) ...