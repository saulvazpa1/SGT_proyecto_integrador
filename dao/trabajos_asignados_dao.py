#DAO: Data Access Object
#cliente_dao: Objeto de acceso a datos de la tabla trabajos_asignados

from database.conexion import Conexion
from models.trabajo_asignado import TrabajoAsignado

class TrabajoAsignadoDAO:
    # SELECT * FROM trabajos_asignados
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM trabajos_asignados")
        registros = cursor.fetchall()
        
        trabajos = []
        for registro in registros:
            trabajo = TrabajoAsignado(
                registro[0],  # trabajo_id
                registro[1],  # trabajador_id
                registro[2],  # produccion_id
                registro[3],  # trabajo_nombre
                registro[4],  # trabajo_fecha
                registro[5]   # trabajo_estado
            )
            trabajos.append(trabajo)
            
        cursor.close()
        conexion.close()
        return trabajos
    
        # Crear insertar
    def insertar(self, trabajo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO trabajos_asignados(
	    trabajo_id, trabajador_id, produccion_id, trabajo_nombre, trabajo_fecha, trabajo_estado)
	    VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            sql,
            (trabajo.trabajo_id,
            trabajo.trabajador_id,
            trabajo.produccion_id,
            trabajo.trabajo_nombre,
            trabajo.trabajo_fecha,
            trabajo.trabajo_estado
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar un registro existente
    def actualizar(self, trabajo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE trabajos_asignados
        SET trabajador_id = %s, produccion_id = %s,
        trabajador_nombre = %s, trabajador_fecha = %s, trabajo_estado = %s
        WHERE salida_id = %s
        """

        cursor.execute(
            sql,
            (trabajo.trabajo_id,
            trabajo.trabajador_id,
            trabajo.produccion_id,
            trabajo.trabajo_nombre,
            trabajo.trabajo_fecha,
            trabajo.trabajo_estado
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, trabajo_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM trabajos_asignados WHERE trabajador_id = %s",
            (trabajo_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()