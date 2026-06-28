from database.conexion import Conexion    # Carpeta/archivo/clase 
from models.usuario import Usuario
from models.cliente import Cliente
from models.material import Material
from models.entrada_material import EntradaMaterial

# Importaciones de la rama de Ulises
from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from dao.material_dao import MaterialDAO
from dao.entrada_material_dao import EntradaMaterialDAO
from dao.orden_produccion_dao import OrdenProduccionDAO
from dao.salida_material_dao import SalidaMaterialDAO
from dao.trabajos_asignados_dao import TrabajoAsignadoDAO

# ==========================================
# 1. SUBMÓDULO: USUARIOS (RF_02, RF_03, RF_04)
# ==========================================
def ver_usuarios():
    try:
        usuario_dao = UsuarioDAO() 
        usuarios = usuario_dao.obtener_todos()
        print("\n=== Usuarios en el Sistema ===")
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


# ==========================================
# 2. SUBMÓDULO: CLIENTES (RF_27)
# ==========================================
def ver_clientes():
    try:
        cliente_dao = ClienteDAO() 
        clientes = cliente_dao.obtener_todos()
        print("\n=== Clientes en el Sistema ===")
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
    nombre = input("Escribe el nombre o razón social del cliente: ")
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
        nombre = input("Escribe el nuevo nombre o razón social: ")
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
        print("Error al eliminar el cliente\n", e)


# ==========================================
# 3. SUBMÓDULO: MATERIALES (RF_17, RF_18)
# ==========================================
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
                    f" Cantidad:{mat.material_cantidad} {mat.material_unidad},"
                    f" Marca:{mat.material_marca}, Precio:${mat.material_precio}"
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


# ==========================================
# 4. SUBMÓDULO: ENTRADAS DE MATERIALES (RF_19)
# ==========================================
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


# ==========================================
# NUEVOS SUBMÓDULOS DEL EQUIPO (RAMA ULISES)
# ==========================================
def ver_ordenes_produccion():
    try:
        orden_produccion_dao = OrdenProduccionDAO() 
        ordenes = orden_produccion_dao.obtener_todos()
        print("\n=== Ordenes de Producción en el Sistema ===")
        if len(ordenes) == 0:
            print("No hay ordenes registradas")
        else:
            for orden in ordenes:
                print("-------------------------------------------")
                print(
                    f"ID:{orden.produccion_id}, Pedido:{orden.pedido_id},"
                    f" Producto:{orden.producto_id}, Encargado de producción:{orden.encargado_produccion_id},"
                    f" Cantidad:{orden.produccion_cantidad}, Estado de produccion:{orden.produccion_estado},"
                    f" Inicio:{orden.fecha_inicio}, Entrega:{orden.fecha_entrega},"
                    f" Tipo de tela:{orden.tela_tipo}, Ancho de tela:{orden.tela_ancho},"
                    f" Largo de tela:{orden.tela_largo}, Patron Largo:{orden.patron_largo},"
                    f" Patron ancho:{orden.patron_ancho}, Sobrante:{orden.retazo_sobrante},"
                    f" Total de tela utilizada:{orden.tela_total_utilizada}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error:", e)

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
        print("\n Conexión exitosa a la base de datos")
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


# ==========================================
# MENÚS DE CONTROL Y NAVEGACIÓN DE PANTALLAS
# ==========================================
def submenu(modulo, f_ver, f_ins, f_act=None, f_elim=None, es_movimiento=False):
    while True:
        print(f"\n--- Panel de Gestión: {modulo} ---")
        print("1. Consultar listado completo")
        print("2. Registrar nuevo elemento")
        if not es_movimiento:
            print("3. Modificar/Editar un registro")
            print("4. Dar de baja/Eliminar un registro")
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
        print("    SISTEMA DE GESTIÓN SGT INTEGRADOR    ")
        print("=========================================")
        print("1. Módulo: Usuarios del Sistema")
        print("2. Módulo: Clientes Registrados")
        print("3. Módulo: Inventario de Materiales")
        print("4. Módulo: Historial de Entradas")
        print("5. Módulo: Órdenes de Producción (Nuevo)")
        print("6. Módulo: Salidas de Materiales (Nuevo)")
        print("7. Módulo: Trabajos Asignados (Nuevo)")
        print("8. Salir de la Aplicación")

        try:
            opcion = int(input("\nSelecciona un submódulo (1-8): "))
            match opcion:
                case 1:
                    submenu("Usuarios", ver_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario)
                case 2:
                    submenu("Clientes", ver_clientes, insertar_cliente, actualizar_cliente, eliminar_cliente)
                case 3:
                    submenu("Inventario", ver_materiales, insertar_material, actualizar_material, eliminar_material)
                case 4:
                    submenu("Entradas de Almacén", ver_entradas_materiales, insertar_entrada, es_movimiento=True)
                case 5:
                    submenu("Órdenes de Producción", ver_ordenes_produccion, lambda: print("Función insertar en desarrollo..."), es_movimiento=True)
                case 6:
                    submenu("Salidas de Materiales", ver_salidas, lambda: print("Función insertar en desarrollo..."), es_movimiento=True)
                case 7:
                    submenu("Trabajos Asignados", ver_trabajos, lambda: print("Función insertar en desarrollo..."), es_movimiento=True)
                case 8:
                    print("Cerrando sesión en SGT Integrador... ¡Hasta luego BOT !")
                    break
                case _:
                    print("Opción fuera de rango. Elige entre 1 y 8.")
        except ValueError:
            print("Entrada no válida. Elige una opción del menú numérico.")

if __name__ == "__main__":
    main()
