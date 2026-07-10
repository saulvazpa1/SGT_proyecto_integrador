#DAO: Data Access Object
#cliente_dao: Objeto de acceso a datos de la tabla ordenes_produccion

from database.conexion import Conexion
from models.ordenes_produccion import OrdenProduccion

class OrdenProduccionDAO:
    # SELECT * FROM ordenes_produccion
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ordenes_produccion")
        registros = cursor.fetchall()
        
        ordenes = []
        for registro in registros:
            orden = OrdenProduccion(
                registro[0],  # produccion_id
                registro[1],  # pedido_id
                registro[2],  # producto_id
                registro[3],  # encargado_produccion_id
                registro[4],  # produccion_cantidad
                registro[5],  # produccion_estado
                registro[6],  # fecha_inicio
                registro[7],  # fecha_entrega
                registro[8],  # tela_tipo
                registro[9],  # tela_ancho
                registro[10], # tela_largo
                registro[11], #patron_largo
                registro[12], #patron_ancho
                registro[13], #retazo_sobrante
                registro[14]  #tela_total_utilizada
            )
            ordenes.append(ordenes)
            
        cursor.close()
        conexion.close()
        return ordenes
    
    # Crear insertar
    def insertar(self, orden):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO ordenes_produccion(
	    produccion_id, pedido_id, producto_id, encargado_produccion_id, produccion_cantidad, produccion_estado, fecha_inicio, fecha_entrega, tela_tipo, tela_ancho, tela_largo, patron_largo, patron_ancho, retazo_sobrante, tela_total_utilizada)
	    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            sql,
            (orden.produccion_id,
            orden.pedido_id,
            orden.producto_id,
            orden.encargado_produccion_id,
            orden.produccion_cantidad,
            orden.produccion_estado,
            orden.fecha_inicio,
            orden.fecha_entrega,
            orden.tela_tipo,
            orden.tela_ancho,
            orden.tela_largo,
            orden.patron_largo,
            orden.patron_ancho,
            orden.retazo_sobrante,
            orden.tela_total_utilizada
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # Actualizar un registro existente
    def actualizar(self, orden):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE ordenes_produccion
        SET pedido_id = %s, producto_id = %s,
        encargado_produccion_id = %s, produccion_cantidad = %s, produccion_estado = %s,
        fecha_inicio = %s, fecha_entrega = %s, tela_tipo = %s, tela_ancho = %s, tela_largo = %s,
        patron_largo = %s, patron_ancho = %s, retazo_sobrante = %s, tela_total_utilizada = %s
        WHERE produccion_id = %s
        """

        cursor.execute(
            sql,
            (orden.produccion_id,
            orden.pedido_id,
            orden.producto_id,
            orden.encargado_produccion_id,
            orden.produccion_cantidad,
            orden.produccion_estado,
            orden.fecha_inicio,
            orden.fecha_entrega,
            orden.tela_tipo,
            orden.tela_ancho,
            orden.tela_largo,
            orden.patron_largo,
            orden.patron_ancho,
            orden.retazo_sobrante,
            orden.tela_total_utilizada
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # Eliminar un registro
    def eliminar(self, produccion_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM ordenes_produccion WHERE produccion_id = %s",
            (produccion_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    #cambio
