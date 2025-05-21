import customtkinter as ctk
from controllers.proyecto_controller import ProyectoController
from tkinter import ttk
from views.ctk_treeview import CTkTreeview

class ProyectoView(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, user, project=None):
        super().__init__(parent)
        self.parent = parent
        self.switch_callback = switch_callback
        self.user = user
        self.project = project  # Proyecto a editar (None si es nuevo)
        self.proyecto_controller = ProyectoController()
        self.participants = []  # Lista de participantes
        
        # Configurar el frame
        self.pack(fill="both", expand=True)
        
        # Crear los widgets
        self.create_widgets()
        
        # Si es edición, cargar los datos del proyecto
        if self.project:
            self.load_project_data()
    
    def create_widgets(self):
        # Frame superior para la barra de navegación
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Título con el nombre del usuario y rol
        title_label = ctk.CTkLabel(
            nav_frame, 
            text=f"{self.user['nombre']} - {self.user['rol'].replace('_', ' ')}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Botón de volver al dashboard
        back_button = ctk.CTkButton(
            nav_frame, 
            text="Volver al Dashboard",
            command=lambda: self.switch_callback("dashboard", self.user)
        )
        back_button.pack(side="right", padx=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la sección
        section_title = "Editar Proyecto" if self.project else "Nuevo Proyecto"
        section_label = ctk.CTkLabel(
            main_frame, 
            text=section_title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=10, padx=10, anchor="w")
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Configurar el grid para expandirse
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Campos del formulario
        # Nombre del proyecto
        nombre_label = ctk.CTkLabel(form_frame, text="Nombre del Proyecto:")
        nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.nombre_entry = ctk.CTkEntry(form_frame, width=400)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Materia
        materia_label = ctk.CTkLabel(form_frame, text="Materia:")
        materia_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.materia_entry = ctk.CTkEntry(form_frame, width=400)
        self.materia_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Descripción
        descripcion_label = ctk.CTkLabel(form_frame, text="Descripción:")
        descripcion_label.grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        
        self.descripcion_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        self.descripcion_text.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Frame para la lista de participantes
        participants_frame = ctk.CTkFrame(main_frame)
        participants_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de participantes
        participants_label = ctk.CTkLabel(
            participants_frame, 
            text="Participantes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        participants_label.pack(pady=5, padx=10, anchor="w")
        
        # Frame para añadir participantes
        add_participant_frame = ctk.CTkFrame(participants_frame)
        add_participant_frame.pack(fill="x", padx=10, pady=5)
        
        # Configurar el grid para expandirse
        add_participant_frame.grid_columnconfigure(1, weight=1)
        add_participant_frame.grid_columnconfigure(3, weight=1)
        
        # Campos para añadir participante
        # Nombre
        nombre_part_label = ctk.CTkLabel(add_participant_frame, text="Nombre:")
        nombre_part_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.nombre_part_entry = ctk.CTkEntry(add_participant_frame, width=200)
        self.nombre_part_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Cédula
        cedula_label = ctk.CTkLabel(add_participant_frame, text="Cédula:")
        cedula_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.cedula_entry = ctk.CTkEntry(add_participant_frame, width=150)
        self.cedula_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Botón para añadir
        add_button = ctk.CTkButton(
            add_participant_frame, 
            text="Añadir",
            command=self.add_participant
        )
        add_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Mensaje de estado para participantes
        self.participant_status_label = ctk.CTkLabel(add_participant_frame, text="", text_color="red")
        self.participant_status_label.grid(row=1, column=0, columnspan=5, pady=5, padx=10, sticky="w")
        
        # Frame para la lista de participantes
        list_frame = ctk.CTkFrame(participants_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear el Treeview para mostrar los participantes
        columns = ("ID", "Nombre", "Cédula", "Acciones")
        
        # Treeview con scrollbar
        tree_frame = ctk.CTkFrame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.participants_tree = CTkTreeview(
            tree_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar las columnas
        self.participants_tree.column("ID", width=50)
        self.participants_tree.column("Nombre", width=200)
        self.participants_tree.column("Cédula", width=150)
        self.participants_tree.column("Acciones", width=100)
        
        # Configurar los encabezados
        for col in columns:
            self.participants_tree.heading(col, text=col)
        
        # Empaquetar el treeview
        self.participants_tree.pack(fill="both", expand=True)
        scrollbar.configure(command=self.participants_tree.yview)
        
        # Frame para botones de acción
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar",
            command=lambda: self.switch_callback("dashboard", self.user)
        )
        cancel_button.pack(side="left", padx=10, pady=10)
        
        # Botón para guardar
        save_button = ctk.CTkButton(
            buttons_frame, 
            text="Guardar Proyecto",
            command=self.save_project
        )
        save_button.pack(side="right", padx=10, pady=10)
        
        # Mensaje de estado
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="green")
        self.status_label.pack(pady=5, padx=10)
    
    def load_project_data(self):
        """Carga los datos del proyecto a editar"""
        if self.project:
            # Cargar datos básicos
            self.nombre_entry.insert(0, self.project['nombre'])
            self.materia_entry.insert(0, self.project['materia'])
            self.descripcion_text.insert("1.0", self.project['descripcion'])
            
            # Cargar participantes
            participants = self.proyecto_controller.get_participants(self.project['id'])
            for participant in participants:
                self.participants.append(participant)
            
            # Actualizar la lista de participantes
            self.update_participants_list()
    
    def add_participant(self):
        """Añade un participante a la lista temporal"""
        nombre = self.nombre_part_entry.get()
        cedula = self.cedula_entry.get()
        
        # Validar campos
        if not nombre or not cedula:
            self.participant_status_label.configure(text="Por favor, complete todos los campos del participante", text_color="red")
            return
        
        # Verificar si el participante ya existe en otro proyecto
        proyecto_id = self.project['id'] if self.project else None
        exists, duplicado = self.proyecto_controller.check_participant_exists(cedula, proyecto_id)
        
        if exists:
            self.participant_status_label.configure(
                text=f"El participante con cédula {cedula} ya está registrado en el proyecto '{duplicado['nombre']}'", 
                text_color="red"
            )
            return
        
        # Crear un participante temporal (sin ID si es nuevo proyecto)
        participant = {
            'id': None,  # Se asignará al guardar
            'nombre': nombre,
            'cedula': cedula,
            'temp_id': len(self.participants) + 1  # ID temporal para la lista
        }
        
        # Añadir a la lista
        self.participants.append(participant)
        
        # Limpiar campos
        self.nombre_part_entry.delete(0, 'end')
        self.cedula_entry.delete(0, 'end')
        
        # Actualizar la lista
        self.update_participants_list()
        
        # Limpiar mensaje de estado
        self.participant_status_label.configure(text="")
        self.status_label.configure(text="")
    
    def update_participants_list(self):
        """Actualiza la lista de participantes en el treeview"""
        # Limpiar el treeview
        for item in self.participants_tree.get_children():
            self.participants_tree.delete(item)
        
        # Insertar participantes
        for participant in self.participants:
            # Usar ID real o temporal
            participant_id = participant.get('id') or participant.get('temp_id')
            
            item_id = self.participants_tree.insert(
                "", "end", 
                values=(
                    participant_id,
                    participant['nombre'],
                    participant['cedula'],
                    "Eliminar"
                )
            )
            
            # Configurar evento para eliminar
            self.participants_tree.tag_bind(
                item_id, 
                '<ButtonRelease-1>', 
                lambda event, id=participant_id: self.remove_participant(id)
            )
    
    def remove_participant(self, participant_id):
        """Elimina un participante de la lista temporal"""
        # Buscar el participante por ID
        for i, participant in enumerate(self.participants):
            if (participant.get('id') == participant_id or 
                participant.get('temp_id') == participant_id):
                # Eliminar de la lista
                self.participants.pop(i)
                break
        
        # Actualizar la lista
        self.update_participants_list()
    
    def save_project(self):
        """Guarda el proyecto (nuevo o edición)"""
        # Obtener datos del formulario
        nombre = self.nombre_entry.get()
        materia = self.materia_entry.get()
        descripcion = self.descripcion_text.get("1.0", "end-1c")  # Obtener texto sin el último salto de línea
        
        # Validar campos
        if not nombre or not materia or not descripcion:
            self.status_label.configure(text="Por favor, complete todos los campos del proyecto", text_color="red")
            return
        
        if not self.participants:
            self.status_label.configure(text="Debe añadir al menos un participante", text_color="red")
            return
        
        # Guardar el proyecto
        if self.project:  # Edición
            success, message = self.proyecto_controller.update_project(
                self.project['id'], nombre, descripcion, materia
            )
            
            if success:
                # Eliminar participantes existentes y añadir los nuevos
                for participant in self.participants:
                    if not participant.get('id'):  # Si es nuevo participante
                        self.proyecto_controller.add_participant(
                            self.project['id'], participant['nombre'], participant['cedula']
                        )
                
                self.status_label.configure(text="Proyecto actualizado exitosamente", text_color="green")
                # Volver al dashboard después de un breve retraso
                self.after(2000, lambda: self.switch_callback("dashboard", self.user))
            else:
                self.status_label.configure(text=message, text_color="red")
        
        else:  # Nuevo proyecto
            success, proyecto_id, message = self.proyecto_controller.create_project(
                nombre, descripcion, materia, self.user['id']
            )
            
            if success:
                # Añadir participantes
                for participant in self.participants:
                    self.proyecto_controller.add_participant(
                        proyecto_id, participant['nombre'], participant['cedula']
                    )
                
                self.status_label.configure(text="Proyecto creado exitosamente", text_color="green")
                # Volver al dashboard después de un breve retraso
                self.after(2000, lambda: self.switch_callback("dashboard", self.user))
            else:
                self.status_label.configure(text=message, text_color="red")
    
    def destroy(self):
        """Destruye la vista actual"""
        super().destroy()
