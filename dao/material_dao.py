#DAO: Data Access Object
#material_dao: Objeto de acceso a datos de la tabla materiales


from database.conexion import Conexion    #Carpeta/archivo/clase 
from models.material import Material

class MaterialDAO:
#SELECT * FROM materiales
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        #objeto para postgresql 
        cursor = conexion.cursor()
        #que comando ejecutar

        cursor.execute("SELECT * FROM materiales")
        registros = cursor.fetchall() #nombre de la tabla/el resultado de cursor fetchall
        
        materiales = [] #lista vacia
        for registro in registros:  #crea un nuevo material con nueva info
            material = Material(
                material_id=registro[0],
                material_nombre=registro[1],
                material_tipo=registro[2],
                material_color=registro[3],
                material_cantidad=registro[4],
                material_unidad=registro[5],
                material_marca=registro[6],
                material_proveedor=registro[7],
                material_precio=registro[8]
            )
            materiales.append(material)

        cursor.close()
        conexion.close()
        return materiales
    #Crear insertar

    def insertar(self, material):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#Conexion es la clase conexion es la variable

#recibe parametro %s
        sql = """
        INSERT INTO materiales(material_id, material_nombre, material_tipo, material_color, material_cantidad, material_unidad, material_marca, material_proveedor, material_precio)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (material.material_id,
            material.material_nombre,
            material.material_tipo,
            material.material_color,
            material.material_cantidad,
            material.material_unidad,
            material.material_marca,
            material.material_proveedor,
            material.material_precio)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        

    def actualizar(self, material):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#C

        #modifique por ID 
        sql = """ 
        UPDATE materiales
        SET material_nombre = %s, material_tipo = %s, material_color = %s,
            material_cantidad = %s, material_unidad = %s, material_marca = %s,
            material_proveedor = %s, material_precio = %s
        WHERE material_id = %s  
        """
        cursor.execute(
            sql,
            (material.material_nombre,
            material.material_tipo,
            material.material_color,
            material.material_cantidad,
            material.material_unidad,
            material.material_marca,
            material.material_proveedor,
            material.material_precio,
            material.material_id)
        )

        conexion.commit()#confirmar un edicion de base de datos
        cursor.close()
        conexion.close()



    #eliminar un regsitro
    def eliminar(self, material_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()#C

        cursor.execute(
            "DELETE FROM materiales WHERE material_id = %s",
             (material_id,)
             )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT material_id FROM materiales ORDER BY material_id DESC")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]