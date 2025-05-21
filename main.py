import customtkinter as ctk
from views.login_view import LoginView
from models.database import Database
from database.database_creator import DatabaseCreator
from config import DB_CONFIG
import os

class App:
    def __init__(self):
        # Configurar tema de CustomTkinter
        ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Inicializar la base de datos si es necesario
        self.initialize_database()
        
        # Conectar a la base de datos
        self.db = Database()
        connection_success = self.db.connect()
        
        if not connection_success:
            print("✗ No se pudo conectar a la base de datos. Verifique la configuración.")
            return
        
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Gestión de Proyectos Académicos")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Centrar la ventana en la pantalla
        self.center_window()
        
        # Mostrar la vista de login
        self.current_view = None
        self.switch_view("login")
        
        # Iniciar el bucle principal
        self.root.mainloop()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def initialize_database(self):
        """Inicializa la base de datos si es necesario"""
        # Verificar si la base de datos ya existe
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = conn.cursor()
            
            # Verificar si la base de datos existe
            cursor.execute(f"SHOW DATABASES LIKE '{DB_CONFIG['database']}'")
            result = cursor.fetchone()
            
            if not result:
                print(f"✗ Base de datos '{DB_CONFIG['database']}' no encontrada. Creando...")
                # Crear la base de datos y las tablas
                creator = DatabaseCreator()
                success = creator.create_database()
                if success:
                    print("✓ Base de datos creada exitosamente")
                else:
                    print("✗ Error al crear la base de datos")
            else:
                print(f"✓ Base de datos '{DB_CONFIG['database']}' ya existe.")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"✗ Error al verificar la base de datos: {e}")
            print("Intentando crear la base de datos...")
            creator = DatabaseCreator()
            creator.create_database()
    
    def switch_view(self, view_name, user=None, project=None):
        """Cambia entre diferentes vistas de la aplicación"""
        # Destruir la vista actual si existe
        if self.current_view is not None:
            self.current_view.pack_forget()
            self.current_view.destroy()
            self.current_view = None
        
        # Limpiar todos los widgets hijos del root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cargar la nueva vista
        if view_name == "login":
            from views.login_view import LoginView
            self.current_view = LoginView(self.root, self.switch_view)
        elif view_name == "dashboard":
            from views.dashboard_view import DashboardView
            self.current_view = DashboardView(self.root, self.switch_view, user)
        elif view_name == "proyecto":
            from views.proyecto_view import ProyectoView
            self.current_view = ProyectoView(self.root, self.switch_view, user, project)
        elif view_name == "usuario":
            from views.usuario_view import UsuarioView
            self.current_view = UsuarioView(self.root, self.switch_view, user)

if __name__ == "__main__":
    app = App()
