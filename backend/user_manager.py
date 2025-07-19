import bcrypt
from database import Database

class UserManager:
    def __init__(self):
        self.db = Database()
    
    def _hash_password(self, password):
        """Generar hash de la contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password, hashed):
        """Verificar si la contraseña coincide con el hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_user(self, username, email, password):
        """Registrar un nuevo usuario"""
        if not self.db.connect():
            return False
        
        # Verificar si el usuario ya existe
        query_check = "SELECT id FROM usuarios WHERE username = %s OR email = %s"
        existing_user = self.db.fetch_one(query_check, (username, email))
        
        if existing_user:
            print(f"❌ El usuario '{username}' o email '{email}' ya existe")
            self.db.disconnect()
            return False
        
        # Hash de la contraseña
        hashed_password = self._hash_password(password)
        
        # Insertar nuevo usuario
        query_insert = """
        INSERT INTO usuarios (username, email, password) 
        VALUES (%s, %s, %s)
        """
        
        if self.db.execute_query(query_insert, (username, email, hashed_password)):
            print(f"✅ Usuario '{username}' registrado exitosamente")
            self.db.disconnect()
            return True
        else:
            print(f"❌ Error al registrar usuario '{username}'")
            self.db.disconnect()
            return False
    
    def login_user(self, username, password):
        """Autenticar usuario"""
        if not self.db.connect():
            return None
        
        # Buscar usuario
        query = "SELECT id, username, email, password FROM usuarios WHERE username = %s"
        user = self.db.fetch_one(query, (username,))
        
        if not user:
            print(f"❌ Usuario '{username}' no encontrado")
            self.db.disconnect()
            return None
        
        # Verificar contraseña
        if self._verify_password(password, user['password']):
            print(f"✅ Login exitoso para '{username}'")
            self.db.disconnect()
            # Retornar datos del usuario sin la contraseña
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        else:
            print(f"❌ Contraseña incorrecta para '{username}'")
            self.db.disconnect()
            return None
    
    def get_all_users(self):
        """Obtener todos los usuarios (sin contraseñas)"""
        if not self.db.connect():
            return []
        
        query = "SELECT id, username, email, created_at FROM usuarios ORDER BY created_at DESC"
        users = self.db.fetch_all(query)
        
        self.db.disconnect()
        return users
    
    def delete_user(self, username):
        """Eliminar un usuario"""
        if not self.db.connect():
            return False
        
        query = "DELETE FROM usuarios WHERE username = %s"
        
        if self.db.execute_query(query, (username,)):
            print(f"✅ Usuario '{username}' eliminado exitosamente")
            self.db.disconnect()
            return True
        else:
            print(f"❌ Error al eliminar usuario '{username}'")
            self.db.disconnect()
            return False
    
    def change_password(self, username, old_password, new_password):
        """Cambiar contraseña de un usuario"""
        if not self.db.connect():
            return False
        
        # Verificar usuario y contraseña actual
        query_verify = "SELECT password FROM usuarios WHERE username = %s"
        user = self.db.fetch_one(query_verify, (username,))
        
        if not user:
            print(f"❌ Usuario '{username}' no encontrado")
            self.db.disconnect()
            return False
        
        if not self._verify_password(old_password, user['password']):
            print(f"❌ Contraseña actual incorrecta para '{username}'")
            self.db.disconnect()
            return False
        
        # Actualizar contraseña
        new_hashed = self._hash_password(new_password)
        query_update = "UPDATE usuarios SET password = %s WHERE username = %s"
        
        if self.db.execute_query(query_update, (new_hashed, username)):
            print(f"✅ Contraseña cambiada exitosamente para '{username}'")
            self.db.disconnect()
            return True
        else:
            print(f"❌ Error al cambiar contraseña para '{username}'")
            self.db.disconnect()
            return False