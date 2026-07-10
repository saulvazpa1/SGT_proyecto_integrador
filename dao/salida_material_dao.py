#DAO: Data Access Object
#cliente_dao: Objeto de acceso a datos de la tabla salidas_materiales

from database.conexion import Conexion
from models.salida_material import SalidaMaterial

class SalidaMaterialDAO:
    # SELECT * FROM salidas_materiales
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM salidas_materiales")
        registros = cursor.fetchall()
        
        salidas = []
        for registro in registros:
            salida = SalidaMaterial(
                registro[0],  # salida_id
                registro[1],  # material_id
                registro[2],  # produccion_id
                registro[3],  # usuario_id
                registro[4],  # salida_fecha
                registro[5]   # salida cantidad
            )
            salidas.append(salida)
            
        cursor.close()
        conexion.close()
        return salidas
    
        # Crear insertar
    def insertar(self, salida):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO salidas_materiales(
	    salida_id, material_id, produccion_id, usuario_id, salida_fecha, salida_cantidad)
	    VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            sql,
            (salida.salida_id,
            salida.material_id,
            salida.produccion_id,
            salida.usuario_id,
            salida.salida_fecha,
            salida.salida_cantidad
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

        # Actualizar un registro existente
    def actualizar(self, salida):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE salidas_materiales
        SET material_id = %s, produccion_id = %s,
        usuario_id = %s, salida_fecha = %s, salida_cantidad = %s
        WHERE salida_id = %s
        """

        cursor.execute(
            sql,
            (salida.salida_id,
            salida.material_id,
            salida.produccion_id,
            salida.usuario_id,
            salida.salida_fecha,
            salida.salida_cantidad
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, salida_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM ordenes_produccion WHERE salidas_materiales = %s",
            (salida_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()