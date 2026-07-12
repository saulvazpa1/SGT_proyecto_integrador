from database.conexion import Conexion    # Carpeta/archivo/clase 
from models.usuario import Usuario
from models.cliente import Cliente
from models.material import Material
from models.entrada_material import EntradaMaterial
from database.conexion import Conexion  # Ajusta la ruta según tu proyecto
from models.orden_produccion import OrdenProduccion


from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from dao.material_dao import MaterialDAO
from dao.entrada_material_dao import EntradaMaterialDAO
from dao.ordenes_produccion_dao import OrdenProduccionDAO
from dao.salida_material_dao import SalidaMaterialDAO
from dao.trabajos_asignados_dao import TrabajoAsignadoDAO
from dao.rol_dao import RolDAO
from dao.producto_dao import ProductoDAO
from models.producto import Producto
from dao.pedido_dao import PedidoDAO
from models.pedido import Pedido
from models.producto import Producto

#Funciones v 2.0
def ver_materiales():
    try:
        material_dao = MaterialDAO()
        materiales = material_dao.obtener_todos()
        print("\n=== Materiales en Inventario ===")
        if len(materiales) == 0:
            print("No hay materiales registrados")
        else:
            for mat in materiales:  
                print("-------------------------------------------")
                print(
                    f"ID:{mat.material_id}, Nombre:{mat.material_nombre},"
                    f" Tipo:{mat.material_tipo}, Color:{mat.material_color},"
                    f" Cantidad:{mat.material_cantidad}, Medida:{mat.material_unidad}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

def insertar_material():
    nombre = input("Nombre de la tela o insumo: ")
    tipo = input("Tipo de material: ")
    color = input("Color del material: ")
    cantidad = float(input("Cantidad en almacén: "))
    unidad = input("Unidad de medida (Metros/Rollos/Piezas): ")
    marca = input("Marca del fabricante: ")
    proveedor = input("Nombre del proveedor: ")
    precio = float(input("Precio unitario: "))
    try:
        material_dao = MaterialDAO()
        id = material_dao.obtener_ultimo_id() + 1
        material = Material(id, nombre, tipo, color, cantidad, unidad, marca, proveedor, precio)
        material_dao.insertar(material)
        print("Material registrado exitosamente en el inventario")
    except Exception as e:
        print("Error al registrar el material\n", e)

def actualizar_material():
    print("Selecciona el material a actualizar")
    try:
        material_dao = MaterialDAO()
        ver_materiales()
        id = int(input("Escribe el ID del material a modificar: "))
        nombre = input("Nuevo nombre del material: ")
        tipo = input("Nuevo tipo: ")
        color = input("Nuevo color: ")
        cantidad = float(input("Modificar cantidad física actual: "))
        unidad = input("Nueva unidad de medida: ")
        marca = input("Nueva marca: ")
        proveedor = input("Nuevo proveedor: ")
        precio = float(input("Nuevo precio unitario: "))
        
        material = Material(id, nombre, tipo, color, cantidad, unidad, marca, proveedor, precio)
        material_dao.actualizar(material)
        print(f"El material {id} ha sido actualizado")
    except Exception as e:
        print("Error al actualizar material\n", e)

def eliminar_material():
    try:
        material_dao = MaterialDAO()
        ver_materiales()
        id = int(input("Escribe el ID del material a eliminar de los registros: "))
        material_dao.eliminar(id)
        print(f"El material {id} fue removido")
    except Exception as e:
        print("Error al borrar material\n", e)

def ver_entradas_materiales():
    try:
        entrada_dao = EntradaMaterialDAO()
        entradas = entrada_dao.obtener_todos()
        print("\n=== Historial de Entradas de Materiales ===")
        if len(entradas) == 0:
            print("No hay entradas de materiales registradas")
        else:
            for entrada in entradas:
                print("-------------------------------------------")
                print(
                    f"ID Entrada:{entrada.entrada_id}, ID Material:{entrada.material_id},"
                    f" ID Usuario:{entrada.usuario_id}, Fecha:{entrada.entrada_fecha},"
                    f" Cantidad:{entrada.entrada_cantidad}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

def insertar_entrada():
    try:
        entrada_dao = EntradaMaterialDAO()
        ver_materiales()
        material_id = int(input("Escribe el ID del material que va a ingresar: "))
        ver_usuarios()
        usuario_id = int(input("Escribe tu ID de usuario receptor: "))
        fecha = input("Fecha de entrada (AAAA-MM-DD): ")
        cantidad = float(input("Cantidad física que ingresa: "))
        
        id = entrada_dao.obtener_ultimo_id() + 1
        entrada = EntradaMaterial(id, material_id, usuario_id, fecha, cantidad)
        entrada_dao.insertar(entrada)
        print("¡Entrada e historial de almacén añadidos exitosamente!")
    except Exception as e:
        print("Error al guardar transacción de entrada\n", e)

def ver_salidas():
    try:
        salida_material_dao = SalidaMaterialDAO() 
        ordenes = salida_material_dao.obtener_todos()
        print("\n=== Salidas de Material en el Sistema ===")
        if len(ordenes) == 0:
            print("No hay salidas registradas")
        else:
            for salida in ordenes:
                print("-------------------------------------------")
                print(
                    f"ID:{salida.salida_id}, Material:{salida.material_id},"
                    f" Produccion:{salida.produccion_id}, Usuario:{salida.usuario_id},"
                    f" Fecha de salida:{salida.salida_fecha}, Cantidad:{salida.salida_cantidad}"
                )
                print("-------------------------------------------")
        print("\nConexión exitosa a la base de datos")
    except Exception as e:
        print("Error:\n", e)

def insertar_rol():
    nombre = input("Escribe el nombre del rol: ")
    permisos = input("Escribe los permisos: ")
    try:
        roles_dao = RolDAO()
        id = roles_dao.obtener_ultimo_id() + 1
        rol = rol(id, nombre, permisos)
        roles_dao.insertar(rol)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error:", e)

def ver_trabajos():
    try:
        trabajos_asignados_dao = TrabajoAsignadoDAO() 
        trabajos = trabajos_asignados_dao.obtener_todos()
        print("\n=== Trabajos Asignados en el Sistema ===")
        if len(trabajos) == 0:
            print("No hay trabajos registrados")
        else:
            for trabajo in trabajos:
                print("-------------------------------------------")
                print(
                    f"ID:{trabajo.trabajo_id}, Trabajador:{trabajo.trabajador_id},"
                    f" Produccion:{trabajo.produccion_id}, Nombre del trabajo:{trabajo.trabajo_nombre},"
                    f" Fecha del trabajo:{trabajo.trabajo_fecha}, Estado del trabajo:{trabajo.trabajo_estado}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)


#Usuario
def ver_usuarios():
    try:
        usuario_dao = UsuarioDAO()
        usuarios = usuario_dao.obtener_todos()
        print("=== Usuarios en el Sistema ===")
        if len(usuarios) == 0:
            print("No hay usuarios registrados")
        else:
            for usuario in usuarios:
                print("-------------------------------------------")
                print(
                    f"ID:{usuario.usuario_id}, Nombre:{usuario.usuario_nombre},"
                    f" Apellido Paterno:{usuario.usuario_apellidop}, Apellido Materno:{usuario.usuario_apellidom},"
                    f" Teléfono:{usuario.usuario_telefono}, Correo:{usuario.usuario_correo},"
                    f" Password:{usuario.usuario_password}, Rol ID:{usuario.rol_id}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

def insertar_usuario():
    nombre = input("Escribe el nombre del nuevo usuario: ")
    apellidop = input("Escribe el apellido paterno: ")
    apellidom = input("Escribe el apellido materno: ")
    telefono = input("Escribe el teléfono: ")
    correo = input("Escribe el correo electrónico: ")
    password = input("Escribe la contraseña: ")
    rol_id = int(input("Escribe el ID del rol asignado: "))
    try:
        usuario_dao = UsuarioDAO()
        id = usuario_dao.obtener_ultimo_id() + 1
        usuario = Usuario(id, nombre, apellidop, apellidom, telefono, correo, password, rol_id)
        usuario_dao.insertar(usuario)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo usuario\n", e)

def actualizar_usuario():
    print("Selecciona el usuario a actualizar")
    try:
        usuario_dao = UsuarioDAO()
        ver_usuarios()
        id = int(input("Escribe el ID del usuario a actualizar: "))
        nombre = input("Escribe el nuevo nombre: ")
        apellidop = input("Escribe el nuevo apellido paterno: ")
        apellidom = input("Escribe el nuevo apellido materno: ")
        telefono = input("Escribe el nuevo teléfono: ")
        correo = input("Escribe el nuevo correo: ")
        password = input("Escribe la nueva contraseña: ")
        rol_id = int(input("Escribe el nuevo ID del rol: "))
        
        usuario = Usuario(id, nombre, apellidop, apellidom, telefono, correo, password, rol_id)
        usuario_dao.actualizar(usuario)
        print(f"El usuario {id} se ha actualizado exitosamente")
    except Exception as e:
        print(" Error al actualizar usuario\n", e)

def eliminar_usuario():
    try:
        usuario_dao = UsuarioDAO()
        print("Lista de usuarios registrados:")
        ver_usuarios()
        id = int(input("Escribe el ID del usuario a eliminar: "))
        usuario_dao.eliminar(id)
        print(f"El usuario {id} ha sido eliminado con éxito")
    except Exception as e:
        print("Error al eliminar el usuario\n", e)


#Cliente
def ver_clientes():
    try:
        cliente_dao = ClienteDAO()
        clientes = cliente_dao.obtener_todos()
        print("=== Clientes en el Sistema ===")
        if len(clientes) == 0:
            print("No hay clientes registrados")
        else:
            for cliente in clientes:
                print("-------------------------------------------")
                print(
                    f"ID:{cliente.cliente_id}, Nombre:{cliente.cliente_nombre},"
                    f" Teléfono:{cliente.cliente_telefono}, Correo:{cliente.cliente_correo},"
                    f" Calle:{cliente.cliente_calle}, Num:{cliente.cliente_numero},"
                    f" Municipio:{cliente.cliente_municipio}, Estado:{cliente.cliente_estado},"
                    f" CP:{cliente.cliente_codigopostal}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

def insertar_cliente():
    nombre = input("Escribe el nombre  cliente: ")
    telefono = input("Escribe el teléfono del cliente: ")
    correo = input("Escribe el correo electrónico: ")
    calle = input("Escribe la calle: ")
    numero = input("Escribe el número: ")
    municipio = input("Escribe el municipio: ")
    estado = input("Escribe el estado: ")
    cp = input("Escribe el código postal: ")
    try:
        cliente_dao = ClienteDAO()
        id = cliente_dao.obtener_ultimo_id() + 1
        cliente = Cliente(id, nombre, telefono, correo, calle, numero, municipio, estado, cp)
        cliente_dao.insertar(cliente)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo cliente\n", e)

def actualizar_cliente():
    print("Selecciona el cliente a actualizar")
    try:
        cliente_dao = ClienteDAO()
        ver_clientes()
        id = int(input("Escribe el ID del cliente a actualizar: "))
        nombre = input("Escribe el nuevo nombre : ")
        telefono = input("Escribe el nuevo teléfono: ")
        correo = input("Escribe el nuevo correo: ")
        calle = input("Escribe la nueva calle: ")
        numero = input("Escribe el nuevo número: ")
        municipio = input("Escribe el nuevo municipio: ")
        estado = input("Escribe el nuevo estado: ")
        cp = input("Escribe el nuevo código postal: ")
        
        cliente = Cliente(id, nombre, telefono, correo, calle, numero, municipio, estado, cp)
        cliente_dao.actualizar(cliente)
        print(f"El cliente {id} se ha actualizado exitosamente")
    except Exception as e:
        print(" Error al actualizar cliente\n", e)

def eliminar_cliente():
    try:
        cliente_dao = ClienteDAO()
        print("Lista de clientes registrados:")
        ver_clientes()
        id = int(input("Escribe el ID del cliente a eliminar: "))
        cliente_dao.eliminar(id)
        print(f"El cliente {id} ha sido eliminado con éxito")
    except Exception as e:
        print("Error:\n", e)

#productos

def ver_productos():
    try:
        producto_dao = ProductoDAO()
        productos = producto_dao.obtener_todos()
        print("\n=== Catálogo de Productos Textiles ===")
        if len(productos) == 0:
            print("No hay productos registrados")
        else:
            for prod in productos:
                print("-------------------------------------------")
                print(
                    f"ID: {prod.producto_id} | Nombre: {prod.producto_nombre}\n"
                    f"Categoría: {prod.producto_categoria} | Precio: ${prod.producto_precio}\n"
                    f"Stock Actual: {prod.producto_stock} | Medida: {prod.producto_unidad_medida}\n"
                    f"Color: {prod.producto_color} | Descripción: {prod.producto_descripcion}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error al visualizar productos:", e)

def insertar_producto():
    nombre = input("Nombre de la prenda/bolsa: ")
    categoria = input("Categoría del producto: ")
    precio = float(input("Precio de venta: "))
    stock = int(input("Stock inicial en almacén: "))
    descripcion = input("Descripción del producto: ")
    unidad = input("Unidad de medida (Pza/Docena): ")
    color = input("Color del producto: ")
    try:
        producto_dao = ProductoDAO()
       
        id_nuevo = producto_dao.obtener_ultimo_id() + 1
        
       
      
        producto = Producto(id_nuevo, nombre, categoria, precio, stock, descripcion, unit_medida=unidad, color=color)
        
        producto_dao.insertar(producto)
        print("¡Producto registrado con éxito en el catálogo!")
    except Exception as e:
        print("Error al registrar el producto:\n", e)
def ver_productos():
    try:
        producto_dao = ProductoDAO()
        productos = producto_dao.obtener_todos()
        print("\n=== Catálogo de Productos Textiles ===")
        if len(productos) == 0:
            print("No hay productos registrados")
        else:
            for prod in productos:
                print("-------------------------------------------")
                print(
                    f"ID: {prod.producto_id} | Nombre: {prod.producto_nombre}\n"
                    f"Categoría: {prod.producto_categoria} | Precio: ${prod.producto_precio}\n"
                    f"Stock Actual: {prod.producto_stock} | Medida: {prod.producto_unidad_medida}\n"
                    f"Color: {prod.producto_color} | Descripción: {prod.producto_descripcion}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error al visualizar productos:", e)

def insertar_producto():
    nombre = input("Nombre de la prenda/bolsa: ")
    categoria = input("Categoría del producto: ")
    precio = float(input("Precio de venta: "))
    stock = int(input("Stock inicial en almacén: "))
    descripcion = input("Descripción del producto: ")
    unidad = input("Unidad de medida (Pza/Docena): ")
    color = input("Color del producto: ")
    try:
        producto_dao = ProductoDAO()
        id_nuevo = producto_dao.obtener_ultimo_id() + 1
        
        producto = Producto(id_nuevo, nombre, categoria, precio, stock, descripcion, unidad, color)
        producto_dao.insertar(producto)
        print("¡Producto registrado con éxito en el catálogo!")
    except Exception as e:
        print("Error al registrar el producto:\n", e)

def actualizar_producto():
    print("Selecciona el producto a actualizar")
    try:
        producto_dao = ProductoDAO()
        ver_productos()
        id = int(input("Escribe el ID del producto a modificar: "))
        nombre = input("Nuevo nombre del producto: ")
        categoria = input("Nueva categoría: ")
        precio = float(input("Nuevo precio de venta: "))
        stock = int(input("Modificar stock actual: "))
        descripcion = input("Nueva descripción: ")
        unidad = input("Nueva unidad de medida: ")
        color = input("Nuevo color: ")
        
        producto = Producto(id, nombre, categoria, precio, stock, descripcion, unidad, color)
        producto_dao.actualizar(producto)
        print(f"El producto con ID {id} ha sido actualizado correctamente.")
    except Exception as e:
        print("Error al actualizar el producto:\n", e)

def eliminar_producto():
    try:
        producto_dao = ProductoDAO()
        ver_productos()
        id = int(input("Escribe el ID del producto a eliminar permanentemente: "))
        producto_dao.eliminar(id)
        print(f"El producto con ID {id} fue removido del catálogo.")
    except Exception as e:
        print("Error al borrar el producto:\n", e)

#pedido

def ver_pedidos():
    try:
        pedido_dao = PedidoDAO()
        pedidos = pedido_dao.obtener_todos()
        print("=== Pedidos en el Sistema ===")
        if len(pedidos) == 0:
            print("No hay pedidos registrados")
        else:
            for pedido in pedidos:
                print("-------------------------------------------")
                
                print(
                    f"ID:{pedido.pedido_id}, Cliente:{pedido.cliente_id},"
                    f" Vendedor:{pedido.vendedor_id}, Producto:{pedido.producto_id},"
                    f" Cantidad:{pedido.pedido_cantidad}, Total:{pedido.pedido_total},"
                    f" Estado:{pedido.pedido_estado}, Fecha:{pedido.pedido_fecha}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

def insertar_pedido():
    ver_clientes()
    cliente_id = int(input("Escribe el ID del cliente asignado: "))
    ver_usuarios()
    vendedor_id = int(input("Escribe el ID del vendedor asignado: "))
    ver_productos()
    producto_id = int(input("Escribe el ID del producto asignado: "))
    cantidad = int(input("Escribe la cantidad: "))
    total = float(input("Escribe el total: "))
    estado = input("Escribe el estado del pedido: ")
    fecha = input("Escribe la fecha (AAAA-MM-DD HH:MM:SS): ")
    try:
        pedido_dao = PedidoDAO()
        id = pedido_dao.obtener_ultimo_id() + 1
        pedido = Pedido(id, cliente_id, vendedor_id, producto_id, cantidad, total, estado, fecha)
        pedido_dao.insertar(pedido)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo pedido\n", e)

def actualizar_pedido():
    print("Selecciona el pedido a actualizar")
    try:
        pedido_dao = PedidoDAO()
        ver_pedidos()
        id = int(input("Escribe el ID del pedido a actualizar: "))
        cliente_id = int(input("Escribe el nuevo ID del cliente: "))
        vendedor_id = int(input("Escribe el nuevo ID del vendedor: "))
        producto_id = int(input("Escribe el nuevo ID del producto: "))
        cantidad = int(input("Escribe la nueva cantidad: "))
        total = float(input("Escribe el nuevo total: "))
        estado = input("Escribe el nuevo estado: ")
        fecha = input("Escribe la nueva fecha (AAAA-MM-DD HH:MM:SS): ")
        
        pedido = Pedido(id, cliente_id, vendedor_id, producto_id, cantidad, total, estado, fecha)
        pedido_dao.actualizar(pedido)
        print(f"El pedido {id} se ha actualizado exitosamente")
    except Exception as e:
        print(" Error al actualizar pedido\n", e)

def eliminar_pedido():
    try:
        pedido_dao = PedidoDAO()
        print("Lista de pedidos registrados:")
        ver_pedidos()
        id = int(input("Escribe el ID del pedido a eliminar: "))
        pedido_dao.eliminar(id)
        print(f"El pedido {id} ha sido eliminado con éxito")
    except Exception as e:
        print("Error al eliminar el pedido\n", e)
#ORdenes de produccion
def ver_ordenes_produccion():
    try:
        orden_dao = OrdenProduccionDAO()
        ordenes = orden_dao.obtener_todos()
        print("=== Órdenes de Producción en el Sistema ===")
        if len(ordenes) == 0:
            print("No hay órdenes de producción registradas")
        else:
            for orden in ordenes:
                print("-------------------------------------------")
                # Imprimimos los datos generales
                print(
                    f"ID Orden:{orden.produccion_id}, Pedido ID:{orden.pedido_id}, "
                    f"Producto ID:{orden.producto_id}, Encargado ID:{orden.encargado_produccion_id}\n"
                    f"Cantidad:{orden.produccion_cantidad}, Estado:{orden.produccion_estado}, "
                    f"Inicio:{orden.fecha_inicio}, Entrega:{orden.fecha_entrega}"
                )
                # ¡Aquí agregamos los datos de la tela que te faltaban mostrar!
                print(
                    f"Tipo Tela:{orden.tela_tipo}, Ancho:{orden.tela_ancho}m, Largo:{orden.tela_largo}m\n"
                    f"Patrón Largo:{orden.patron_largo}cm, Patrón Ancho:{orden.patron_ancho}cm\n"
                    f"Retazo Sobrante:{orden.retazo_sobrante}m, Tela Total Utilizada:{orden.tela_total_utilizada}m"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)


def insertar_orden_produccion():
    print("\n=== Registrar Nueva Orden de Producción ===")
    
    # Pedimos los datos base
    # ver_pedidos() # Puedes descomentar esto si quieres listar los pedidos antes
    pedido_id = int(input("Escribe el ID del pedido asociado: "))
    ver_productos()  
    producto_id = int(input("Escribe el ID del producto a fabricar: "))
    ver_usuarios()   
    encargado_id = int(input("Escribe el ID del encargado de taller: "))
    cantidad = int(input("Escribe la cantidad de bolsas a elaborar: "))
    estado = input("Escribe el estado inicial (En Espera / En Proceso): ")
    fecha_ini = input("Escribe la fecha de inicio (AAAA-MM-DD): ")
    fecha_ent = input("Escribe la fecha de entrega (AAAA-MM-DD): ")
    
    # Pedimos los datos de confección
    tela_tipo = input("Escribe el tipo de tela: ")
    tela_ancho = float(input("Escribe el ancho de la tela (metros): "))
    tela_largo = float(input("Escribe el largo de la tela (metros): "))
    patron_largo = float(input("Escribe el largo del patrón de la bolsa: "))
    patron_ancho = float(input("Escribe el ancho del patrón de la bolsa: "))
    retazo_sobrante = float(input("Escribe el retazo sobrante estimado: "))
    tela_usada = float(input("Escribe los metros de tela totales a usar: "))
    
    try:
        orden_dao = OrdenProduccionDAO()
        
        # Calculamos tu ID correlativo manual como lo manejas en Usuarios
        id_nuevo = orden_dao.obtener_ultimo_id() + 1
        
        # Enviamos los 15 parámetros en el orden exacto que requiere el desempaquetado de tu DAO
        nueva_orden = OrdenProduccion(
            id_nuevo,              # 1. produccion_id
            pedido_id,             # 2. pedido_id (¡El que nos faltaba!)
            producto_id,           # 3. producto_id
            encargado_id,          # 4. encargado_produccion_id
            cantidad,              # 5. produccion_cantidad
            estado,                # 6. produccion_estado
            fecha_ini,             # 7. fecha_inicio
            fecha_ent,             # 8. fecha_entrega
            tela_tipo,             # 9. tela_tipo
            tela_ancho,            # 10. tela_ancho
            tela_largo,            # 11. tela_largo
            patron_largo,          # 12. patron_largo
            patron_ancho,          # 13. patron_ancho
            retazo_sobrante,       # 14. retazo_sobrante
            tela_usada             # 15. tela_total_utilizada
        )
        
        orden_dao.insertar(nueva_orden)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo usuario\n", e) # Mantenemos tu formato de print para errores
def actualizar_orden_produccion():
    print("=== Selecciona la Orden de Producción a actualizar ===")
    try:
        orden_dao = OrdenProduccionDAO()
        ver_ordenes_produccion()  # Para que veas los IDs existentes
        
        # Pedimos el ID de la orden que se va a modificar
        id = int(input("Escribe el ID de la orden a actualizar: "))
        
        # Pedimos los 14 datos restantes en el orden exacto del modelo
        pedido_id = int(input("Escribe el nuevo ID del pedido asociado: "))
        producto_id = int(input("Escribe el nuevo ID del producto: "))
        encargado_id = int(input("Escribe el nuevo ID del encargado de taller: "))
        cantidad = int(input("Escribe la nueva cantidad a elaborar: "))
        estado = input("Escribe el nuevo estado (En Espera / En Proceso / Terminado): ")
        fecha_ini = input("Escribe la nueva fecha de inicio (AAAA-MM-DD): ")
        fecha_ent = input("Escribe la nueva fecha de entrega (AAAA-MM-DD): ")
        
        tela_tipo = input("Escribe el nuevo tipo de tela: ")
        tela_ancho = float(input("Escribe el nuevo ancho de la tela (metros): "))
        tela_largo = float(input("Escribe el nuevo largo de la tela (metros): "))
        patron_largo = float(input("Escribe el nuevo largo del patrón: "))
        patron_ancho = float(input("Escribe el nuevo ancho del patrón: "))
        retazo_sobrante = float(input("Escribe el nuevo retazo sobrante estimado: "))
        tela_usada = float(input("Escribe los nuevos metros de tela totales utilizados: "))
        
        # Armamos el objeto con los 15 parámetros idénticos al constructor
        orden = OrdenProduccion(
            id,
            pedido_id,
            producto_id,
            encargado_id,
            cantidad,
            estado,
            fecha_ini,
            fecha_ent,
            tela_tipo,
            tela_ancho,
            tela_largo,
            patron_largo,
            patron_ancho,
            retazo_sobrante,
            tela_usada
        )
        
        orden_dao.actualizar(orden)
        print(f"El usuario {id} se ha actualizado exitosamente") # Manteniendo tu estilo de print
    except Exception as e:
        print(" Error al actualizar usuario\n", e)
def eliminar_orden_produccion():
    print("\n=== Eliminar Orden de Producción ===")
    try:
        orden_dao = OrdenProduccionDAO()
        ver_ordenes_produccion()
        
        id = int(input("Escribe el ID de la orden que deseas eliminar: "))
        orden_dao.eliminar(id)
        print(f"¡La orden {id} ha sido eliminada con éxito!")
    except Exception as e:
        print("Error al eliminar la orden de producción:\n", e)


#Menu Submenu
def submenu(modulo, f_ver, f_ins, f_act=None, f_elim=None, es_movimiento=False):
    while True:
        print(f"\n--- Panel de Gestión: {modulo} ---")
        print("1. Consultar listado completo")
        print("2. Registrar nuevo elemento")
        if not es_movimiento:
            print("3.Editar un registro")
            print("4.Eliminar un registro")
        print("5. Volver al Menú Anterior")
        
        try:
            opc = int(input("Selecciona una opción (1-5): "))
            match opc:
                case 1: f_ver()
                case 2: f_ins()
                case 3 if not es_movimiento: f_act()
                case 4 if not es_movimiento: f_elim()
                case 5: break
                case _: print("Opción no válida.")
        except ValueError:
            print("Por favor, ingresa solo dígitos enteros.")

def main():
    while True:
        print("\n=========================================")
        print(" SISTEMA DE GESTIÓN DE PRODUCCIÓN TEXTIL ")
        print("=========================================")
        print("1. Usuarios")
        print("2.Clientes ")
        print("3. Productos")
        print("4. Pedidos")
        print("5.Ordenes Producción")
        print("6. Salir de la Aplicación")

        try:
            opcion = int(input("\nSelecciona un submódulo (1-6): "))
            match opcion:
                case 1:
                    submenu("Usuarios", ver_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario)
                case 2:
                    submenu("Clientes", ver_clientes, insertar_cliente, actualizar_cliente, eliminar_cliente)
                case 3:
                    submenu("Productos", ver_productos, insertar_producto, actualizar_producto, eliminar_producto)
                case 4:
                 
                    submenu("Pedidos", ver_pedidos, insertar_pedido, actualizar_pedido, eliminar_pedido)
                case 5:
                    submenu("Órdenes de Producción", ver_ordenes_produccion, insertar_orden_produccion, actualizar_orden_produccion,eliminar_orden_produccion)
                case 6:
                    print("Cerrando sesión en SGT Integrador... ¡Hasta luego, bro!")
                    break
                case _:
                    print("Opción fuera de rango. Elige entre 1 y 6.")
        except ValueError:
            print("Entrada no válida. Elige una opción del menú numérico.")

if __name__ == "__main__":
    main()