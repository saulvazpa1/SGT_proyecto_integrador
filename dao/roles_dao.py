#DAO: Data Access Object
#cliente_dao: Objeto de acceso a datos de la tabla clientes

from database.conexion import Conexion
from models.cliente import Cliente

class RolesDAO:
    # SELECT * FROM clientes
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM roles")
        registros = cursor.fetchall()
        
        roles = []
        for registro in registros:
            roles = roles( 
                registro[0],  # rol_id
                registro[1],  # rol_nombre
                registro[2],  # rol_permisos
            )
            roles.append(roles)
            
        cursor.close()
        conexion.close()
        return roles

    # Crear insertar
    def insertar(self, roles):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO roles(rol_id, rol_nombre, rol_permisos)
        VALUES(%s, %s, %s)
        """
        cursor.execute(
            sql,
            (roles.rol_id,
             roles.rol_nombre,
             roles.rol_permisos,
             )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, roles):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE roles
        SET rol_nombre = %s, rol_permisos = %s,
        WHERE rol_id = %s
        """
        cursor.execute(
            sql,
            (roles.rol_nombre,
             roles.rol_permisos,
             roles.rol_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # eliminar un registro
    def eliminar(self, rol_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM clientes WHERE rol_id = %s",
            (rol_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()