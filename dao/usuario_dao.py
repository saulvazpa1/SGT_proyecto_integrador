# DAO: Data Access Object
# usuario_dao: Objeto de acceso a datos de la tabla usuarios

from database.conexion import Conexion
from models.usuario import Usuario

class UsuarioDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT u.usuario_id, u.usuario_nombre, u.usuario_apellidop, u.usuario_apellidom,
                   u.usuario_telefono, u.usuario_correo, u.usuario_password, r.rol_nombre
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.rol_id
            ORDER BY u.usuario_nombre
        """)
        registros = cursor.fetchall()

        usuarios = []
        for reg in registros:
            usuario = Usuario(
                usuario_id=reg[0],
                usuario_nombre=reg[1],
                usuario_apellidop=reg[2],
                usuario_apellidom=reg[3],
                usuario_telefono=reg[4],
                usuario_correo=reg[5],
                usuario_password=reg[6],
                rol_id=reg[7]
            )
            usuarios.append(usuario)

        cursor.close()
        conexion.close()
        return usuarios

    def insertar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuarios(usuario_id, usuario_nombre, usuario_apellidop, usuario_apellidom, usuario_telefono, usuario_correo, usuario_password, rol_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (usuario.usuario_id, usuario.usuario_nombre, usuario.usuario_apellidop, 
             usuario.usuario_apellidom, usuario.usuario_telefono, usuario.usuario_correo, 
             usuario.usuario_password, usuario.rol_id) # Aquí sí mandas el ID numérico al insertar
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE usuarios
        SET usuario_nombre = %s, usuario_apellidop = %s, usuario_apellidom = %s,
            usuario_telefono = %s, usuario_correo = %s, usuario_password = %s, rol_id = %s
        WHERE usuario_id = %s
        """
        cursor.execute(
            sql,
            (usuario.usuario_nombre, usuario.usuario_apellidop, usuario.usuario_apellidom,
             usuario.usuario_telefono, usuario.usuario_correo, usuario.usuario_password, 
             usuario.rol_id, usuario.usuario_id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, usuario_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE usuario_id = %s",
            (usuario_id,)
            )
        cursor.execute("DELETE FROM usuarios WHERE usuario_id = %s", (usuario_id,))
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT usuario_id FROM usuarios ORDER BY usuario_id DESC LIMIT 1")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]

    #Inicio de sesion
    def iniciar_sesion(self, correo, password):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT * FROM usuarios
        WHERE usuario_correo = %s
        AND usuario_password = %s
        """

        cursor.execute(sql, (correo, password))
        registro = cursor.fetchone()
        cursor.close()
        conexion.close()

        if registro:
            return Usuario(
                usuario_id = registro[0],
                usuario_nombre = registro[1],
                usuario_apellidop = registro[2],
                usuario_apellidom = registro[3],
                usuario_telefono = registro[4],
                usuario_correo = registro[5],
                usuario_password = registro[6],
                rol_id = registro[7]
            )
        return None