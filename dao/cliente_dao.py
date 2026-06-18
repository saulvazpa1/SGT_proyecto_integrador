#DAO: Data Access Object
#cliente_dao: Objeto de acceso a datos de la tabla clientes

from database.conexion import Conexion
from models.cliente import Cliente

class ClienteDAO:
    # SELECT * FROM clientes
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        registros = cursor.fetchall()
        
        clientes = []
        for registro in registros:
            cliente = Cliente(
                registro[0],  # cliente_id
                registro[1],  # cliente_nombre
                registro[2],  # cliente_telefono
                registro[3],  # cliente_correo
                registro[4],  # cliente_calle
                registro[5],  # cliente_numero
                registro[6],  # cliente_municipio
                registro[7],  # cliente_estado
                registro[8]   # cliente_codigopostal
            )
            clientes.append(cliente)
            
        cursor.close()
        conexion.close()
        return clientes

    # Crear insertar
    def insertar(self, cliente):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO clientes(cliente_id, cliente_nombre, cliente_telefono, cliente_correo, cliente_calle, cliente_numero, cliente_municipio, cliente_estado, cliente_codigopostal)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (cliente.cliente_id,
             cliente.cliente_nombre,
             cliente.cliente_telefono,
             cliente.cliente_correo,
             cliente.cliente_calle,
             cliente.cliente_numero,
             cliente.cliente_municipio,
             cliente.cliente_estado,
             cliente.cliente_codigopostal)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, cliente):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE clientes
        SET cliente_nombre = %s, cliente_telefono = %s, cliente_correo = %s,
            cliente_calle = %s, cliente_numero = %s, cliente_municipio = %s,
            cliente_estado = %s, cliente_codigopostal = %s
        WHERE cliente_id = %s
        """
        cursor.execute(
            sql,
            (cliente.cliente_nombre,
             cliente.cliente_telefono,
             cliente.cliente_correo,
             cliente.cliente_calle,
             cliente.cliente_numero,
             cliente.cliente_municipio,
             cliente.cliente_estado,
             cliente.cliente_codigopostal,
             cliente.cliente_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    # eliminar un registro
    def eliminar(self, cliente_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM clientes WHERE cliente_id = %s",
            (cliente_id,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()