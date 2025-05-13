import psycopg2
from datetime import datetime, timedelta
import random


# Funciones para generar datos aleatorios
def generar_proveedores(cantidad):
    return [
        (f"Proveedor {i}", f"proveedor{i}@correo.com", f"123456789{i}")
        for i in range(1, cantidad + 1)
    ]

def generar_trabajadores(cantidad):
    roles = ["Administrador", "Vendedor", "Gerente"]
    return [
        (f"Trabajador {i}", f"trabajador{i}@correo.com", random.choice(roles))
        for i in range(1, cantidad + 1)
    ]

def generar_categorias(cantidad):
    return [(f"Categoria {i}",) for i in range(1, cantidad + 1)]

def generar_productos(cantidad, categorias):
    return [
        (
            f"Producto {i}",
            f"Descripción del producto {i}",
            random.choice(categorias),
            random.randint(10, 100),
            random.choice(["kg", "litros", "unidades"]),
            random.randint(5, 20),
            random.randint(20, 100)
        )
        for i in range(1, cantidad + 1)
    ]

def generar_compras(cantidad, proveedores):
    return [
        (
            random.choice(proveedores),
            datetime.now() - timedelta(days=random.randint(0, 365)),
            random.randint(1000, 10000)
        )
        for _ in range(cantidad)
    ]

def generar_ventas(cantidad, trabajadores):
    return [
        (
            random.choice(trabajadores),
            random.randint(100, 10000),
            datetime.now() - timedelta(days=random.randint(0, 365))
        )
        for _ in range(cantidad)
    ]

# Funciones para insertar datos en las tablas
def insertar_proveedores(datos):
    cursor.executemany(
        'INSERT INTO "Proveedores" ("Nombre", "Correo", "Teléfono") VALUES (%s, %s, %s)',
        datos
    )
    conn.commit()

def insertar_trabajadores(datos):
    cursor.executemany(
        'INSERT INTO "Trabajadores" ("Nombre", "Correo", "Rol") VALUES (%s, %s, %s)',
        datos
    )
    conn.commit()

def insertar_categorias(datos):
    cursor.executemany(
        'INSERT INTO "Categoria" ("Nombre") VALUES (%s)',
        datos
    )
    conn.commit()

def insertar_productos(datos):
    cursor.executemany(
        'INSERT INTO "Productos" ("Nombre", "Descripcion", "FK_ID_Categoria", "Precio_Unidad", "Unidad_Medida", "Stock_Minimo", "Stock_Actual") VALUES (%s, %s, %s, %s, %s, %s, %s)',
        datos
    )
    conn.commit()

def insertar_compras(datos):
    cursor.executemany(
        'INSERT INTO "Compras" ("FK_ID_Proveedor", "Fecha", "Monto_Total") VALUES (%s, %s, %s)',
        datos
    )
    conn.commit()

def insertar_ventas(datos):
    cursor.executemany(
        'INSERT INTO "Ventas" ("FK_ID_Trabajador", "Monto_Total", "Fecha") VALUES (%s, %s, %s)',
        datos
    )
    conn.commit()


if __name__ == "__main__":

    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname="gestion_inventario",
        user="proyecto_bd",
        password="1234",
        host="localhost",
    )
    cursor = conn.cursor()

    # Llenar la base de datos con datos aleatorios
    print("Llenando la base de datos con datos aleatorios...")
    try:
        # Insertar Proveedores
        proveedores = generar_proveedores(10)
        insertar_proveedores(proveedores)

        # Insertar Trabajadores
        trabajadores = generar_trabajadores(10)
        insertar_trabajadores(trabajadores)

        # Insertar Categorías
        categorias = generar_categorias(5)
        insertar_categorias(categorias)

        # Obtener IDs de categorías para asignar a productos
        cursor.execute('SELECT "PK_ID_Categoria" FROM "Categoria"')
        categorias_ids = [row[0] for row in cursor.fetchall()]

        # Insertar Productos
        productos = generar_productos(20, categorias_ids)
        insertar_productos(productos)

        # Obtener IDs de proveedores para asignar a compras
        cursor.execute('SELECT "PK_ID_Proveedor" FROM "Proveedores"')
        proveedores_ids = [row[0] for row in cursor.fetchall()]

        # Insertar Compras
        compras = generar_compras(15, proveedores_ids)
        insertar_compras(compras)

        # Obtener IDs de trabajadores para asignar a ventas
        cursor.execute('SELECT "PK_ID_Trabajador" FROM "Trabajadores"')
        trabajadores_ids = [row[0] for row in cursor.fetchall()]

        # Insertar Ventas
        ventas = generar_ventas(20, trabajadores_ids)
        insertar_ventas(ventas)

        print("La base de datos ha sido llenada con datos aleatorios.")
    except Exception as e:
        print(f"Error, no se pudo llenar la base de datos\nDetalle: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()