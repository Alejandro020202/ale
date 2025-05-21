# Sistema de Gestión de Proyectos Académicos

Este sistema permite gestionar proyectos académicos, incluyendo la creación, edición y aprobación de proyectos, así como la gestión de usuarios.

## Requisitos

- Python 3.7 o superior
- MySQL 5.7 o superior
- Bibliotecas Python:
  - customtkinter
  - mysql-connector-python
  - bcrypt

## Instalación

1. Clonar o descargar este repositorio
2. Instalar las dependencias:
   \`\`\`
   pip install customtkinter mysql-connector-python bcrypt
   \`\`\`
3. Configurar la conexión a la base de datos en `config.py`
4. Ejecutar el script de inicialización de la base de datos:
   \`\`\`
   python database/db_initializer.py [host] [usuario] [contraseña]
   \`\`\`
   O simplemente ejecutar la aplicación, que inicializará la base de datos automáticamente.

## Ejecución

\`\`\`
python main.py
\`\`\`

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `config.py`: Configuración de la base de datos
- `database/`: Scripts y utilidades para la base de datos
  - `create_database.sql`: Script SQL para crear la base de datos y tablas
  - `db_initializer.py`: Inicializador de la base de datos
- `models/`: Modelos de datos
- `views/`: Interfaces de usuario
- `controllers/`: Lógica de negocio
- `utils/`: Utilidades varias

## Usuarios por Defecto

El sistema crea un usuario administrador por defecto:

- Email: admin@example.com
- Contraseña: admin123
- Rol: Profesora Administradora

## Roles de Usuario

- **Directora**: Puede aprobar proyectos
- **Coordinadora**: Puede aprobar proyectos
- **Profesora Administradora**: Puede gestionar usuarios y aprobar proyectos
- **Profesora Encargada**: Puede crear y editar proyectos

## Flujo de Aprobación de Proyectos

Un proyecto necesita 3 aprobaciones para cambiar su estado a "Aprobado". Las aprobaciones pueden venir de usuarios con roles de Directora, Coordinadora o Profesora Administradora.
