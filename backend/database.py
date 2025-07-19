import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.connection = None
    
    def connect(self):
        """Conectar a la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("✅ Conexión exitosa a MySQL")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error de conexión: {err}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Desconectado de MySQL")
    
    def execute_query(self, query, params=None):
        """Ejecutar una consulta (INSERT, UPDATE, DELETE)"""
        if not self.connection or not self.connection.is_connected():
            print("❌ No hay conexión a la base de datos")
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error en consulta: {err}")
            return False
    
    def fetch_one(self, query, params=None):
        """Ejecutar una consulta SELECT y obtener un resultado"""
        if not self.connection or not self.connection.is_connected():
            print("❌ No hay conexión a la base de datos")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"❌ Error en consulta: {err}")
            return None
    
    def fetch_all(self, query, params=None):
        """Ejecutar una consulta SELECT y obtener todos los resultados"""
        if not self.connection or not self.connection.is_connected():
            print("❌ No hay conexión a la base de datos")
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            print(f"❌ Error en consulta: {err}")
            return []