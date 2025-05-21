import bcrypt

def hash_password(password):
    """Genera un hash seguro para la contraseña"""
    # Generar un salt aleatorio
    salt = bcrypt.gensalt()
    # Hashear la contraseña con el salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Devolver el hash como string
    return hashed.decode('utf-8')

def check_password(password, hashed_password):
    """Verifica si la contraseña coincide con el hash almacenado"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def sanitize_input(input_str):
    """Sanitiza la entrada para prevenir inyección SQL"""
    if input_str is None:
        return None
    # Eliminar caracteres potencialmente peligrosos
    sanitized = input_str.replace("'", "''")
    return sanitized
