# DAO: Data Access Object
# pedido_dao: Objeto de acceso a datos de la tabla pedidos

from database.conexion import Conexion    # Carpeta/archivo/clase 
from models.pedido import Pedido

class PedidoDAO:
# SELECT * FROM pedidos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        # objeto para postgresql 
        cursor = conexion.cursor()
        # que comando ejecutar

        cursor.execute("SELECT * FROM vista_pedido")
        registros = cursor.fetchall() # nombre de la tabla/el resultado de cursor fetchall
        
        pedidos = [] # lista vacia
        for registro in registros:  # crea un nuevo pedido con nueva info
            pedido = Pedido(
                pedido_id=registro[0],
                cliente_id=registro[1],
                vendedor_id=registro[2],
                producto_id=registro[3],
                pedido_cantidad=registro[4],
                pedido_total=registro[5],
                pedido_estado=registro[6],
                pedido_fecha=registro[7]
            )
            pedidos.append(pedido)

        cursor.close()
        conexion.close()
        return pedidos
    # Crear insertar

    def insertar(self, pedido):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # Conexion es la clase conexion es la variable

# recibe parametro %s
        sql = """
        INSERT INTO pedidos(pedido_id, cliente_id, vendedor_id, producto_id, pedido_cantidad, pedido_total, pedido_estado, pedido_fecha)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (pedido.pedido_id,
             pedido.cliente_id,
             pedido.vendedor_id,
             pedido.producto_id,
             pedido.pedido_cantidad,
             pedido.pedido_total,
             pedido.pedido_estado,
             pedido.pedido_fecha)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        

    def actualizar(self, pedido):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # C

        # modifique por ID 
        sql = """ 
        UPDATE pedidos
        SET cliente_id = %s, vendedor_id = %s, producto_id = %s,
            pedido_cantidad = %s, pedido_total = %s, pedido_estado = %s,
            pedido_fecha = %s
        WHERE pedido_id = %s  
        """
        cursor.execute(
            sql,
            (pedido.cliente_id,
             pedido.vendedor_id,
             pedido.producto_id,
             pedido.pedido_cantidad,
             pedido.pedido_total,
             pedido.pedido_estado,
             pedido.pedido_fecha,
             pedido.pedido_id)
        )

        conexion.commit() # confirmar un edicion de base de datos
        cursor.close()
        conexion.close()


    # eliminar un regsitro
    def eliminar(self, pedido_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() # C

        cursor.execute(
            "DELETE FROM pedidos WHERE pedido_id = %s",
            (pedido_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT pedido_id FROM pedidos ORDER BY pedido_id DESC")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]