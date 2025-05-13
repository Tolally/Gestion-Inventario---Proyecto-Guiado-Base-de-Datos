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

def generar_productos_comprados(cantidad, compras, productos):
    return [
        (
            random.choice(compras),
            random.choice(productos),
            random.randint(1, 10),  # Cantidad
            random.randint(10, 100)  # Precio por unidad
        )
        for _ in range(cantidad)
    ]

def generar_productos_vendidos(cantidad, ventas, productos):
    return [
        (
            random.choice(ventas),
            random.choice(productos),
            random.randint(1, 10),  # Cantidad
            random.randint(10, 100)  # Precio por unidad
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

def insertar_productos_comprados(datos):
    cursor.executemany(
        'INSERT INTO "Productos_Comprados" ("FK_ID_Compras", "FK_ID_Catalogo", "Cantidad", "Precio_Unidad") VALUES (%s, %s, %s, %s)',
        datos
    )
    conn.commit()

def insertar_productos_vendidos(datos):
    cursor.executemany(
        'INSERT INTO "Productos_Vendidos" ("FK_ID_Ventas", "FK_ID_Productos", "Cantidad", "Precio_Unidad") VALUES (%s, %s, %s, %s)',
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
        compras = []
        for _ in range(15):

            proveedor_id = random.choice(proveedores_ids)
            fecha = datetime.now() - timedelta(days=random.randint(0, 365))
            cursor.execute('SELECT "PK_ID_Productos", "Precio_Unidad" FROM "Productos"')
            productos_disponibles = cursor.fetchall()
            productos_comprados = []
            monto_total = 0

            for _ in range(random.randint(1, 5)):  # Productos por compra
                producto_id, precio_unidad = random.choice(productos_disponibles)
                cantidad = random.randint(1, 10)
                productos_comprados.append((producto_id, cantidad, precio_unidad))
                monto_total += cantidad * precio_unidad

            cursor.execute(
                'INSERT INTO "Compras" ("FK_ID_Proveedor", "Fecha", "Monto_Total") VALUES (%s, %s, %s) RETURNING "PK_ID_Compras"',
                (proveedor_id, fecha, monto_total)
            )

            compra_id = cursor.fetchone()[0]
            compras.append(compra_id)

            for producto_id, cantidad, precio_unidad in productos_comprados:
                cursor.execute(
                    'INSERT INTO "Productos_Comprados" ("FK_ID_Compras", "FK_ID_Catalogo", "Cantidad", "Precio_Unidad") VALUES (%s, %s, %s, %s)',
                    (compra_id, producto_id, cantidad, precio_unidad)
                )

        # Insertar Ventas
        cursor.execute('SELECT "PK_ID_Trabajador" FROM "Trabajadores"')
        trabajadores_ids = [row[0] for row in cursor.fetchall()]
        ventas = []

        for _ in range(20):
            trabajador_id = random.choice(trabajadores_ids)
            fecha = datetime.now() - timedelta(days=random.randint(0, 365))
            cursor.execute('SELECT "PK_ID_Productos", "Precio_Unidad" FROM "Productos"')
            productos_disponibles = cursor.fetchall()
            productos_vendidos = []
            monto_total = 0

            for _ in range(random.randint(1, 5)):  # Productos por venta
                producto_id, precio_unidad = random.choice(productos_disponibles)
                cantidad = random.randint(1, 10)
                productos_vendidos.append((producto_id, cantidad, precio_unidad))
                monto_total += cantidad * precio_unidad

            cursor.execute(
                'INSERT INTO "Ventas" ("FK_ID_Trabajador", "Monto_Total", "Fecha") VALUES (%s, %s, %s) RETURNING "PK_ID_Ventas"',
                (trabajador_id, monto_total, fecha)
            )

            venta_id = cursor.fetchone()[0]
            ventas.append(venta_id)

            for producto_id, cantidad, precio_unidad in productos_vendidos:
                cursor.execute(
                    'INSERT INTO "Productos_Vendidos" ("FK_ID_Ventas", "FK_ID_Productos", "Cantidad", "Precio_Unidad") VALUES (%s, %s, %s, %s)',
                    (venta_id, producto_id, cantidad, precio_unidad)
                )

        conn.commit()
        print("La base de datos ha sido llenada con datos aleatorios.")
    except Exception as e:
        print(f"Error, no se pudo llenar la base de datos\nDetalle: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()