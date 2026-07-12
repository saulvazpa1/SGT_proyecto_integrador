# DAO: Data Access Object
# producto_dao: Objeto de acceso a datos de la tabla productos

from database.conexion import Conexion
from models.producto import Producto

class ProductoDAO:

    # SELECT * FROM productos
    # SELECT * FROM vista_productos (Ajustado a sus 7 columnas reales)
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        # Llama a tu vista tal cual, sin complicaciones
        cursor.execute("SELECT * FROM vista_productos")
        registros = cursor.fetchall()
        
        productos = []
        for reg in registros:
            producto = Producto(
                producto_id=reg[0],            # producto_id
                producto_nombre=reg[1],        # articulo
                producto_categoria=reg[2],     # categoria
                producto_precio=reg[3],        # precio_venta
                producto_stock=reg[4],         # inventario_disponible
                producto_descripcion="",       # Se deja vacío porque tu vista no tiene descripción
                producto_unidad_medida=reg[5],  # unidad
                producto_color=reg[6]          # producto_color
            )
            productos.append(producto)

        cursor.close()
        conexion.close()
        return productos
    # Insertar un nuevo producto
    def insertar(self, producto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos(producto_id, producto_nombre, producto_categoria, producto_precio, producto_stock, producto_descripcion, producto_unidad_medida, producto_color)
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
                producto.producto_color
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar un producto existente
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
                producto.producto_id
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

    # Obtener el último ID para el auto-incremental manual
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(producto_id) FROM productos")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado and resultado[0] is not None:
            return resultado[0]
        return 0