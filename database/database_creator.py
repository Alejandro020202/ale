import mysql.connector
from mysql.connector import Error
import os
import bcrypt
from config import DB_CONFIG
import random
from datetime import datetime, timedelta

class DatabaseCreator:
    def __init__(self, host=None, user=None, password=None):
        self.host = host or DB_CONFIG['host']
        self.user = user or DB_CONFIG['user']
        self.password = password or DB_CONFIG['password']
        self.database_name = DB_CONFIG['database']
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con MySQL sin seleccionar una base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("✓ Conexión a MySQL establecida")
            return True
        except Error as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            return False
    
    def create_database(self):
        """Crea la base de datos y todas sus tablas"""
        try:
            if not self.connect():
                return False
            
            # Crear la base de datos si no existe
            self.cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
            self.cursor.execute(f"CREATE DATABASE {self.database_name}")
            print(f"✓ Base de datos '{self.database_name}' creada")
            
            # Usar la base de datos
            self.cursor.execute(f"USE {self.database_name}")
            print(f"✓ Usando base de datos '{self.database_name}'")
            
            # Crear todas las tablas
            self._create_tables()
            
            # Insertar datos iniciales
            self._insert_initial_data()
            
            print("✓ Base de datos configurada exitosamente")
            return True
            
        except Error as e:
            print(f"✗ Error al configurar la base de datos: {e}")
            return False
        finally:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("✓ Conexión a MySQL cerrada")
    
    def _create_tables(self):
        """Crea todas las tablas necesarias para el sistema"""
        tables = [
            """
            CREATE TABLE Usuarias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                rol ENUM('Directora', 'Coordinadora', 'Profesora_Administradora', 'Profesora_Encargada') NOT NULL,
                materia_asignada VARCHAR(100),
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE Proyectos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(150) NOT NULL,
                descripcion TEXT NOT NULL,
                materia VARCHAR(100) NOT NULL,
                profesora_id INT NOT NULL,
                estado ENUM('Pendiente', 'Aprobado', 'Rechazado') NOT NULL DEFAULT 'Pendiente',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profesora_id) REFERENCES Usuarias(id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE Participantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                proyecto_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                cedula VARCHAR(20) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id) ON DELETE CASCADE,
                UNIQUE KEY unique_cedula (cedula)
            )
            """,
            """
            CREATE TABLE Aprobaciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                proyecto_id INT NOT NULL,
                usuaria_id INT NOT NULL,
                rol_aprobador VARCHAR(50) NOT NULL,
                fecha_aprobacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id) ON DELETE CASCADE,
                FOREIGN KEY (usuaria_id) REFERENCES Usuarias(id) ON DELETE CASCADE,
                UNIQUE KEY unique_aprobacion (proyecto_id, usuaria_id)
            )
            """
        ]
        
        print("\nCreando tablas...")
        for i, table in enumerate(tables, 1):
            try:
                self.cursor.execute(table)
                print(f"✓ Tabla {i} creada exitosamente")
            except Error as e:
                print(f"✗ Error al crear tabla {i}: {e}")
                raise
        
        # Crear procedimientos almacenados
        self._create_stored_procedures()
    
    def _create_stored_procedures(self):
        """Crea los procedimientos almacenados necesarios"""
        procedures = [
            """
            CREATE PROCEDURE aprobar_proyecto(
                IN p_proyecto_id INT,
                IN p_usuaria_id INT,
                IN p_rol_aprobador VARCHAR(50),
                OUT p_resultado BOOLEAN,
                OUT p_mensaje VARCHAR(255)
            )
            BEGIN
                DECLARE v_count INT;
                DECLARE v_encargada INT;
                DECLARE v_administradora INT;
                DECLARE v_coordinadora INT;
                DECLARE v_roles_faltantes VARCHAR(255);
                
                -- Verificar si ya aprobó el proyecto
                SELECT COUNT(*) INTO v_count FROM Aprobaciones 
                WHERE proyecto_id = p_proyecto_id AND usuaria_id = p_usuaria_id;
                
                IF v_count > 0 THEN
                    SET p_resultado = FALSE;
                    SET p_mensaje = 'Ya has aprobado este proyecto';
                ELSE
                    -- Añadir la aprobación
                    INSERT INTO Aprobaciones (proyecto_id, usuaria_id, rol_aprobador)
                    VALUES (p_proyecto_id, p_usuaria_id, p_rol_aprobador);
                    
                    -- Contar aprobaciones por rol
                    SELECT 
                        SUM(CASE WHEN rol_aprobador = 'Profesora_Encargada' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN rol_aprobador = 'Profesora_Administradora' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN rol_aprobador = 'Coordinadora' THEN 1 ELSE 0 END)
                    INTO v_encargada, v_administradora, v_coordinadora
                    FROM Aprobaciones 
                    WHERE proyecto_id = p_proyecto_id;
                    
                    -- Inicializar roles faltantes
                    SET v_roles_faltantes = '';
                    
                    -- Verificar roles faltantes
                    IF v_encargada = 0 THEN
                        SET v_roles_faltantes = CONCAT(v_roles_faltantes, 'Profesora Encargada, ');
                    END IF;
                    
                    IF v_administradora = 0 THEN
                        SET v_roles_faltantes = CONCAT(v_roles_faltantes, 'Profesora Administradora, ');
                    END IF;
                    
                    IF v_coordinadora = 0 THEN
                        SET v_roles_faltantes = CONCAT(v_roles_faltantes, 'Coordinadora, ');
                    END IF;
                    
                    -- Eliminar la última coma si hay roles faltantes
                    IF LENGTH(v_roles_faltantes) > 0 THEN
                        SET v_roles_faltantes = LEFT(v_roles_faltantes, LENGTH(v_roles_faltantes) - 2);
                    END IF;
                    
                    -- Verificar si ya tiene todas las aprobaciones necesarias
                    IF v_encargada > 0 AND v_administradora > 0 AND v_coordinadora > 0 THEN
                        -- Actualizar el estado del proyecto a "Aprobado"
                        UPDATE Proyectos SET estado = 'Aprobado'
                        WHERE id = p_proyecto_id;
                        
                        SET p_resultado = TRUE;
                        SET p_mensaje = 'Proyecto aprobado completamente. Todas las aprobaciones requeridas han sido obtenidas.';
                    ELSE
                        SET p_resultado = TRUE;
                        SET p_mensaje = CONCAT('Aprobación registrada. Aún se requiere la aprobación de: ', v_roles_faltantes, '.');
                    END IF;
                END IF;
            END
            """,
            """
            CREATE PROCEDURE obtener_proyectos_por_profesora(
                IN p_profesora_id INT
            )
            BEGIN
                SELECT * FROM Proyectos 
                WHERE profesora_id = p_profesora_id;
            END
            """,
            """
            CREATE PROCEDURE obtener_proyectos_con_profesora(
            )
            BEGIN
                SELECT p.*, u.nombre as profesora_nombre 
                FROM Proyectos p
                JOIN Usuarias u ON p.profesora_id = u.id;
            END
            """,
            """
            CREATE PROCEDURE verificar_participante_duplicado(
                IN p_cedula VARCHAR(20),
                IN p_exclude_proyecto_id INT,
                OUT p_existe BOOLEAN,
                OUT p_proyecto_nombre VARCHAR(150),
                OUT p_participante_nombre VARCHAR(100)
            )
            BEGIN
                DECLARE v_count INT;
                DECLARE v_proyecto_id INT;
                
                IF p_exclude_proyecto_id IS NULL THEN
                    -- Verificar si existe en cualquier proyecto
                    SELECT COUNT(*), proyecto_id INTO v_count, v_proyecto_id
                    FROM Participantes
                    WHERE cedula = p_cedula
                    LIMIT 1;
                ELSE
                    -- Verificar si existe en otro proyecto diferente al excluido
                    SELECT COUNT(*), proyecto_id INTO v_count, v_proyecto_id
                    FROM Participantes
                    WHERE cedula = p_cedula AND proyecto_id != p_exclude_proyecto_id
                    LIMIT 1;
                END IF;
                
                IF v_count > 0 THEN
                    -- Obtener información del proyecto y participante
                    SELECT p.nombre, part.nombre 
                    INTO p_proyecto_nombre, p_participante_nombre
                    FROM Proyectos p
                    JOIN Participantes part ON part.proyecto_id = p.id
                    WHERE part.cedula = p_cedula
                    LIMIT 1;
                    
                    SET p_existe = TRUE;
                ELSE
                    SET p_existe = FALSE;
                    SET p_proyecto_nombre = NULL;
                    SET p_participante_nombre = NULL;
                END IF;
            END
            """
        ]
        
        print("\nCreando procedimientos almacenados...")
        for i, procedure in enumerate(procedures, 1):
            try:
                self.cursor.execute(procedure)
                print(f"✓ Procedimiento {i} creado exitosamente")
            except Error as e:
                print(f"✗ Error al crear procedimiento {i}: {e}")
                raise
    
    def _hash_password(self, password):
        """Genera un hash seguro para la contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _insert_initial_data(self):
        """Inserta datos iniciales en la base de datos"""
        print("\nInsertando datos iniciales...")
        
        try:
            # Insertar usuarios con diferentes roles
            usuarios = [
                ("Administrador", "admin@example.com", self._hash_password("admin123"), "Profesora_Administradora", "Administración"),
                ("Directora", "directora@example.com", self._hash_password("directora123"), "Directora", "Dirección"),
                ("Coordinadora", "coordinadora@example.com", self._hash_password("coordinadora123"), "Coordinadora", "Coordinación"),
                ("Profesora 1", "profesora1@example.com", self._hash_password("profesora123"), "Profesora_Encargada", "Matemáticas"),
                ("Profesora 2", "profesora2@example.com", self._hash_password("profesora123"), "Profesora_Encargada", "Física"),
                ("Profesora 3", "profesora3@example.com", self._hash_password("profesora123"), "Profesora_Encargada", "Química"),
                ("Profesora 4", "profesora4@example.com", self._hash_password("profesora123"), "Profesora_Encargada", "Biología"),
                ("Profesora 5", "profesora5@example.com", self._hash_password("profesora123"), "Profesora_Encargada", "Informática")
            ]
            
            print("Insertando usuarios...")
            user_ids = {}
            for usuario in usuarios:
                query = """
                INSERT INTO Usuarias (nombre, email, password_hash, rol, materia_asignada) 
                VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, usuario)
                user_id = self.cursor.lastrowid
                user_ids[usuario[1]] = user_id  # Guardar ID por email
            
            self.connection.commit()
            print(f"✓ {len(usuarios)} usuarios insertados")
            
            # Lista de profesoras encargadas
            profesoras = [
                user_ids["profesora1@example.com"],
                user_ids["profesora2@example.com"],
                user_ids["profesora3@example.com"],
                user_ids["profesora4@example.com"],
                user_ids["profesora5@example.com"]
            ]
            
            # Datos para generar proyectos aleatorios
            materias = ["Matemáticas", "Física", "Química", "Biología", "Informática", "Historia", "Literatura", "Inglés", "Educación Física", "Arte"]
            
            nombres_proyectos = [
                "Sistema de Gestión Académica", "Aplicación Móvil Educativa", "Plataforma de Aprendizaje Virtual",
                "Laboratorio Virtual", "Simulador de Experimentos", "Herramienta de Análisis de Datos",
                "Juego Educativo", "Asistente Virtual para Estudiantes", "Sistema de Evaluación Automática",
                "Biblioteca Digital", "Plataforma de Colaboración", "Herramienta de Visualización",
                "Sistema de Tutoría Inteligente", "Aplicación de Realidad Aumentada", "Plataforma de Cursos Online",
                "Sistema de Gestión de Proyectos", "Plataforma de Comunicación Educativa", "Herramienta de Diseño Gráfico",
                "Aplicación de Robótica Educativa", "Sistema de Monitoreo de Aprendizaje", "Plataforma de Gamificación",
                "Herramienta de Programación Visual", "Aplicación de Educación Inclusiva", "Sistema de Gestión de Contenidos",
                "Plataforma de Evaluación por Competencias", "Herramienta de Análisis Estadístico", "Aplicación de Educación Ambiental"
            ]
            
            descripciones = [
                "Este proyecto tiene como objetivo desarrollar una solución innovadora que permita mejorar el proceso de enseñanza-aprendizaje mediante el uso de tecnologías de la información.",
                "La propuesta busca crear una herramienta que facilite la adquisición de conocimientos y habilidades en los estudiantes, promoviendo la autonomía y el pensamiento crítico.",
                "Este sistema permitirá a los docentes realizar un seguimiento personalizado del progreso de cada estudiante, identificando áreas de mejora y fortalezas.",
                "La plataforma integrará diferentes recursos multimedia y actividades interactivas para enriquecer la experiencia educativa y motivar a los estudiantes.",
                "Este proyecto implementará metodologías activas de aprendizaje, fomentando la participación y el trabajo colaborativo entre los estudiantes.",
                "La herramienta incorporará elementos de gamificación para aumentar la motivación y el compromiso de los estudiantes con su proceso de aprendizaje.",
                "Este sistema utilizará inteligencia artificial para adaptar los contenidos y actividades al ritmo y estilo de aprendizaje de cada estudiante.",
                "La plataforma facilitará la comunicación entre docentes, estudiantes y padres de familia, creando una comunidad educativa más integrada y participativa.",
                "Este proyecto implementará estrategias de evaluación formativa que permitirán identificar y corregir errores en tiempo real, mejorando el rendimiento académico.",
                "La herramienta promoverá el desarrollo de competencias digitales en los estudiantes, preparándolos para los desafíos del siglo XXI."
            ]
            
            # Generar nombres y cédulas únicos para participantes
            participantes = []
            for i in range(1, 200):  # Generar 200 participantes
                nombre = f"Estudiante {i}"
                cedula = f"{random.randint(1000000, 9999999)}"
                participantes.append((nombre, cedula))
            
            # Generar 15 proyectos para cada profesora
            print("Generando proyectos para cada profesora...")
            all_proyecto_ids = []
            
            for profesora_id in profesoras:
                for i in range(15):
                    # Generar datos aleatorios para el proyecto
                    nombre = random.choice(nombres_proyectos) + f" {i+1}"
                    descripcion = random.choice(descripciones)
                    materia = random.choice(materias)
                    
                    # Estado aleatorio con mayor probabilidad de "Pendiente"
                    estado = random.choices(
                        ["Pendiente", "Aprobado", "Rechazado"], 
                        weights=[0.6, 0.3, 0.1], 
                        k=1
                    )[0]
                    
                    # Fecha de creación aleatoria en los últimos 6 meses
                    dias_atras = random.randint(1, 180)
                    fecha_creacion = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Insertar proyecto
                    query = """
                    INSERT INTO Proyectos (nombre, descripcion, materia, profesora_id, estado, fecha_creacion) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(query, (nombre, descripcion, materia, profesora_id, estado, fecha_creacion))
                    proyecto_id = self.cursor.lastrowid
                    all_proyecto_ids.append(proyecto_id)
                    
                    # Generar entre 2 y 5 participantes para el proyecto
                    num_participantes = random.randint(2, 5)
                    participantes_seleccionados = random.sample(participantes, num_participantes)
                    
                    for nombre_participante, cedula in participantes_seleccionados:
                        try:
                            # Insertar participante
                            query = """
                            INSERT INTO Participantes (proyecto_id, nombre, cedula) 
                            VALUES (%s, %s, %s)
                            """
                            self.cursor.execute(query, (proyecto_id, nombre_participante, cedula))
                        except Error as e:
                            # Si hay error por duplicado, ignorar y continuar
                            if "Duplicate entry" in str(e):
                                print(f"Participante con cédula {cedula} ya existe, omitiendo...")
                                continue
                            else:
                                raise
                    
                    # Si el proyecto está aprobado, generar aprobaciones
                    if estado == "Aprobado":
                        # Seleccionar aprobadores específicos para los roles requeridos
                        aprobadores = [
                            (user_ids["profesora1@example.com"], "Profesora_Encargada"),  # Una profesora encargada
                            (user_ids["admin@example.com"], "Profesora_Administradora"),  # La administradora
                            (user_ids["coordinadora@example.com"], "Coordinadora")  # La coordinadora
                        ]
                        
                        # Insertar aprobaciones
                        for aprobador_id, rol in aprobadores:
                            # Fecha de aprobación aleatoria después de la creación del proyecto
                            dias_despues = random.randint(1, min(30, dias_atras))
                            fecha_aprobacion = (datetime.now() - timedelta(days=dias_atras-dias_despues)).strftime('%Y-%m-%d %H:%M:%S')
                            
                            query = """
                            INSERT INTO Aprobaciones (proyecto_id, usuaria_id, rol_aprobador, fecha_aprobacion) 
                            VALUES (%s, %s, %s, %s)
                            """
                            self.cursor.execute(query, (proyecto_id, aprobador_id, rol, fecha_aprobacion))
            
            self.connection.commit()
            print(f"✓ {len(profesoras) * 15} proyectos generados con sus participantes y aprobaciones")
            
            print("\n✓ Todos los datos iniciales fueron insertados correctamente")
            
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error al insertar datos iniciales: {e}")
            raise
