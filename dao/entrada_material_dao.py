#DAO: Data Access Object
#entrada_material_dao: Objeto de acceso a datos de la tabla entradas_materiales


from database.conexion import Conexion    #Carpeta/archivo/clase 
from models.entrada_material import EntradaMaterial

class EntradaMaterialDAO:
#SELECT * FROM entradas_materiales
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        #objeto para postgresql 
        cursor = conexion.cursor()
        #que comando ejecutar

        cursor.execute("SELECT * FROM entradas_materiales")
        registros = cursor.fetchall() #nombre de la tabla/el resultado de cursor fetchall
        
        entradas = [] #lista vacia
        for registro in registros:  #crea un nuevo entrada con nueva info
            entrada = EntradaMaterial(
                entrada_id=registro[0],
                material_id=registro[1],
                usuario_id=registro[2],
                entrada_fecha=registro[3],
                entrada_cantidad=registro[4]
            )
            entradas.append(entrada)

        cursor.close()
        conexion.close()
        return entradas
    #Crear insertar

    def insertar(self, entrada):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#Conexion es la clase conexion es la variable

#recibe parametro %s
        sql = """
        INSERT INTO entradas_materiales(entrada_id, material_id, usuario_id, entrada_fecha, entrada_cantidad)
        VALUES(%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (entrada.entrada_id,
            entrada.material_id,
            entrada.usuario_id,
            entrada.entrada_fecha,
            entrada.entrada_cantidad)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        

    def actualizar(self, entrada):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#C

        #modifique por ID 
        sql = """ 
        UPDATE entradas_materiales
        SET material_id = %s, usuario_id = %s, entrada_fecha = %s,
            entrada_cantidad = %s
        WHERE entrada_id = %s  
        """
        cursor.execute(
            sql,
            (entrada.material_id,
            entrada.usuario_id,
            entrada.entrada_fecha,
            entrada.entrada_cantidad,
            entrada.entrada_id)
        )

        conexion.commit()#confirmar un edicion de base de datos
        cursor.close()
        conexion.close()



    #eliminar un regsitro
    def eliminar(self, entrada_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#C

        cursor.execute(
            "DELETE FROM entradas_materiales WHERE entrada_id = %s",
             (entrada_id,)
             )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT entrada_id FROM entradas_materiales ORDER BY entrada_id DESC")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]