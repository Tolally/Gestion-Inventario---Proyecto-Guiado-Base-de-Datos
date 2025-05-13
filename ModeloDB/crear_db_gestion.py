import psycopg2
from getpass import getpass
import os


def crear_sistema_restaurantes():
    '''
    Crea la base de datos 'sistema_restaurante' y luego a su usuario 'proyecto_bd' 
    junto con sus permisos.
    '''
    try:
        conn.set_session(autocommit=True)

        # Crear la base de datos
        cur.execute("CREATE DATABASE gestion_inventario;")

        # Crear el usuario para la base de datos
        cur.execute("CREATE USER proyecto_bd WITH PASSWORD '1234';")
        cur.execute("GRANT CONNECT ON DATABASE gestion_inventario TO proyecto_bd;")

        print("> Base de datos gestion_inventario creada")
        print("> Usuario creado exitosamente\nNombre: proyecto_bd\nContraseña: 1234")

        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="gestion_inventario",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        # Otorgar permisos a proyecto_bd
        cur_sr.execute("GRANT USAGE ON SCHEMA public TO proyecto_bd;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO proyecto_bd;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO proyecto_bd;")
        conn_sr.commit()
        print("> Permisos para proyecto_bd concedidos con éxito")

        # Cerrar conexión de postgres a sistema_restaurante
        cur_sr.close()
        conn_sr.close()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de gestion_inventario\nDetalle -> {e}")


def crear_esquema_bd():
    '''
    Crea el esquema de la base de datos de análisis del sistema de restaurantes\n
    Tener el archivo RestaurantDB.sql en la misma carpeta que este script python pls\n
    Link dbdiagram: https://dbdiagram.io/d/RestaurantDB-V2-0-6818e8e31ca52373f588d4c4
    '''
    script = True

    try:
        conn_sr = psycopg2.connect(
            database="gestion_inventario",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()
        print("> postgres conectado con éxito a gestion_inventario")
    except Exception as e:
        script = False
        print(f"# Error al conectar a gestion_inventario\nDetalle -> {e}")
    
    if script:
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
            sql_file_path = os.path.join(script_path, "Gestion_InventarioDB.sql")
            
            with open(sql_file_path, 'r', encoding="utf-8") as f:
                script_modelo = f.read()
            
            for statement in script_modelo.split(';'):
                stmt = statement.strip()
                if stmt:
                    cur_sr.execute(stmt + ';')

            conn_sr.commit()
            print("> Modelo de base de datos creado con éxito")

        except Exception as e:
            conn_sr.rollback()
            print(f"# Error con la creación del esquema\nDetalle -> {e}")
        
        cur_sr.close()
        conn_sr.close()



if __name__ == "__main__":
    # Conexión a postgres en ámbito global
    clave = getpass("Ingrese su contraseña del usuario postgres: ")
    try: 
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur = conn.cursor()
        print(f"> Conexión exitosa\nUser: {conn.info.user}\nBase de datos: {conn.info.dbname}")
        crear_sistema_restaurantes()
        crear_esquema_bd()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"# Fallo de conexión\nDetalle: {e}")