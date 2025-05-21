-- Script para la creación de la base de datos y tablas
-- Sistema de Gestión de Proyectos Académicos

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS proyectos_academicos;

-- Usar la base de datos
USE proyectos_academicos;

-- Tabla de Usuarias (profesoras, directoras, coordinadoras, etc.)
CREATE TABLE IF NOT EXISTS Usuarias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('Directora', 'Coordinadora', 'Profesora_Administradora', 'Profesora_Encargada') NOT NULL,
    materia_asignada VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Proyectos
CREATE TABLE IF NOT EXISTS Proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    materia VARCHAR(100) NOT NULL,
    profesora_id INT NOT NULL,
    estado ENUM('Pendiente', 'Aprobado', 'Rechazado') NOT NULL DEFAULT 'Pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profesora_id) REFERENCES Usuarias(id) ON DELETE CASCADE
);

-- Tabla de Participantes (estudiantes que participan en los proyectos)
CREATE TABLE IF NOT EXISTS Participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proyecto_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id) ON DELETE CASCADE
);

-- Tabla de Aprobaciones (registro de aprobaciones de proyectos)
CREATE TABLE IF NOT EXISTS Aprobaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proyecto_id INT NOT NULL,
    usuaria_id INT NOT NULL,
    rol_aprobador VARCHAR(50) NOT NULL,
    fecha_aprobacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuaria_id) REFERENCES Usuarias(id) ON DELETE CASCADE,
    UNIQUE KEY unique_aprobacion (proyecto_id, usuaria_id)
);

-- Insertar usuario administrador por defecto
-- Contraseña: admin123 (hash generado con bcrypt)
INSERT INTO Usuarias (nombre, email, password_hash, rol, materia_asignada)
VALUES (
    'Administrador', 
    'admin@example.com', 
    '$2b$12$tGpRxMfWD5G8mxFJx4u9UOzBaEbR0KgYsM1sDiq.TQTmT5JxoZhK2', 
    'Profesora_Administradora', 
    'Administración'
) ON DUPLICATE KEY UPDATE id = id;
