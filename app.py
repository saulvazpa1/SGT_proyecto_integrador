# app.py
from dao.usuario_dao import UsuarioDAO #Carpeta/archivo/clase
from models.usuario import Usuario
from dao.cliente_dao import ClienteDAO
from dao.producto_dao import ProductoDAO
from models.producto import Producto
from dao.pagos_dao import PagosDAO
from models.pago import Pago
from dao.pedidos_dao import PedidosDAO
from models.pedido import Pedido
from dao.roles_dao import RolesDAO
from models.rol import Rol
from dao.material_dao import MaterialDAO
from models.material import Material
from dao.entrada_material_dao import EntradaMaterialDAO #Carpeta/archivo/clase



def ver_usuarios():
    try:
        usuario_dao = UsuarioDAO() #tiene todo de Usuario Dao

        usuarios = usuario_dao.obtener_todos()

        print("=== Usuarios en el Sistema ===")

    #si es que no hay usuarios
        if len(usuarios) == 0:
            print("No hay usuarios registrados")
        else:
            for usuario in usuarios:
                print("-------------------------------------------")

                print(
                    f"ID:{usuario.usuario_id},Nombre:{usuario.usuario_nombre},"
                    f"Apellido Paterno:{usuario.usuario_apellidop},Apellido Materno:{usuario.usuario_apellidom},"
                    f"Teléfono:{usuario.usuario_telefono},Correo:{usuario.usuario_correo},"
                    f"Password:{usuario.usuario_password},Rol ID:{usuario.rol_id}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

def ver_clientes():
    try:
        cliente_dao = ClienteDAO()#tiene todo de Cliente Dao

        clientes = cliente_dao.obtener_todos()

        print("=== Clientes en el Sistema ===")

    #si es que no hay clientes
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
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

def ver_entradas_materiales():
    try:
        entrada_dao = EntradaMaterialDAO() #tiene todo de EntradaMaterialDAO

        entradas = entrada_dao.obtener_todos()

        print("=== Entradas de Materiales en el Sistema ===")

        #si es que no hay entradas
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
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

# app.py
from dao.material_dao import MaterialDAO
from models.material import Material

def ver_materiales():
    try:
        material_dao = MaterialDAO()
        materiales = material_dao.obtener_todos()

        print("=== Materiales en Inventario ===")

        if len(materiales) == 0:
            print("No hay materiales registrados")
        else:
            for mat in materiales:
                print("-------------------------------------------")
                print(
                    f"ID:{mat.material_id}, Nombre:{mat.material_nombre},"
                    f" Tipo:{mat.material_tipo}, Color:{mat.material_color},"
                    f" Cantidad:{mat.material_cantidad} {mat.material_unidad},"
                    f" Marca:{mat.material_marca}, Precio:${mat.material_precio}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

# ==========================================
# 5. SUBMÓDULO: PRODUCTOS
# ==========================================

def ver_productos():
    try:
        producto_dao = ProductoDAO()  # tiene todo de ProductoDAO
        productos = producto_dao.obtener_todos()

        print("\n=== Productos Registrados ===")

        if len(productos) == 0:
            print("No hay productos registrados")
        else:
            for producto in productos:
                print("-------------------------------------------")
                print(
                    f"ID:{producto.producto_id}, "
                    f"Nombre:{producto.producto_nombre}, "
                    f"Categoría:{producto.producto_categoria}, "
                    f"Precio:{producto.producto_precio}, "
                    f"Stock:{producto.producto_stock}, "
                    f"Descripción:{producto.producto_descripcion}, "
                    f"Unidad:{producto.producto_unidad_medida}, "
                    f"Color:{producto.producto_color}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

def insertar_producto():
    nombre = input("Escribe el nombre del producto: ")
    categoria = input("Escribe la categoría: ")
    precio = float(input("Escribe el precio: "))
    stock = int(input("Escribe el stock: "))
    descripcion = input("Escribe la descripción: ")
    unidad = input("Escribe la unidad de medida: ")
    color = input("Escribe el color: ")

    try:
        producto_dao = ProductoDAO()
        id = producto_dao.obtener_ultimo_id() + 1

        producto = Producto(
            id,
            nombre,
            categoria,
            precio,
            stock,
            descripcion,
            unidad,
            color
        )

        producto_dao.insertar(producto)
        print("Inserción realizada con éxito")

    except Exception as e:
        print("Error al insertar un nuevo producto")
        print(e)


def actualizar_producto():
    print("Selecciona el producto a actualizar")

    try:
        producto_dao = ProductoDAO()

        ver_productos()

        id = int(input("Escribe el ID del producto a actualizar: "))
        nombre = input("Escribe el nuevo nombre: ")
        categoria = input("Escribe la nueva categoría: ")
        precio = float(input("Escribe el nuevo precio: "))
        stock = int(input("Escribe el nuevo stock: "))
        descripcion = input("Escribe la nueva descripción: ")
        unidad = input("Escribe la nueva unidad de medida: ")
        color = input("Escribe el nuevo color: ")

        producto = Producto(
            id,
            nombre,
            categoria,
            precio,
            stock,
            descripcion,
            unidad,
            color
        )

        producto_dao.actualizar(producto)

        print(f"El producto {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar producto")
        print(e)


def eliminar_producto():
    try:
        producto_dao = ProductoDAO()

        print("Lista de productos registrados:")

        ver_productos()

        id = int(input("Escribe el ID del producto a eliminar: "))

        producto_dao.eliminar(id)

        print(f"El producto {id} ha sido eliminado con éxito")

    except Exception as e:
        print("Error al eliminar el producto")
        print(e)

# ==========================================
# 6. SUBMÓDULO: PAGOS
# ==========================================

def ver_pagos():
    try:
        pagos_dao = PagosDAO()  # tiene todo de PagosDAO
        pagos = pagos_dao.obtener_todos()

        print("\n=== Pagos Registrados ===")

        if len(pagos) == 0:
            print("No hay pagos registrados")
        else:
            for pago in pagos:
                print("-------------------------------------------")
                print(
                    f"ID Pago:{pago.pago_id}, "
                    f"ID Pedido:{pago.pedido_id}, "
                    f"Monto:${pago.pago_monto}, "
                    f"Fecha:{pago.pago_fecha}, "
                    f"Método:{pago.pago_metodo}"
                )
                print("-------------------------------------------")

        print("\n Conexión exitosa ala base de datos")

    except Exception as e:
        print("Error:")
        print(e)


def insertar_pago():

    pedido_id = int(input("Escribe el ID del pedido: "))
    monto = float(input("Escribe el monto del pago: "))
    fecha = input("Escribe la fecha del pago (AAAA-MM-DD): ")
    metodo = input("Escribe el método de pago: ")

    try:

        pagos_dao = PagosDAO()

        id = pagos_dao.obtener_ultimo_id() + 1

        pago = Pago(
            id,
            pedido_id,
            monto,
            fecha,
            metodo
        )

        pagos_dao.insertar(pago)

        print("Inserción realizada con éxito")

    except Exception as e:
        print("Error al insertar un nuevo pago")
        print(e)


def actualizar_pago():

    print("Selecciona el pago a actualizar")

    try:

        pagos_dao = PagosDAO()

        ver_pagos()

        id = int(input("Escribe el ID del pago a actualizar: "))
        pedido_id = int(input("Escribe el nuevo ID del pedido: "))
        monto = float(input("Escribe el nuevo monto: "))
        fecha = input("Escribe la nueva fecha: ")
        metodo = input("Escribe el nuevo método de pago: ")

        pago = Pago(
            id,
            pedido_id,
            monto,
            fecha,
            metodo
        )

        pagos_dao.actualizar(pago)

        print(f"El pago {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar pago")
        print(e)


def eliminar_pago():

    try:

        pagos_dao = PagosDAO()

        print("Lista de pagos registrados:")

        ver_pagos()

        id = int(input("Escribe el ID del pago a eliminar: "))

        pagos_dao.eliminar(id)

        print(f"El pago {id} ha sido eliminado con éxito")

    except Exception as e:
        print("Error al eliminar el pago")
        print(e)

# ==========================================
# 7. SUBMÓDULO: PEDIDOS
# ==========================================

def ver_pedidos():
    try:
        pedidos_dao = PedidosDAO()  # tiene todo de PedidosDAO
        pedidos = pedidos_dao.obtener_todos()

        print("\n=== Pedidos Registrados ===")

        if len(pedidos) == 0:
            print("No hay pedidos registrados")
        else:
            for pedido in pedidos:
                print("-------------------------------------------")
                print(
                    f"ID:{pedido.pedido_id}, Cliente:{pedido.cliente_id}, "
                    f"Vendedor:{pedido.vendedor_id}, Producto:{pedido.producto_id}, "
                    f"Cantidad:{pedido.pedido_cantidad}, Total:${pedido.pedido_total}, "
                    f"Estado:{pedido.pedido_estado}, Fecha:{pedido.pedido_fecha}"
                )
                print("-------------------------------------------")

        print("\n Conexión exitosa ala base de datos")

    except Exception as e:
        print("Error:")
        print(e)


def insertar_pedido():

    cliente_id = int(input("Escribe el ID del cliente: "))
    vendedor_id = int(input("Escribe el ID del vendedor: "))
    producto_id = int(input("Escribe el ID del producto: "))
    cantidad = int(input("Escribe la cantidad: "))
    total = float(input("Escribe el total: "))
    estado = input("Escribe el estado del pedido: ")
    fecha = input("Escribe la fecha del pedido (AAAA-MM-DD): ")

    try:
        pedidos_dao = PedidosDAO()

        id = pedidos_dao.obtener_ultimo_id() + 1

        pedido = Pedido(
            id,
            cliente_id,
            vendedor_id,
            producto_id,
            cantidad,
            total,
            estado,
            fecha
        )

        pedidos_dao.insertar(pedido)

        print("Inserción realizada con éxito")

    except Exception as e:
        print("Error al insertar un nuevo pedido")
        print(e)


def actualizar_pedido():

    print("Selecciona el pedido a actualizar")

    try:
        pedidos_dao = PedidosDAO()

        ver_pedidos()

        id = int(input("Escribe el ID del pedido a actualizar: "))
        cliente_id = int(input("Escribe el nuevo ID del cliente: "))
        vendedor_id = int(input("Escribe el nuevo ID del vendedor: "))
        producto_id = int(input("Escribe el nuevo ID del producto: "))
        cantidad = int(input("Escribe la nueva cantidad: "))
        total = float(input("Escribe el nuevo total: "))
        estado = input("Escribe el nuevo estado: ")
        fecha = input("Escribe la nueva fecha: ")

        pedido = Pedido(
            id,
            cliente_id,
            vendedor_id,
            producto_id,
            cantidad,
            total,
            estado,
            fecha
        )

        pedidos_dao.actualizar(pedido)

        print(f"El pedido {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar pedido")
        print(e)


def eliminar_pedido():

    try:
        pedidos_dao = PedidosDAO()

        print("Lista de pedidos registrados:")

        ver_pedidos()

        id = int(input("Escribe el ID del pedido a eliminar: "))

        pedidos_dao.eliminar(id)

        print(f"El pedido {id} ha sido eliminado con éxito")

    except Exception as e:
        print("Error al eliminar el pedido")
        print(e)

# ==========================================
# 8. SUBMÓDULO: ROLES
# ==========================================

def ver_roles():
    try:
        roles_dao = RolesDAO()
        roles = roles_dao.obtener_todos()

        print("\n=== Roles Registrados ===")

        if len(roles) == 0:
            print("No hay roles registrados")
        else:
            for rol in roles:
                print("-------------------------------------------")
                print(
                    f"ID:{rol.rol_id}, "
                    f"Nombre:{rol.rol_nombre}, "
                    f"Permisos:{rol.rol_permisos}"
                )
                print("-------------------------------------------")

        print("\nConexión exitosa a la base de datos")

    except Exception as e:
        print("Error:")
        print(e)


def insertar_rol():

    nombre = input("Escribe el nombre del rol: ")
    permisos = input("Escribe los permisos: ")

    try:
        roles_dao = RolesDAO()

        id = roles_dao.obtener_ultimo_id() + 1

        rol = Rol(
            id,
            nombre,
            permisos
        )

        roles_dao.insertar(rol)

        print("Inserción realizada con éxito")

    except Exception as e:
        print("Error al insertar un nuevo rol")
        print(e)


def actualizar_rol():

    print("Selecciona el rol a actualizar")

    try:

        roles_dao = RolesDAO()

        ver_roles()

        id = int(input("Escribe el ID del rol a actualizar: "))
        nombre = input("Escribe el nuevo nombre: ")
        permisos = input("Escribe los nuevos permisos: ")

        rol = Rol(
            id,
            nombre,
            permisos
        )

        roles_dao.actualizar(rol)

        print(f"El rol {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar rol")
        print(e)


def eliminar_rol():

    try:

        roles_dao = RolesDAO()

        print("Lista de roles registrados:")

        ver_roles()

        id = int(input("Escribe el ID del rol a eliminar: "))

        roles_dao.eliminar(id)

        print(f"El rol {id} ha sido eliminado con éxito")

    except Exception as e:
        print("Error al eliminar el rol")
        print(e)

def submenu(nombre, ver, insertar=None, actualizar=None, eliminar=None):

    while True:

        print(f"\n===== MÓDULO: {nombre} =====")
        print("1. Ver registros")

        if insertar is not None:
            print("2. Insertar registro")

        if actualizar is not None:
            print("3. Actualizar registro")

        if eliminar is not None:
            print("4. Eliminar registro")

        print("5. Regresar al menú principal")

        opcion = int(input("Seleccione una opción: "))

        match opcion:

            case 1:
                ver()

            case 2:
                if insertar is not None:
                    insertar()

            case 3:
                if actualizar is not None:
                    actualizar()

            case 4:
                if eliminar is not None:
                    eliminar()

            case 5:
                break

            case _:
                print("Opción no válida.")


def main():

    while True:

        print("\n=========================================")
        print(" SISTEMA DE GESTIÓN DE PRODUCCIÓN TEXTIL ")
        print("=========================================")
        print("1. Usuarios")
        print("2. Clientes")
        print("3. Materiales")
        print("4. Entradas de Material")
        print("5. Productos")
        print("6. Pedidos")
        print("7. Pagos")
        print("8. Roles")
        opcion = int(input("Seleccione una opción: "))

        match opcion:

            case 1:
                submenu(
                    "Usuarios",
                    ver_usuarios
                )

            case 2:
                submenu(
                    "Clientes",
                    ver_clientes
                )

            case 3:
                submenu(
                    "Materiales",
                    ver_materiales
                )

            case 4:
                submenu(
                    "Entradas de Material",
                    ver_entradas_materiales
                )

            case 5:
                submenu(
                    "Productos",
                    ver_productos,
                    insertar_producto,
                    actualizar_producto,
                    eliminar_producto
                )

            case 6:
                submenu(
                    "Pedidos",
                    ver_pedidos,
                    insertar_pedido,
                    actualizar_pedido,
                    eliminar_pedido
                )

            case 7:
                submenu(
                    "Pagos",
                    ver_pagos,
                    insertar_pago,
                    actualizar_pago,
                    eliminar_pago
                )

            case 8:
                submenu(
                    "Roles",
                    ver_roles,
                    insertar_rol,
                    actualizar_rol,
                    eliminar_rol
                )

            case 9:
                print("Gracias por utilizar el sistema.")
                break

            case _:
                print("Opción inválida.")
if __name__ == "__main__":
    main()