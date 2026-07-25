#DAO: Data Access Object
#pagos_dao: Objeto de acceso a datos de la tabla pagos

from database.conexion import Conexion
from models.pago import Pago

class PagosDAO:

    # SELECT * FROM pagos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pagos")
        registros = cursor.fetchall()

        pagos = []
        for registro in registros:
            pago = Pago(
                registro[0],  # pago_id
                registro[1],  # pedido_id
                registro[2],  # pago_monto
                registro[3],  # pago_fecha
                registro[4],  # pago_metodo
            )
            pagos.append(pago)

        cursor.close()
        conexion.close()
        return pagos

    # Crear insertar
    def insertar(self, pago):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO pagos(pago_id, pedido_id, pago_monto, pago_fecha, pago_metodo)
        VALUES(%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                pago.pago_id,
                pago.pedido_id,
                pago.pago_monto,
                pago.pago_fecha,
                pago.pago_metodo
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar
    def actualizar(self, pago):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE pagos
        SET pedido_id = %s,
            pago_monto = %s,
            pago_fecha = %s,
            pago_metodo = %s
        WHERE pago_id = %s
        """

        cursor.execute(
            sql,
            (
                pago.pedido_id,
                pago.pago_monto,
                pago.pago_fecha,
                pago.pago_metodo,
                pago.pago_id
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, pago_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM pagos WHERE pago_id = %s",
            (pago_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Obtener el último ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(pago_id) FROM pagos")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0

        return resultado[0]