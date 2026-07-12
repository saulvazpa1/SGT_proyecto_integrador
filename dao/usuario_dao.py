# DAO: Data Access Object
# usuario_dao: Objeto de acceso a datos de la tabla usuarios

from database.conexion import Conexion
from models.usuario import Usuario

class UsuarioDAO:

    # Consulta a la vista para traer el nombre del rol en texto
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        # Usamos la vista de pgAdmin
        cursor.execute("SELECT * FROM vista_usuarios_roles")
        registros = cursor.fetchall()
        
        usuarios = []
        for reg in registros:
            # Creamos el objeto mapeando los datos de la vista.
            # Nota: Asegúrate de adaptar los atributos según tu constructor de la clase Usuario.
            usuario = Usuario(
                usuario_id=reg[0],
                usuario_nombre=reg[1],       
                usuario_apellidop="",         
                usuario_apellidom="",
                usuario_telefono=reg[2],
                usuario_correo=reg[3],
                usuario_password="",          
                rol_id=reg[4]                 
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