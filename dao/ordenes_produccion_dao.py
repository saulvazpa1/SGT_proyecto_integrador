# DAO: Data Access Object
# orden_produccion_dao: Objeto de acceso a datos de la tabla ordenes_produccion

from database.conexion import Conexion    # Carpeta/archivo/clase 
from models.orden_produccion import OrdenProduccion

class OrdenProduccionDAO:
    def obtener_todos(self):
       
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_ordenes_produccion")
        registros = cursor.fetchall() 
        
        ordenes_produccion = [] 
        for registro in registros:  
            # Usamos el asterisco '*' para desempaquetar el registro directo en los 15 parámetros de tu modelo
            orden = OrdenProduccion(*registro)
            ordenes_produccion.append(orden)

        cursor.close()
        conexion.close()
        return ordenes_produccion
        
        
        
    


    def insertar(self, orden):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() 

        sql = """
        INSERT INTO ordenes_produccion(
            produccion_id, pedido_id, producto_id, encargado_produccion_id, 
            produccion_cantidad, produccion_estado, fecha_inicio, fecha_entrega, 
            tela_tipo, tela_ancho, tela_largo, patron_largo, patron_ancho, 
            retazo_sobrante, tela_total_utilizada
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
             orden.tela_total_utilizada)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        
    # Actualización en la tabla base
    def actualizar(self, orden):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() 

        sql = """ 
        UPDATE ordenes_produccion
        SET pedido_id = %s, producto_id = %s, encargado_produccion_id = %s,
            produccion_cantidad = %s, produccion_estado = %s, fecha_inicio = %s,
            fecha_entrega = %s, tela_tipo = %s, tela_ancho = %s, tela_largo = %s,
            patron_largo = %s, patron_ancho = %s, retazo_sobrante = %s,
            tela_total_utilizada = %s
        WHERE produccion_id = %s  
        """
        cursor.execute(
            sql,
            (orden.pedido_id,
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
             orden.tela_total_utilizada,
             orden.produccion_id)
        )

        conexion.commit() 
        cursor.close()
        conexion.close()

    # Eliminación por ID
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

    # Control de ID correlativo secuencial
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT produccion_id FROM ordenes_produccion ORDER BY produccion_id DESC LIMIT 1")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]