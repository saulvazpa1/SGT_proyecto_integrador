#DAO: Data Access Object
#pedidos_dao: Objeto de acceso a datos de la tabla pedidos

from database.conexion import Conexion
from models.pedido import Pedido

class PedidosDAO:

    # SELECT * FROM pedidos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pedidos")
        registros = cursor.fetchall()

        pedidos = []
        for registro in registros:
            pedido = Pedido(
                registro[0],  # pedido_id
                registro[1],  # cliente_id
                registro[2],  # vendedor_id
                registro[3],  # producto_id
                registro[4],  # pedido_cantidad
                registro[5],  # pedido_total
                registro[6],  # pedido_estado
                registro[7],  # pedido_fecha
            )
            pedidos.append(pedido)

        cursor.close()
        conexion.close()
        return pedidos

    # Crear insertar
    def insertar(self, pedido):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO pedidos(
            pedido_id,
            cliente_id,
            vendedor_id,
            producto_id,
            pedido_cantidad,
            pedido_total,
            pedido_estado,
            pedido_fecha
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                pedido.pedido_id,
                pedido.cliente_id,
                pedido.vendedor_id,
                pedido.producto_id,
                pedido.pedido_cantidad,
                pedido.pedido_total,
                pedido.pedido_estado,
                pedido.pedido_fecha
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar
    def actualizar(self, pedido):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE pedidos
        SET cliente_id = %s,
            vendedor_id = %s,
            producto_id = %s,
            pedido_cantidad = %s,
            pedido_total = %s,
            pedido_estado = %s,
            pedido_fecha = %s
        WHERE pedido_id = %s
        """

        cursor.execute(
            sql,
            (
                pedido.cliente_id,
                pedido.vendedor_id,
                pedido.producto_id,
                pedido.pedido_cantidad,
                pedido.pedido_total,
                pedido.pedido_estado,
                pedido.pedido_fecha,
                pedido.pedido_id
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, pedido_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM pedidos WHERE pedido_id = %s",
            (pedido_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Obtener el último ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(pedido_id) FROM pedidos")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0

        return resultado[0]