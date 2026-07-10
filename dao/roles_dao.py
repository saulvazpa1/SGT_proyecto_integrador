# DAO: Data Access Object
# roles_dao: Objeto de acceso a datos de la tabla roles

from database.conexion import Conexion
from models.rol import Rol


class RolesDAO:

    # SELECT * FROM roles
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM roles")
        registros = cursor.fetchall()

        roles = []

        for registro in registros:
            rol = Rol(
                registro[0],  # rol_id
                registro[1],  # rol_nombre
                registro[2],  # rol_permisos
            )

            roles.append(rol)

        cursor.close()
        conexion.close()

        return roles

    # Crear insertar
    def insertar(self, rol):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO roles(rol_id, rol_nombre, rol_permisos)
        VALUES(%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                rol.rol_id,
                rol.rol_nombre,
                rol.rol_permisos
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar
    def actualizar(self, rol):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE roles
        SET rol_nombre = %s,
            rol_permisos = %s
        WHERE rol_id = %s
        """

        cursor.execute(
            sql,
            (
                rol.rol_nombre,
                rol.rol_permisos,
                rol.rol_id
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar
    def eliminar(self, rol_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM roles WHERE rol_id = %s",
            (rol_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    # Obtener último ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(rol_id) FROM roles")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0

        return resultado[0]