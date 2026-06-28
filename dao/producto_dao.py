# DAO: Data Access Object
# producto_dao: Objeto de acceso a datos de la tabla productos

from database.conexion import Conexion
from models.producto import Producto


class ProductoDAO:

    # SELECT * FROM productos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        registros = cursor.fetchall()

        productos = []
        for registro in registros:
            producto = Producto(
                registro[0],  # producto_id
                registro[1],  # producto_nombre
                registro[2],  # producto_categoria
                registro[3],  # producto_precio
                registro[4],  # producto_stock
                registro[5],  # producto_descripcion
                registro[6],  # producto_unidad_medida
                registro[7],  # producto_color
            )
            productos.append(producto)

        cursor.close()
        conexion.close()
        return productos

    # Crear insertar
    def insertar(self, producto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos(
            producto_id,
            producto_nombre,
            producto_categoria,
            producto_precio,
            producto_stock,
            producto_descripcion,
            producto_unidad_medida,
            producto_color
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                producto.producto_id,
                producto.producto_nombre,
                producto.producto_categoria,
                producto.producto_precio,
                producto.producto_stock,
                producto.producto_descripcion,
                producto.producto_unidad_medida,
                producto.producto_color,
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar
    def actualizar(self, producto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE productos
        SET producto_nombre = %s,
            producto_categoria = %s,
            producto_precio = %s,
            producto_stock = %s,
            producto_descripcion = %s,
            producto_unidad_medida = %s,
            producto_color = %s
        WHERE producto_id = %s
        """

        cursor.execute(
            sql,
            (
                producto.producto_nombre,
                producto.producto_categoria,
                producto.producto_precio,
                producto.producto_stock,
                producto.producto_descripcion,
                producto.producto_unidad_medida,
                producto.producto_color,
                producto.producto_id,
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, producto_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM productos WHERE producto_id = %s",
            (producto_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Obtener el último ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(producto_id) FROM productos")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0

        return resultado[0]