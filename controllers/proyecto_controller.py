from models.proyecto_model import ProyectoModel
from utils.security import sanitize_input

class ProyectoController:
    def __init__(self):
        self.proyecto_model = ProyectoModel()
    
    def get_all_projects(self):
        """Obtiene todos los proyectos"""
        print("Controlador: Obteniendo todos los proyectos")
        projects = self.proyecto_model.get_all()
        print(f"Controlador: Proyectos encontrados: {len(projects) if projects else 0}")
        return projects
    
    def get_project_by_id(self, proyecto_id):
        """Obtiene un proyecto por su ID"""
        return self.proyecto_model.get_by_id(proyecto_id)
    
    def get_projects_by_profesora(self, profesora_id):
        """Obtiene todos los proyectos de una profesora"""
        print(f"Controlador: Obteniendo proyectos para profesora ID: {profesora_id}")
        projects = self.proyecto_model.get_by_profesora(profesora_id)
        print(f"Controlador: Proyectos encontrados: {len(projects) if projects else 0}")
        return projects
    
    def create_project(self, nombre, descripcion, materia, profesora_id):
        """Crea un nuevo proyecto"""
        # Sanitizar entradas
        nombre = sanitize_input(nombre)
        descripcion = sanitize_input(descripcion)
        materia = sanitize_input(materia)
        
        # Crear el proyecto
        proyecto_id = self.proyecto_model.create(nombre, descripcion, materia, profesora_id)
        if proyecto_id:
            return True, proyecto_id, "Proyecto creado exitosamente"
        else:
            return False, None, "Error al crear el proyecto"
    
    def update_project(self, proyecto_id, nombre, descripcion, materia):
        """Actualiza un proyecto existente"""
        # Sanitizar entradas
        nombre = sanitize_input(nombre)
        descripcion = sanitize_input(descripcion)
        materia = sanitize_input(materia)
        
        # Actualizar el proyecto
        result = self.proyecto_model.update(proyecto_id, nombre, descripcion, materia)
        if result:
            return True, "Proyecto actualizado exitosamente"
        else:
            return False, "Error al actualizar el proyecto"
    
    def delete_project(self, proyecto_id):
        """Elimina un proyecto"""
        result = self.proyecto_model.delete(proyecto_id)
        if result:
            return True, "Proyecto eliminado exitosamente"
        else:
            return False, "Error al eliminar el proyecto"
    
    def add_participant(self, proyecto_id, nombre, cedula):
        """Añade un participante a un proyecto"""
        # Sanitizar entradas
        nombre = sanitize_input(nombre)
        cedula = sanitize_input(cedula)
        
        # Verificar si el participante ya existe en otro proyecto
        duplicado = self.proyecto_model.check_participante_duplicado(cedula, exclude_proyecto_id=proyecto_id)
        if duplicado:
            return False, f"El participante con cédula {cedula} ya está registrado en el proyecto '{duplicado['nombre']}'"
        
        # Añadir el participante
        result = self.proyecto_model.add_participante(proyecto_id, nombre, cedula)
        if result:
            return True, "Participante añadido exitosamente"
        else:
            return False, "Error al añadir el participante"
    
    def check_participant_exists(self, cedula, exclude_proyecto_id=None):
        """Verifica si un participante ya existe en otro proyecto"""
        duplicado = self.proyecto_model.check_participante_duplicado(cedula, exclude_proyecto_id)
        if duplicado:
            return True, duplicado
        return False, None
    
    def get_participants(self, proyecto_id):
        """Obtiene todos los participantes de un proyecto"""
        return self.proyecto_model.get_participantes(proyecto_id)
    
    def delete_participant(self, participante_id):
        """Elimina un participante"""
        result = self.proyecto_model.delete_participante(participante_id)
        if result:
            return True, "Participante eliminado exitosamente"
        else:
            return False, "Error al eliminar el participante"
    
    def approve_project(self, proyecto_id, usuaria_id, rol_aprobador):
        """Aprueba un proyecto usando el procedimiento almacenado"""
        result = self.proyecto_model.approve_project(proyecto_id, usuaria_id, rol_aprobador)
        if result and 'resultado' in result and result['resultado']:
            return True, result['mensaje']
        else:
            return False, result.get('mensaje', "Error al aprobar el proyecto")
    
    def get_approvals(self, proyecto_id):
        """Obtiene todas las aprobaciones de un proyecto"""
        return self.proyecto_model.get_aprobaciones(proyecto_id)
