#DAO: Data Access Object
#material_dao: Objeto de acceso a datos de la tabla materiales

from database.conexion import Conexion
from models.material import Material

class MaterialDAO:
    # SELECT * FROM materiales
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM materiales")
        registros = cursor.fetchall()
        
        materiales = []
        for registro in registros:
            material = Material(
                registro[0],  # material_id
                registro[1],  # material_nombre
                registro[2],  # material_tipo
                registro[3],  # material_color
                registro[4],  # material_cantidad
                registro[5],  # material_unidad
                registro[6],  # material_marca
                registro[7],  # material_proveedor
                registro[8]   # material_precio
            )
            materiales.append(material)
            
        cursor.close()
        conexion.close()
        return materiales

    # Crear insertar
    def insertar(self, material):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
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

    # Actualizar un registro existente
    def actualizar(self, material):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
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
        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, material_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM materiales WHERE material_id = %s",
            (material_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()