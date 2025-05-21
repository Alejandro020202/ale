from models.database import Database

class ProyectoModel:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def get_all(self):
        """Obtiene todos los proyectos con información de la profesora encargada"""
        print("Modelo: Obteniendo todos los proyectos")
        try:
            # Consulta directa para obtener todos los proyectos
            query = """
            SELECT p.*, u.nombre as profesora_nombre 
            FROM Proyectos p
            JOIN Usuarias u ON p.profesora_id = u.id
            """
            result = self.db.fetch_all(query)
            print(f"Modelo: Proyectos encontrados: {len(result) if result else 0}")
            return result
        except Exception as e:
            print(f"Error al obtener todos los proyectos: {e}")
            return []
    
    def get_by_id(self, proyecto_id):
        """Obtiene un proyecto por su ID"""
        query = """
        SELECT p.*, u.nombre as profesora_nombre 
        FROM Proyectos p
        JOIN Usuarias u ON p.profesora_id = u.id
        WHERE p.id = %s
        """
        return self.db.fetch_one(query, (proyecto_id,))
    
    def get_by_profesora(self, profesora_id):
        """Obtiene todos los proyectos de una profesora"""
        print(f"Modelo: Obteniendo proyectos para profesora ID: {profesora_id}")
        try:
            # Consulta directa para obtener proyectos por profesora
            query = """
            SELECT p.*, u.nombre as profesora_nombre 
            FROM Proyectos p
            JOIN Usuarias u ON p.profesora_id = u.id
            WHERE p.profesora_id = %s
            """
            result = self.db.fetch_all(query, (profesora_id,))
            print(f"Modelo: Proyectos encontrados: {len(result) if result else 0}")
            return result
        except Exception as e:
            print(f"Error al obtener proyectos por profesora: {e}")
            return []
    
    def create(self, nombre, descripcion, materia, profesora_id):
        """Crea un nuevo proyecto"""
        query = """
        INSERT INTO Proyectos (nombre, descripcion, materia, profesora_id, estado)
        VALUES (%s, %s, %s, %s, 'Pendiente')
        """
        params = (nombre, descripcion, materia, profesora_id)
        return self.db.execute_query(query, params)
    
    def update(self, proyecto_id, nombre, descripcion, materia):
        """Actualiza un proyecto existente"""
        query = """
        UPDATE Proyectos 
        SET nombre = %s, descripcion = %s, materia = %s
        WHERE id = %s
        """
        params = (nombre, descripcion, materia, proyecto_id)
        return self.db.execute_query(query, params)
    
    def update_estado(self, proyecto_id, estado):
        """Actualiza el estado de un proyecto"""
        query = """
        UPDATE Proyectos 
        SET estado = %s
        WHERE id = %s
        """
        params = (estado, proyecto_id)
        return self.db.execute_query(query, params)
    
    def delete(self, proyecto_id):
        """Elimina un proyecto"""
        # Primero eliminar las referencias en otras tablas
        self.delete_participantes(proyecto_id)
        self.delete_aprobaciones(proyecto_id)
        
        # Luego eliminar el proyecto
        query = """
        DELETE FROM Proyectos 
        WHERE id = %s
        """
        return self.db.execute_query(query, (proyecto_id,))
    
    def add_participante(self, proyecto_id, nombre, cedula):
        """Añade un participante a un proyecto"""
        query = """
        INSERT INTO Participantes (proyecto_id, nombre, cedula)
        VALUES (%s, %s, %s)
        """
        params = (proyecto_id, nombre, cedula)
        return self.db.execute_query(query, params)
    
    def get_participantes(self, proyecto_id):
        """Obtiene todos los participantes de un proyecto"""
        query = """
        SELECT * FROM Participantes 
        WHERE proyecto_id = %s
        """
        return self.db.fetch_all(query, (proyecto_id,))
    
    def delete_participante(self, participante_id):
        """Elimina un participante"""
        query = """
        DELETE FROM Participantes 
        WHERE id = %s
        """
        return self.db.execute_query(query, (participante_id,))
    
    def delete_participantes(self, proyecto_id):
        """Elimina todos los participantes de un proyecto"""
        query = """
        DELETE FROM Participantes 
        WHERE proyecto_id = %s
        """
        return self.db.execute_query(query, (proyecto_id,))
    
    def check_participante_duplicado(self, cedula, exclude_proyecto_id=None):
        """
        Verifica si un participante ya existe en otro proyecto
        
        Args:
            cedula (str): Cédula del participante a verificar
            exclude_proyecto_id (int, optional): ID del proyecto a excluir de la verificación
            
        Returns:
            dict: Información del proyecto donde ya existe el participante, o None si no existe
        """
        try:
            if exclude_proyecto_id:
                query = """
                SELECT p.id, p.nombre, part.nombre as participante_nombre
                FROM Participantes part
                JOIN Proyectos p ON part.proyecto_id = p.id
                WHERE part.cedula = %s AND p.id != %s
                LIMIT 1
                """
                params = (cedula, exclude_proyecto_id)
            else:
                query = """
                SELECT p.id, p.nombre, part.nombre as participante_nombre
                FROM Participantes part
                JOIN Proyectos p ON part.proyecto_id = p.id
                WHERE part.cedula = %s
                LIMIT 1
                """
                params = (cedula,)
                
            return self.db.fetch_one(query, params)
        except Exception as e:
            print(f"Error al verificar participante duplicado: {e}")
            return None
    
    def approve_project(self, proyecto_id, usuaria_id, rol_aprobador):
        """Aprueba un proyecto verificando los roles específicos requeridos"""
        try:
            # Verificar si ya aprobó el proyecto
            check_query = """
            SELECT * FROM Aprobaciones 
            WHERE proyecto_id = %s AND usuaria_id = %s
            """
            existing = self.db.fetch_one(check_query, (proyecto_id, usuaria_id))
            
            if existing:
                return {'resultado': False, 'mensaje': "Ya has aprobado este proyecto"}
            
            # Añadir la aprobación
            add_query = """
            INSERT INTO Aprobaciones (proyecto_id, usuaria_id, rol_aprobador)
            VALUES (%s, %s, %s)
            """
            self.db.execute_query(add_query, (proyecto_id, usuaria_id, rol_aprobador))
            
            # Verificar si tiene las aprobaciones requeridas
            # Necesitamos: Profesora_Encargada, Profesora_Administradora y Coordinadora
            roles_query = """
            SELECT 
                SUM(CASE WHEN a.rol_aprobador = 'Profesora_Encargada' THEN 1 ELSE 0 END) as encargada,
                SUM(CASE WHEN a.rol_aprobador = 'Profesora_Administradora' THEN 1 ELSE 0 END) as administradora,
                SUM(CASE WHEN a.rol_aprobador = 'Coordinadora' THEN 1 ELSE 0 END) as coordinadora
            FROM Aprobaciones a
            WHERE a.proyecto_id = %s
            """
            roles_result = self.db.fetch_one(roles_query, (proyecto_id,))
            
            if not roles_result:
                return {'resultado': True, 'mensaje': "Aprobación registrada. Se requieren más aprobaciones."}
            
            # Verificar si tiene todas las aprobaciones requeridas
            tiene_encargada = roles_result.get('encargada', 0) > 0
            tiene_administradora = roles_result.get('administradora', 0) > 0
            tiene_coordinadora = roles_result.get('coordinadora', 0) > 0
            
            roles_faltantes = []
            if not tiene_encargada:
                roles_faltantes.append("Profesora Encargada")
            if not tiene_administradora:
                roles_faltantes.append("Profesora Administradora")
            if not tiene_coordinadora:
                roles_faltantes.append("Coordinadora")
            
            if not roles_faltantes:  # Si no faltan roles, está aprobado
                # Actualizar el estado del proyecto a "Aprobado"
                self.update_estado(proyecto_id, "Aprobado")
                return {'resultado': True, 'mensaje': "Proyecto aprobado completamente. Todas las aprobaciones requeridas han sido obtenidas."}
            else:
                # Construir mensaje con roles faltantes
                roles_str = ", ".join(roles_faltantes)
                return {'resultado': True, 'mensaje': f"Aprobación registrada. Aún se requiere la aprobación de: {roles_str}."}
                
        except Exception as e:
            print(f"Error al aprobar proyecto: {e}")
            return {'resultado': False, 'mensaje': f"Error al aprobar el proyecto: {str(e)}"}
    
    def get_aprobaciones(self, proyecto_id):
        """Obtiene todas las aprobaciones de un proyecto"""
        query = """
        SELECT a.*, u.nombre as aprobador_nombre 
        FROM Aprobaciones a
        JOIN Usuarias u ON a.usuaria_id = u.id
        WHERE a.proyecto_id = %s
        """
        return self.db.fetch_all(query, (proyecto_id,))
    
    def delete_aprobaciones(self, proyecto_id):
        """Elimina todas las aprobaciones de un proyecto"""
        query = """
        DELETE FROM Aprobaciones 
        WHERE proyecto_id = %s
        """
        return self.db.execute_query(query, (proyecto_id,))
