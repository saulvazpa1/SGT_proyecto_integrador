#DAO: Data Access Object
#entrada_material_dao: Objeto de acceso a datos de la tabla entradas_materiales

from database.conexion import Conexion
from models.entrada_material import EntradaMaterial

class EntradaMaterialDAO:
    # SELECT * FROM entradas_materiales
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM entradas_materiales")
        registros = cursor.fetchall()
        
        entradas = []
        for registro in registros:
            entrada = EntradaMaterial(
                registro[0],  # entrada_id
                registro[1],  # material_id
                registro[2],  # usuario_id
                registro[3],  # entrada_fecha
                registro[4]   # entrada_cantidad
            )
            entradas.append(entrada)
            
        cursor.close()
        conexion.close()
        return entradas

    # Crear insertar
    def insertar(self, entrada):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
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
        cursor = conexion.cursor()
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
        conexion.commit()
        cursor.close()
        conexion.close()

    # eliminar un registro
    def eliminar(self, entrada_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM entradas_materiales WHERE entrada_id = %s",
            (entrada_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()