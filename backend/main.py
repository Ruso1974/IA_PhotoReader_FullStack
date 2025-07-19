#!/usr/bin/env python3
"""
Aplicación de Gestión de Usuarios con MySQL
Autor: Pablo
Fecha: Julio 2025
"""

from user_manager import UserManager
import getpass

def mostrar_menu():
    """Mostrar el menú principal"""
    print("\n" + "="*50)
    print("🔐 GESTIÓN DE USUARIOS - MySQL")
    print("="*50)
    print("1. 📝 Registrar nuevo usuario")
    print("2. 🔑 Iniciar sesión")
    print("3. 👥 Ver todos los usuarios")
    print("4. 🗑️  Eliminar usuario")
    print("5. 🔒 Cambiar contraseña")
    print("6. ❌ Salir")
    print("="*50)

def registrar_usuario(user_manager):
    """Registrar un nuevo usuario"""
    print("\n📝 REGISTRO DE USUARIO")
    print("-" * 30)
    
    username = input("👤 Username: ").strip()
    email = input("📧 Email: ").strip()
    password = getpass.getpass("🔐 Contraseña: ")
    
    if not username or not email or not password:
        print("❌ Todos los campos son obligatorios")
        return
    
    user_manager.register_user(username, email, password)

def login_usuario(user_manager):
    """Iniciar sesión"""
    print("\n🔑 INICIAR SESIÓN")
    print("-" * 20)
    
    username = input("👤 Username: ").strip()
    password = getpass.getpass("🔐 Contraseña: ")
    
    if not username or not password:
        print("❌ Username y contraseña son obligatorios")
        return None
    
    user = user_manager.login_user(username, password)
    
    if user:
        print(f"\n🎉 ¡Bienvenido {user['username']}!")
        print(f"📧 Email: {user['email']}")
        print(f"🆔 ID: {user['id']}")
    
    return user

def ver_usuarios(user_manager):
    """Ver todos los usuarios"""
    print("\n👥 LISTA DE USUARIOS")
    print("-" * 30)
    
    users = user_manager.get_all_users()
    
    if not users:
        print("📭 No hay usuarios registrados")
        return
    
    print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Fecha Registro':<20}")
    print("-" * 70)
    
    for user in users:
        created_at = user['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        print(f"{user['id']:<5} {user['username']:<15} {user['email']:<25} {created_at:<20}")

def eliminar_usuario(user_manager):
    """Eliminar un usuario"""
    print("\n🗑️  ELIMINAR USUARIO")
    print("-" * 20)
    
    username = input("👤 Username a eliminar: ").strip()
    
    if not username:
        print("❌ Username es obligatorio")
        return
    
    confirmacion = input(f"⚠️  ¿Estás seguro de eliminar '{username}'? (sí/no): ").strip().lower()
    
    if confirmacion in ['sí', 'si', 's', 'yes', 'y']:
        user_manager.delete_user(username)
    else:
        print("❌ Eliminación cancelada")

def cambiar_password(user_manager):
    """Cambiar contraseña"""
    print("\n🔒 CAMBIAR CONTRASEÑA")
    print("-" * 25)
    
    username = input("👤 Username: ").strip()
    old_password = getpass.getpass("🔐 Contraseña actual: ")
    new_password = getpass.getpass("🔐 Nueva contraseña: ")
    confirm_password = getpass.getpass("🔐 Confirmar nueva contraseña: ")
    
    if not all([username, old_password, new_password, confirm_password]):
        print("❌ Todos los campos son obligatorios")
        return
    
    if new_password != confirm_password:
        print("❌ Las contraseñas nuevas no coinciden")
        return
    
    user_manager.change_password(username, old_password, new_password)

def main():
    """Función principal"""
    print("🚀 Inicializando aplicación...")
    user_manager = UserManager()
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Selecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                registrar_usuario(user_manager)
            elif opcion == "2":
                login_usuario(user_manager)
            elif opcion == "3":
                ver_usuarios(user_manager)
            elif opcion == "4":
                eliminar_usuario(user_manager)
            elif opcion == "5":
                cambiar_password(user_manager)
            elif opcion == "6":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()