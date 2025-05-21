import customtkinter as ctk
from controllers.usuario_controller import UsuarioController
from tkinter import ttk
from views.ctk_treeview import CTkTreeview

class UsuarioView(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, user):
        super().__init__(parent)
        self.parent = parent
        self.switch_callback = switch_callback
        self.user = user
        self.usuario_controller = UsuarioController()
        
        # Verificar que el usuario tenga permisos de administrador
        if self.user['rol'] != 'Profesora_Administradora':
            self.switch_callback("dashboard", self.user)
            return
        
        # Configurar el frame
        self.pack(fill="both", expand=True)
        
        # Crear los widgets
        self.create_widgets()
        
        # Cargar usuarios
        self.load_users()
    
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
        section_label = ctk.CTkLabel(
            main_frame, 
            text="Gestión de Usuarios",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=10, padx=10, anchor="w")
        
        # Frame para el formulario de nuevo usuario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Configurar el grid para expandirse
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Título del formulario
        form_label = ctk.CTkLabel(
            form_frame, 
            text="Nuevo Usuario",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        form_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        # Campos del formulario
        # Nombre
        nombre_label = ctk.CTkLabel(form_frame, text="Nombre:")
        nombre_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.nombre_entry = ctk.CTkEntry(form_frame, width=300)
        self.nombre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Email
        email_label = ctk.CTkLabel(form_frame, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.email_entry = ctk.CTkEntry(form_frame, width=300)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Rol
        rol_label = ctk.CTkLabel(form_frame, text="Rol:")
        rol_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        roles = ["Directora", "Coordinadora", "Profesora_Administradora", "Profesora_Encargada"]
        self.rol_var = ctk.StringVar(value=roles[3])  # Default: Profesora_Encargada
        
        self.rol_combobox = ctk.CTkComboBox(form_frame, values=roles, variable=self.rol_var, width=300)
        self.rol_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # Materia asignada
        materia_label = ctk.CTkLabel(form_frame, text="Materia Asignada:")
        materia_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        self.materia_entry = ctk.CTkEntry(form_frame, width=300)
        self.materia_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # Contraseña
        password_label = ctk.CTkLabel(form_frame, text="Contraseña:")
        password_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        
        self.password_entry = ctk.CTkEntry(form_frame, width=300, show="*")
        self.password_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        # Confirmar contraseña
        confirm_label = ctk.CTkLabel(form_frame, text="Confirmar Contraseña:")
        confirm_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        
        self.confirm_entry = ctk.CTkEntry(form_frame, width=300, show="*")
        self.confirm_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        
        # Botón para crear usuario
        create_button = ctk.CTkButton(
            form_frame, 
            text="Crear Usuario",
            command=self.create_user
        )
        create_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10)
        
        # Mensaje de estado
        self.status_label = ctk.CTkLabel(form_frame, text="", text_color="green")
        self.status_label.grid(row=8, column=0, columnspan=2, pady=5, padx=10)
        
        # Frame para la lista de usuarios
        users_frame = ctk.CTkFrame(main_frame)
        users_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la lista
        users_label = ctk.CTkLabel(
            users_frame, 
            text="Usuarios Registrados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        users_label.pack(pady=5, padx=10, anchor="w")
        
        # Frame para el treeview con scrollbar
        tree_frame = ctk.CTkFrame(users_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Crear el Treeview para mostrar los usuarios
        columns = ("ID", "Nombre", "Email", "Rol", "Materia")
        
        self.users_tree = CTkTreeview(
            tree_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar las columnas
        self.users_tree.column("ID", width=50)
        self.users_tree.column("Nombre", width=150)
        self.users_tree.column("Email", width=200)
        self.users_tree.column("Rol", width=150)
        self.users_tree.column("Materia", width=150)
        
        # Configurar los encabezados
        for col in columns:
            self.users_tree.heading(col, text=col)
        
        # Empaquetar el treeview
        self.users_tree.pack(fill="both", expand=True)
        scrollbar.configure(command=self.users_tree.yview)
        
        # Botones de acción para usuarios seleccionados
        action_frame = ctk.CTkFrame(users_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        # Botón para eliminar usuario
        self.delete_button = ctk.CTkButton(
            action_frame,
            text="Eliminar Usuario",
            command=self.delete_user,
            state="disabled"
        )
        self.delete_button.pack(side="left", padx=5, pady=5)
        
        # Botón para cambiar contraseña
        self.change_password_button = ctk.CTkButton(
            action_frame,
            text="Cambiar Contraseña",
            command=self.show_change_password,
            state="disabled"
        )
        self.change_password_button.pack(side="left", padx=5, pady=5)
        
        # Configurar evento de selección
        self.users_tree.bind("<<TreeviewSelect>>", self.on_user_select)
    
    def load_users(self):
        """Carga los usuarios en el treeview"""
        # Limpiar el treeview
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Obtener usuarios
        users = self.usuario_controller.get_all_users()
        
        # Insertar usuarios en el treeview
        for user in users:
            self.users_tree.insert(
                "", "end", 
                values=(
                    user['id'],
                    user['nombre'],
                    user['email'],
                    user['rol'].replace('_', ' '),
                    user['materia_asignada']
                )
            )
    
    def on_user_select(self, event):
        """Maneja la selección de un usuario"""
        # Habilitar botones de acción
        self.delete_button.configure(state="normal")
        self.change_password_button.configure(state="normal")
    
    def create_user(self):
        """Crea un nuevo usuario"""
        # Obtener datos del formulario
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()
        rol = self.rol_var.get()
        materia = self.materia_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Validar campos
        if not nombre or not email or not materia or not password or not confirm:
            self.status_label.configure(text="Por favor, complete todos los campos", text_color="red")
            return
        
        if password != confirm:
            self.status_label.configure(text="Las contraseñas no coinciden", text_color="red")
            return
        
        # Crear usuario
        success, message = self.usuario_controller.create_user(
            nombre, rol, email, password, materia
        )
        
        if success:
            # Limpiar campos
            self.nombre_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.materia_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
            
            # Mostrar mensaje de éxito
            self.status_label.configure(text=message, text_color="green")
            
            # Recargar lista de usuarios
            self.load_users()
        else:
            # Mostrar mensaje de error
            self.status_label.configure(text=message, text_color="red")
    
    def delete_user(self):
        """Elimina un usuario seleccionado"""
        # Obtener el usuario seleccionado
        selected_items = self.users_tree.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        user_id = self.users_tree.item(selected_item)['values'][0]
        
        # Confirmar eliminación
        confirm_dialog = ctk.CTkToplevel(self)
        confirm_dialog.title("Confirmar Eliminación")
        confirm_dialog.geometry("400x150")
        confirm_dialog.transient(self.parent)
        confirm_dialog.grab_set()
        
        # Mensaje
        message_label = ctk.CTkLabel(
            confirm_dialog, 
            text="¿Está seguro que desea eliminar este usuario?",
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
            command=lambda: self.confirm_delete_user(confirm_dialog, user_id)
        )
        confirm_button.pack(side="right", padx=10, pady=10, expand=True)
    
    def confirm_delete_user(self, dialog, user_id):
        """Confirma la eliminación del usuario"""
        # Eliminar el usuario
        success, message = self.usuario_controller.delete_user(user_id)
        
        # Cerrar el diálogo de confirmación
        dialog.destroy()
        
        # Mostrar mensaje de resultado
        result_dialog = ctk.CTkToplevel(self)
        result_dialog.title("Resultado de Eliminación")
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
        
        # Recargar usuarios
        if success:
            self.load_users()
            # Deshabilitar botones de acción
            self.delete_button.configure(state="disabled")
            self.change_password_button.configure(state="disabled")
    
    def show_change_password(self):
        """Muestra el diálogo para cambiar la contraseña"""
        # Obtener el usuario seleccionado
        selected_items = self.users_tree.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        user_id = self.users_tree.item(selected_item)['values'][0]
        user_name = self.users_tree.item(selected_item)['values'][1]
        
        # Crear ventana modal
        modal = ctk.CTkToplevel(self)
        modal.title("Cambiar Contraseña")
        modal.geometry("400x250")
        modal.transient(self.parent)
        modal.grab_set()
        
        # Título
        title_label = ctk.CTkLabel(
            modal, 
            text=f"Cambiar Contraseña para {user_name}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=10, padx=10)
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(modal)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nueva contraseña
        new_password_label = ctk.CTkLabel(form_frame, text="Nueva Contraseña:")
        new_password_label.pack(pady=(10, 0), padx=10, anchor="w")
        
        new_password_entry = ctk.CTkEntry(form_frame, width=300, show="*")
        new_password_entry.pack(pady=(0, 10), padx=10)
        
        # Confirmar nueva contraseña
        confirm_label = ctk.CTkLabel(form_frame, text="Confirmar Contraseña:")
        confirm_label.pack(pady=(10, 0), padx=10, anchor="w")
        
        confirm_entry = ctk.CTkEntry(form_frame, width=300, show="*")
        confirm_entry.pack(pady=(0, 20), padx=10)
        
        # Mensaje de estado
        status_label = ctk.CTkLabel(form_frame, text="", text_color="red")
        status_label.pack(pady=5, padx=10)
        
        # Botones
        buttons_frame = ctk.CTkFrame(modal)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón de cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar",
            command=modal.destroy
        )
        cancel_button.pack(side="left", padx=10, pady=10, expand=True)
        
        # Función para cambiar la contraseña
        def change_password():
            new_password = new_password_entry.get()
            confirm = confirm_entry.get()
            
            # Validar campos
            if not new_password or not confirm:
                status_label.configure(text="Por favor, complete todos los campos", text_color="red")
                return
            
            if new_password != confirm:
                status_label.configure(text="Las contraseñas no coinciden", text_color="red")
                return
            
            # Cambiar la contraseña
            success, message = self.usuario_controller.change_password(user_id, new_password)
            
            if success:
                # Cerrar el modal
                modal.destroy()
                
                # Mostrar mensaje de éxito
                result_dialog = ctk.CTkToplevel(self)
                result_dialog.title("Resultado")
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
            else:
                # Mostrar mensaje de error
                status_label.configure(text=message, text_color="red")
        
        # Botón de guardar
        save_button = ctk.CTkButton(
            buttons_frame, 
            text="Guardar",
            command=change_password
        )
        save_button.pack(side="right", padx=10, pady=10, expand=True)
    
    def destroy(self):
        """Destruye la vista actual"""
        super().destroy()
