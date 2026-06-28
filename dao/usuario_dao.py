#DAO: Data Access Object
#usuario_dao: Objeto de acceso a datos de la tabla usuarios


from database.conexion import Conexion    #Carpeta/archivo/clase 
from models.usuario import Usuario

class UsuarioDAO:
#SELECT * FROM usuarios
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        #objeto para postgresql 
        cursor = conexion.cursor()
        #que comando ejecutar

        cursor.execute("SELECT * FROM usuarios")
        registros = cursor.fetchall() #nombre de la tabla/el resultado de cursor fetchall
        
        usuarios = [] #lista vacia
        for registro in registros:  #crea un nuevo usuario con nueva info
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
    #Crear insertar

    def insertar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#Conexion es la clase conexion es la variable

#recibe parametro %s
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
        cursor = conexion.cursor()#C

        #modifique por ID 
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

        conexion.commit()#confirmar un edicion de base de datos
        cursor.close()
        conexion.close()



    #eliminar un regsitro
    def eliminar(self, usuario_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#C

        cursor.execute(
            "DELETE FROM usuarios WHERE usuario_id = %s",
             (usuario_id,)
             )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT usuario_id FROM usuarios ORDER BY usuario_id DESC")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]