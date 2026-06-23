#DAO: Data Access Object
#pagos_dao: Objeto de acceso a datos de la tabla pagos

from database.conexion import Conexion
from models.pagos import Pagos

class PagosDAO:
    # SELECT * FROM pagos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pagos")
        registros = cursor.fetchall()
        
        pagos = []
        for registro in registros:
            pagos = Pagos(
                registro[0],  # pago_id
                registro[1],  # pedido_id
                registro[2],  # pago_monto
                registro[3],  # pago_fecha
                registro[4],  # pago_metodo
            )
            pagos.append(pagos)
            
        cursor.close()
        conexion.close()
        return pagos

    # Crear insertar
    def insertar(self, pagos):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO pagos(pago_id, pedido_id, pago_monto, pago_fecha, pago_metodo)
        VALUES(%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (pagos.pago_id,
             pagos.pedido_id,
             pagos.pago_monto,
             pagos.pago_fecha,
             pagos.pago_metodo
             )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, pagos):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE pagos
        SET pedido_id = %s, pago_monto = %s, pago_fecha = %s,
            pago_metodo = %s
        WHERE pago_id = %s
        """
        cursor.execute(
            sql,
            (pagos.pedido_id,
             pagos.pago_monto,
             pagos.pago_fecha,
             pagos.pago_metodo,
             pagos.pago_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # eliminar un registro
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