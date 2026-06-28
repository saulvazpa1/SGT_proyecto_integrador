#DAO: Data Access Object
#usuario_dao: Objeto de acceso a datos de la tabla usuarios

from database.conexion import Conexion
from models.usuario import Usuario

class UsuarioDAO:
    # SELECT * FROM usuarios
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        registros = cursor.fetchall()
        
        usuarios = []
        for registro in registros:
            usuario = Usuario(
                usuario_id=registro[0],
                usuario_nombre=registro[1],
                usuario_apellidop=registro[2],
                usuario_apellidom=registro[3],
                usuario_telefono=registro[4],
                usuario_correo=registro[5],
                usuario_password=registro[6],
                rol_id=registro[7]
            )
            usuarios.append(usuario)
            
        cursor.close()
        conexion.close()
        return usuarios

    # Crear insertar
    def insertar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO usuarios(usuario_id, usuario_nombre, usuario_apellidop, usuario_apellidom, usuario_telefono, usuario_correo, usuario_password, rol_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (usuario.usuario_id,
            usuario.usuario_nombre,
            usuario.usuario_apellidop,
            usuario.usuario_apellidom,
            usuario.usuario_telefono,
            usuario.usuario_correo,
            usuario.usuario_password,
            usuario.rol_id)
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
            usuario_telefono = %s, usuario_correo = %s, usuario_password = %s,
            rol_id = %s
        WHERE usuario_id = %s
        """
        cursor.execute(
            sql,
            (usuario.usuario_nombre,
            usuario.usuario_apellidop,
            usuario.usuario_apellidom,
            usuario.usuario_telefono,
            usuario.usuario_correo,
            usuario.usuario_password,
            usuario.rol_id,
            usuario.usuario_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # eliminar un registro
    def eliminar(self, usuario_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM usuarios WHERE usuario_id = %s",
            (usuario_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()