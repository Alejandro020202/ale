import customtkinter as ctk
from controllers.auth_controller import AuthController
from PIL import Image, ImageTk
import os

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent, fg_color="#f0f0f0")
        self.parent = parent
        self.switch_callback = switch_callback
        self.auth_controller = AuthController()
        
        # Configurar el frame
        self.pack(fill="both", expand=True)
        
        # Crear los widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Configurar colores
        primary_color = "#3498db"  # Azul
        secondary_color = "#2980b9"  # Azul oscuro
        accent_color = "#e74c3c"  # Rojo
        text_color = "#2c3e50"  # Azul oscuro/gris
        bg_color = "#ecf0f1"  # Gris claro
        
        # Frame principal con dos columnas
        main_frame = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # Columna izquierda (imagen/banner)
        left_frame = ctk.CTkFrame(main_frame, fg_color=primary_color, corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Logo o imagen
        logo_label = ctk.CTkLabel(
            left_frame, 
            text="Sistema de\nGestión de\nProyectos\nAcadémicos",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        logo_label.pack(pady=(150, 20), padx=30)
        
        # Descripción
        description_label = ctk.CTkLabel(
            left_frame, 
            text="Plataforma para la gestión, seguimiento\ny aprobación de proyectos académicos",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        description_label.pack(pady=10, padx=30)
        
        # Versión
        version_label = ctk.CTkLabel(
            left_frame, 
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        version_label.pack(side="bottom", pady=20)
        
        # Columna derecha (formulario)
        right_frame = ctk.CTkFrame(main_frame, fg_color=bg_color, corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Contenedor del formulario
        form_container = ctk.CTkFrame(right_frame, fg_color="white", corner_radius=15)
        form_container.pack(pady=100, padx=60, fill="both", expand=False)
        
        # Título
        title_label = ctk.CTkLabel(
            form_container, 
            text="Iniciar Sesión",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=text_color
        )
        title_label.pack(pady=(30, 20), padx=30)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            form_container, 
            text="Ingrese sus credenciales para acceder al sistema",
            font=ctk.CTkFont(size=14),
            text_color=text_color
        )
        subtitle_label.pack(pady=(0, 20), padx=30)
        
        # Campo de email
        email_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        email_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        email_label = ctk.CTkLabel(
            email_frame, 
            text="Email",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=text_color
        )
        email_label.pack(anchor="w", padx=5)
        
        self.email_entry = ctk.CTkEntry(
            email_frame, 
            width=300,
            height=40,
            placeholder_text="ejemplo@correo.com",
            border_width=1,
            corner_radius=8
        )
        self.email_entry.pack(fill="x", pady=(5, 0))
        
        # Campo de contraseña
        password_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        password_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        password_label = ctk.CTkLabel(
            password_frame, 
            text="Contraseña",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=text_color
        )
        password_label.pack(anchor="w", padx=5)
        
        self.password_entry = ctk.CTkEntry(
            password_frame, 
            width=300,
            height=40,
            placeholder_text="••••••••",
            show="•",
            border_width=1,
            corner_radius=8
        )
        self.password_entry.pack(fill="x", pady=(5, 0))
        
        # Botón de inicio de sesión
        login_button = ctk.CTkButton(
            form_container, 
            text="Iniciar Sesión",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            corner_radius=8,
            fg_color=primary_color,
            hover_color=secondary_color,
            command=self.login
        )
        login_button.pack(pady=(20, 10), padx=30, fill="x")
        
        # Mensaje de error
        self.error_label = ctk.CTkLabel(
            form_container, 
            text="",
            text_color=accent_color,
            font=ctk.CTkFont(size=14)
        )
        self.error_label.pack(pady=(5, 30), padx=30)
        
        # Información de ayuda
        help_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        help_frame.pack(side="bottom", fill="x", padx=30, pady=20)
        
        help_label = ctk.CTkLabel(
            help_frame, 
            text="¿Necesita ayuda? Contacte al administrador del sistema",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        )
        help_label.pack(side="left")
        
        # Configurar eventos de teclado
        self.email_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Enfocar el campo de email al inicio
        self.email_entry.focus()
    
    def login(self):
        """Maneja el inicio de sesión"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        # Validar campos
        if not email or not password:
            self.error_label.configure(text="Por favor, complete todos los campos")
            return
        
        # Intentar autenticar
        user, message = self.auth_controller.login(email, password)
        
        if user:
            # Autenticación exitosa, cambiar a la vista de dashboard
            self.switch_callback("dashboard", user)
        else:
            # Mostrar mensaje de error
            self.error_label.configure(text=message)
            # Limpiar campo de contraseña
            self.password_entry.delete(0, 'end')
    
    def destroy(self):
        """Destruye la vista actual"""
        super().destroy()
