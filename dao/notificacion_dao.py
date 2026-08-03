# DAO: Data Access Object
# notificacion_dao: Objeto de acceso a datos de la tabla notificaciones

from database.conexion import Conexion
from models.notificacion import Notificacion


class NotificacionDAO:

    def insertar(self, mensaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO notificaciones (mensaje) VALUES (%s)",
            (mensaje,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_recientes(self, limite=50):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT notificacion_id, mensaje, fecha_creacion, leida
            FROM notificaciones
            ORDER BY fecha_creacion DESC
            LIMIT %s
            """,
            (limite,)
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [Notificacion(*fila) for fila in filas]

    def contar_no_leidas(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM notificaciones WHERE leida = FALSE")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else 0

    def marcar_todas_leidas(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE notificaciones SET leida = TRUE WHERE leida = FALSE")
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, notificacion_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM notificaciones WHERE notificacion_id = %s",
            (notificacion_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_todas(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM notificaciones")
        conexion.commit()
        cursor.close()
        conexion.close()