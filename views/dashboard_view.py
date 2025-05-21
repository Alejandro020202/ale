import customtkinter as ctk
from controllers.proyecto_controller import ProyectoController
from tkinter import ttk
from views.ctk_treeview import CTkTreeview

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, user):
        super().__init__(parent)
        self.parent = parent
        self.switch_callback = switch_callback
        self.user = user
        self.proyecto_controller = ProyectoController()
        
        # Configurar el frame
        self.pack(fill="both", expand=True)
        
        # Crear los widgets
        self.create_widgets()
        
        # Cargar proyectos
        self.load_projects()
    
    def create_widgets(self):
        # Frame superior para la barra de navegación
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Título con el nombre del usuario y rol
        title_label = ctk.CTkLabel(
            nav_frame, 
            text=f"Bienvenido/a, {self.user['nombre']} - {self.user['rol'].replace('_', ' ')}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Botón de cerrar sesión
        logout_button = ctk.CTkButton(
            nav_frame, 
            text="Cerrar Sesión",
            command=self.logout
        )
        logout_button.pack(side="right", padx=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la sección
        section_label = ctk.CTkLabel(
            main_frame, 
            text="Panel de Control",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=10, padx=10, anchor="w")
        
        # Frame para botones de acción según el rol
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        # Botones según el rol del usuario
        if self.user['rol'] == 'Profesora_Encargada':
            # Botón para crear nuevo proyecto
            new_project_button = ctk.CTkButton(
                actions_frame, 
                text="Nuevo Proyecto",
                command=self.new_project
            )
            new_project_button.pack(side="left", padx=10)
        
        elif self.user['rol'] == 'Profesora_Administradora':
            # Botón para gestionar usuarios
            manage_users_button = ctk.CTkButton(
                actions_frame, 
                text="Gestionar Usuarios",
                command=self.manage_users
            )
            manage_users_button.pack(side="left", padx=10)
        
        # Frame para la lista de proyectos
        projects_frame = ctk.CTkFrame(main_frame)
        projects_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la lista de proyectos
        projects_label = ctk.CTkLabel(
            projects_frame, 
            text="Proyectos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        projects_label.pack(pady=5, padx=10, anchor="w")
        
        # Crear el Treeview para mostrar los proyectos
        columns = ("ID", "Nombre", "Materia", "Profesora", "Estado")
        
        # Frame para el treeview con scrollbar
        tree_frame = ctk.CTkFrame(projects_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        self.projects_tree = CTkTreeview(
            tree_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar las columnas
        self.projects_tree.column("ID", width=50)
        self.projects_tree.column("Nombre", width=200)
        self.projects_tree.column("Materia", width=150)
        self.projects_tree.column("Profesora", width=150)
        self.projects_tree.column("Estado", width=100)
        
        # Configurar los encabezados
        for col in columns:
            self.projects_tree.heading(col, text=col)
        
        # Empaquetar el treeview
        self.projects_tree.pack(fill="both", expand=True)
        scrollbar.configure(command=self.projects_tree.yview)
        
        # Configurar el evento de doble clic
        self.projects_tree.bind("<Double-1>", self.on_project_select)
        
        # Frame para detalles del proyecto
        self.details_frame = ctk.CTkFrame(main_frame)
        self.details_frame.pack(fill="x", padx=10, pady=10)
        
        # Título de detalles
        details_label = ctk.CTkLabel(
            self.details_frame, 
            text="Detalles del Proyecto",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        details_label.pack(pady=5, padx=10, anchor="w")
        
        # Contenedor para los detalles
        self.project_details = ctk.CTkTextbox(self.details_frame, height=150)
        self.project_details.pack(fill="x", padx=10, pady=5)
        self.project_details.configure(state="disabled")
        
        # Frame para botones de acción sobre el proyecto seleccionado
        self.project_actions_frame = ctk.CTkFrame(self.details_frame)
        self.project_actions_frame.pack(fill="x", padx=10, pady=5)
        
        # Botón para ver participantes
        self.view_participants_button = ctk.CTkButton(
            self.project_actions_frame, 
            text="Ver Participantes",
            command=self.show_participants,
            state="disabled"
        )
        self.view_participants_button.pack(side="left", padx=5)
        
        # Botón para ver aprobaciones
        self.view_approvals_button = ctk.CTkButton(
            self.project_actions_frame, 
            text="Ver Aprobaciones",
            command=self.show_approvals,
            state="disabled"
        )
        self.view_approvals_button.pack(side="left", padx=5)
        
        # Botón para aprobar proyecto (solo para roles específicos)
        if self.user['rol'] in ['Directora', 'Coordinadora', 'Profesora_Administradora']:
            self.approve_button = ctk.CTkButton(
                self.project_actions_frame, 
                text="Aprobar Proyecto",
                command=self.approve_project,
                state="disabled"
            )
            self.approve_button.pack(side="left", padx=5)
        
        # Botón para editar proyecto (solo para Profesora Encargada)
        if self.user['rol'] == 'Profesora_Encargada':
            self.edit_button = ctk.CTkButton(
                self.project_actions_frame, 
                text="Editar Proyecto",
                command=self.edit_project,
                state="disabled"
            )
            self.edit_button.pack(side="left", padx=5)
    
    def load_projects(self):
        """Carga los proyectos según el rol del usuario"""
        # Limpiar el treeview
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        print(f"Cargando proyectos para usuario: {self.user['nombre']} con rol: {self.user['rol']}")
        
        # Obtener proyectos según el rol
        projects = []
        if self.user['rol'] in ['Directora', 'Coordinadora', 'Profesora_Administradora']:
            # Pueden ver todos los proyectos
            print("Obteniendo todos los proyectos...")
            projects = self.proyecto_controller.get_all_projects()
        else:  # Profesora_Encargada
            # Solo ven sus propios proyectos
            print(f"Obteniendo proyectos para profesora ID: {self.user['id']}")
            projects = self.proyecto_controller.get_projects_by_profesora(self.user['id'])
        
        print(f"Proyectos encontrados: {len(projects) if projects else 0}")
        
        # Insertar proyectos en el treeview
        if projects:
            for project in projects:
                print(f"Insertando proyecto: {project['id']} - {project['nombre']}")
                self.projects_tree.insert(
                    "", "end", 
                    values=(
                        project['id'],
                        project['nombre'],
                        project['materia'],
                        project.get('profesora_nombre', self.user['nombre']),
                        project['estado']
                    ),
                    tags=(str(project['id']),)
                )
        else:
            print("No se encontraron proyectos para mostrar")
            # Mostrar mensaje en el treeview
            self.project_details.configure(state="normal")
            self.project_details.delete("1.0", "end")
            self.project_details.insert("1.0", "No se encontraron proyectos para mostrar.")
            self.project_details.configure(state="disabled")
    
    def on_project_select(self, event):
        """Maneja la selección de un proyecto"""
        # Verificar si hay elementos seleccionados
        selected_items = self.projects_tree.selection()
        if not selected_items:
            return
            
        # Obtener el item seleccionado
        selected_item = selected_items[0]
        values = self.projects_tree.item(selected_item)['values']
        if not values:
            return
            
        project_id = values[0]
        
        # Obtener los detalles del proyecto
        project = self.proyecto_controller.get_project_by_id(project_id)
        
        if project:
            # Mostrar detalles en el textbox
            self.project_details.configure(state="normal")
            self.project_details.delete("1.0", "end")
            self.project_details.insert("1.0", f"ID: {project['id']}\n")
            self.project_details.insert("end", f"Nombre: {project['nombre']}\n")
            self.project_details.insert("end", f"Materia: {project['materia']}\n")
            self.project_details.insert("end", f"Profesora: {project.get('profesora_nombre', '')}\n")
            self.project_details.insert("end", f"Estado: {project['estado']}\n")
            self.project_details.insert("end", f"Fecha de Creación: {project['fecha_creacion']}\n")
            self.project_details.insert("end", f"\nDescripción:\n{project['descripcion']}")
            self.project_details.configure(state="disabled")
            
            # Habilitar botones de acción
            self.view_participants_button.configure(state="normal")
            self.view_approvals_button.configure(state="normal")
            
            # Habilitar botón de aprobar si corresponde
            if hasattr(self, 'approve_button'):
                # Solo habilitar si el proyecto está pendiente
                if project['estado'] == 'Pendiente':
                    self.approve_button.configure(state="normal")
                else:
                    self.approve_button.configure(state="disabled")
            
            # Habilitar botón de editar si corresponde
            if hasattr(self, 'edit_button'):
                # Solo si es la profesora encargada del proyecto
                if project['profesora_id'] == self.user['id']:
                    self.edit_button.configure(state="normal")
                else:
                    self.edit_button.configure(state="disabled")
            
            # Guardar el ID del proyecto seleccionado
            self.selected_project_id = project_id
    
    def show_participants(self):
        """Muestra los participantes del proyecto seleccionado"""
        if hasattr(self, 'selected_project_id'):
            # Obtener participantes
            participants = self.proyecto_controller.get_participants(self.selected_project_id)
            
            # Crear ventana modal
            modal = ctk.CTkToplevel(self)
            modal.title("Participantes del Proyecto")
            modal.geometry("400x300")
            modal.transient(self.parent)  # Hacer que la ventana sea modal
            modal.grab_set()  # Bloquear la ventana principal
            
            # Título
            title_label = ctk.CTkLabel(
                modal, 
                text="Participantes del Proyecto",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=10, padx=10)
            
            # Frame para la lista
            list_frame = ctk.CTkFrame(modal)
            list_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Crear el Treeview para mostrar los participantes
            columns = ("ID", "Nombre", "Cédula")
            
            # Treeview con scrollbar
            tree_frame = ctk.CTkFrame(list_frame)
            tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            scrollbar = ctk.CTkScrollbar(tree_frame)
            scrollbar.pack(side="right", fill="y")
            
            participants_tree = CTkTreeview(
                tree_frame, 
                columns=columns,
                show="headings",
                yscrollcommand=scrollbar.set
            )
            
            # Configurar las columnas
            participants_tree.column("ID", width=50)
            participants_tree.column("Nombre", width=200)
            participants_tree.column("Cédula", width=150)
            
            # Configurar los encabezados
            for col in columns:
                participants_tree.heading(col, text=col)
            
            # Insertar participantes
            for participant in participants:
                participants_tree.insert(
                    "", "end", 
                    values=(
                        participant['id'],
                        participant['nombre'],
                        participant['cedula']
                    )
                )
            
            # Empaquetar el treeview
            participants_tree.pack(fill="both", expand=True)
            scrollbar.configure(command=participants_tree.yview)
            
            # Botón para cerrar
            close_button = ctk.CTkButton(
                modal, 
                text="Cerrar",
                command=modal.destroy
            )
            close_button.pack(pady=10)
    
    def show_approvals(self):
        """Muestra las aprobaciones del proyecto seleccionado"""
        if hasattr(self, 'selected_project_id'):
            # Obtener aprobaciones
            approvals = self.proyecto_controller.get_approvals(self.selected_project_id)
            
            # Crear ventana modal
            modal = ctk.CTkToplevel(self)
            modal.title("Aprobaciones del Proyecto")
            modal.geometry("500x300")
            modal.transient(self.parent)  # Hacer que la ventana sea modal
            modal.grab_set()  # Bloquear la ventana principal
            
            # Título
            title_label = ctk.CTkLabel(
                modal, 
                text="Aprobaciones del Proyecto",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=10, padx=10)
            
            # Frame para la lista
            list_frame = ctk.CTkFrame(modal)
            list_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Crear el Treeview para mostrar las aprobaciones
            columns = ("ID", "Aprobador", "Rol", "Fecha")
            
            # Treeview con scrollbar
            tree_frame = ctk.CTkFrame(list_frame)
            tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            scrollbar = ctk.CTkScrollbar(tree_frame)
            scrollbar.pack(side="right", fill="y")
            
            approvals_tree = CTkTreeview(
                tree_frame, 
                columns=columns,
                show="headings",
                yscrollcommand=scrollbar.set
            )
            
            # Configurar las columnas
            approvals_tree.column("ID", width=50)
            approvals_tree.column("Aprobador", width=150)
            approvals_tree.column("Rol", width=150)
            approvals_tree.column("Fecha", width=150)
            
            # Configurar los encabezados
            for col in columns:
                approvals_tree.heading(col, text=col)
            
            # Insertar aprobaciones
            for approval in approvals:
                approvals_tree.insert(
                    "", "end", 
                    values=(
                        approval['id'],
                        approval['aprobador_nombre'],
                        approval['rol_aprobador'],
                        approval['fecha_aprobacion']
                    )
                )
            
            # Empaquetar el treeview
            approvals_tree.pack(fill="both", expand=True)
            scrollbar.configure(command=approvals_tree.yview)
            
            # Botón para cerrar
            close_button = ctk.CTkButton(
                modal, 
                text="Cerrar",
                command=modal.destroy
            )
            close_button.pack(pady=10)
    
    def approve_project(self):
        """Aprueba el proyecto seleccionado"""
        if hasattr(self, 'selected_project_id'):
            # Confirmar la aprobación
            confirm_dialog = ctk.CTkToplevel(self)
            confirm_dialog.title("Confirmar Aprobación")
            confirm_dialog.geometry("400x150")
            confirm_dialog.transient(self.parent)
            confirm_dialog.grab_set()
            
            # Mensaje
            message_label = ctk.CTkLabel(
                confirm_dialog, 
                text="¿Está seguro que desea aprobar este proyecto?",
                font=ctk.CTkFont(size=14)
            )
            message_label.pack(pady=20, padx=20)
            
            # Frame para botones
            buttons_frame = ctk.CTkFrame(confirm_dialog)
            buttons_frame.pack(fill="x", padx=20, pady=10)
            
            # Botón de cancelar
            cancel_button = ctk.CTkButton(
                buttons_frame, 
                text="Cancelar",
                command=confirm_dialog.destroy
            )
            cancel_button.pack(side="left", padx=10, pady=10, expand=True)
            
            # Botón de confirmar
            confirm_button = ctk.CTkButton(
                buttons_frame, 
                text="Confirmar",
                command=lambda: self.confirm_approval(confirm_dialog)
            )
            confirm_button.pack(side="right", padx=10, pady=10, expand=True)
    
    def confirm_approval(self, dialog):
        """Confirma la aprobación del proyecto"""
        # Aprobar el proyecto
        success, message = self.proyecto_controller.approve_project(
            self.selected_project_id, 
            self.user['id'], 
            self.user['rol']
        )
        
        # Cerrar el diálogo de confirmación
        dialog.destroy()
        
        # Mostrar mensaje de resultado
        result_dialog = ctk.CTkToplevel(self)
        result_dialog.title("Resultado de Aprobación")
        result_dialog.geometry("400x150")
        result_dialog.transient(self.parent)
        result_dialog.grab_set()
        
        # Mensaje
        message_label = ctk.CTkLabel(
            result_dialog, 
            text=message,
            font=ctk.CTkFont(size=14)
        )
        message_label.pack(pady=20, padx=20)
        
        # Botón de aceptar
        ok_button = ctk.CTkButton(
            result_dialog, 
            text="Aceptar",
            command=result_dialog.destroy
        )
        ok_button.pack(pady=10)
        
        # Recargar proyectos
        self.load_projects()
    
    def edit_project(self):
        """Edita el proyecto seleccionado"""
        if hasattr(self, 'selected_project_id'):
            # Obtener el proyecto
            project = self.proyecto_controller.get_project_by_id(self.selected_project_id)
            
            # Verificar que sea el propietario
            if project['profesora_id'] != self.user['id']:
                return
            
            # Cambiar a la vista de proyecto con el proyecto seleccionado
            self.switch_callback("proyecto", self.user, project)
    
    def new_project(self):
        """Crea un nuevo proyecto"""
        # Cambiar a la vista de proyecto sin proyecto seleccionado
        self.switch_callback("proyecto", self.user, None)
    
    def manage_users(self):
        """Gestiona usuarios"""
        # Cambiar a la vista de usuario
        self.switch_callback("usuario", self.user)
    
    def logout(self):
        """Cierra la sesión del usuario"""
        # Cambiar a la vista de login
        self.switch_callback("login")
    
    def destroy(self):
        """Destruye la vista actual"""
        super().destroy()
