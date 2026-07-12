# DAO: Data Access Object
# rol_dao: Objeto de acceso a datos de la tabla roles

from database.conexion import Conexion    # Carpeta/archivo/clase 
from models.rol import Rol

class RolDAO:
# SELECT * FROM roles
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        # objeto para postgresql 
        cursor = conexion.cursor()
        # que comando ejecutar

        cursor.execute("SELECT * FROM roles")
        registros = cursor.fetchall() # nombre de la tabla/el resultado de cursor fetchall
        
        roles = [] # lista vacia
        for registro in registros:  # crea un nuevo rol con nueva info
            rol = Rol(
                rol_id=registro[0],
                rol_nombre=registro[1],
                rol_permisos=registro[2]
            )
            roles.append(rol)

        cursor.close()
        conexion.close()
        return roles
    # Crear insertar

    def insertar(self, rol):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # Conexion es la clase conexion es la variable

# recibe parametro %s
        sql = """
        INSERT INTO roles(rol_id, rol_nombre, rol_permisos)
        VALUES(%s, %s, %s)
        """
        cursor.execute(
            sql,
            (rol.rol_id,
             rol.rol_nombre,
             rol.rol_permisos)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        

    def actualizar(self, rol):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # C

        # modifique por ID 
        sql = """ 
        UPDATE roles
        SET rol_nombre = %s, rol_permisos = %s
        WHERE rol_id = %s  
        """
        cursor.execute(
            sql,
            (rol.rol_nombre,
             rol.rol_permisos,
             rol.rol_id)
        )

        conexion.commit() # confirmar un edicion de base de datos
        cursor.close()
        conexion.close()


    # eliminar un regsitro
    def eliminar(self, rol_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # C

        cursor.execute(
            "DELETE FROM roles WHERE rol_id = %s",
            (rol_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT rol_id FROM roles ORDER BY rol_id DESC")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]