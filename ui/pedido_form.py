from datetime import datetime
import flet as ft
from database.conexion import Conexion
from models.pedido import Pedido
from dao.pedido_dao import PedidoDAO
from ui.colores import *


ESTADOS_SUGERIDOS = ["Pendiente", "En proceso", "Completado", "Cancelado"]


def _obtener_clientes():
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT cliente_id, cliente_nombre FROM clientes ORDER BY cliente_nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def _obtener_productos():
    """(producto_id, producto_nombre, producto_precio)"""
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT producto_id, producto_nombre, producto_precio FROM productos ORDER BY producto_nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def _obtener_vendedores():
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT u.usuario_id, u.usuario_nombre, u.usuario_apellidop
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.rol_id
        WHERE r.rol_nombre ILIKE %s
        ORDER BY u.usuario_nombre
    """, ('%vendedor%',))
    filas = cursor.fetchall()

    if not filas:
        cursor.execute("SELECT usuario_id, usuario_nombre, usuario_apellidop FROM usuarios ORDER BY usuario_nombre")
        filas = cursor.fetchall()

    cursor.close()
    conexion.close()
    return [(uid, f"{nombre} {apellido}".strip()) for uid, nombre, apellido in filas]


def pedido_form(regresar, pedido=None, page=None):
    editando = pedido is not None

    clientes = _obtener_clientes()
    productos = _obtener_productos()
    vendedores = _obtener_vendedores()

    precio_por_producto = {str(pid): float(precio) for pid, _, precio in productos}

    cliente_dropdown = ft.Dropdown(
        label="Cliente:",
        width=320,
        value=str(pedido.cliente_id) if editando else None,
        options=[ft.dropdown.Option(key=str(cid), text=nombre) for cid, nombre in clientes],
    )

    producto_dropdown = ft.Dropdown(
        label="Producto:",
        width=320,
        value=str(pedido.producto_id) if editando else None,
        options=[ft.dropdown.Option(key=str(pid), text=nombre) for pid, nombre, _ in productos],
    )

    vendedor_dropdown = ft.Dropdown(
        label="Vendedor:",
        width=320,
        value=str(pedido.vendedor_id) if editando else None,
        options=[ft.dropdown.Option(key=str(uid), text=nombre) for uid, nombre in vendedores],
    )

    estados_disponibles = list(ESTADOS_SUGERIDOS)
    if editando and pedido.pedido_estado and pedido.pedido_estado not in estados_disponibles:
        estados_disponibles = [pedido.pedido_estado] + estados_disponibles

    estado_dropdown = ft.Dropdown(
        label="Estado:",
        width=320,
        value=pedido.pedido_estado if editando else "Pendiente",
        options=[ft.dropdown.Option(key=e, text=e) for e in estados_disponibles],
    )

    cantidad_input = ft.TextField(
        label="Cantidad:",
        width=320,
        border_radius=6,
        value=str(pedido.pedido_cantidad) if editando else "",
    )

    total_input = ft.TextField(
        label="Total:",
        width=320,
        border_radius=6,
        prefix=ft.Text("$"),
        value=str(pedido.pedido_total) if editando else "",
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    def calcular_total(e):
        producto_id = producto_dropdown.value
        try:
            cantidad = int(cantidad_input.value or 0)
        except ValueError:
            mensaje.value = "La cantidad debe ser un número entero"
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        if not producto_id or producto_id not in precio_por_producto:
            mensaje.value = "Selecciona un producto para calcular el total"
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        precio = precio_por_producto[producto_id]
        total_input.value = str(round(precio * cantidad, 2))
        mensaje.value = ""
        if page:
            page.update()

    boton_calcular = ft.TextButton(
        "Calcular total",
        icon=ft.Icons.CALCULATE,
        on_click=calcular_total,
    )

    def guardar_pedido(e):
        p_page = page or e.page

        if not cliente_dropdown.value or not producto_dropdown.value or not vendedor_dropdown.value or not cantidad_input.value or not total_input.value:
            mensaje.value = "Cliente, producto, vendedor, cantidad y total son obligatorios"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            cantidad_num = int(cantidad_input.value)
            total_num = float(total_input.value)
        except ValueError:
            mensaje.value = "Cantidad debe ser entero y Total debe ser numérico"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if cantidad_num <= 0:
            mensaje.value = "La cantidad debe ser mayor a 0"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if total_num <= 0:
            mensaje.value = "El total debe ser mayor a 0"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            dao = PedidoDAO()

            if editando:
                pedido_actualizado = Pedido(
                    pedido_id=pedido.pedido_id,
                    cliente_id=int(cliente_dropdown.value),
                    vendedor_id=int(vendedor_dropdown.value),
                    producto_id=int(producto_dropdown.value),
                    pedido_cantidad=cantidad_num,
                    pedido_total=total_num,
                    pedido_estado=estado_dropdown.value,
                    pedido_fecha=pedido.pedido_fecha,
                )
                dao.actualizar(pedido_actualizado)
                regresar(f"Pedido #{pedido.pedido_id} actualizado correctamente")
                return

            nuevo_id = dao.obtener_ultimo_id() + 1
            nuevo_pedido = Pedido(
                pedido_id=nuevo_id,
                cliente_id=int(cliente_dropdown.value),
                vendedor_id=int(vendedor_dropdown.value),
                producto_id=int(producto_dropdown.value),
                pedido_cantidad=cantidad_num,
                pedido_total=total_num,
                pedido_estado=estado_dropdown.value,
                pedido_fecha=datetime.now(),
            )
            dao.insertar(nuevo_pedido)
            regresar(f"Pedido #{nuevo_id} registrado correctamente")
            return

        except Exception as error:
            mensaje.value = f"Error al guardar el pedido: {error}"
            mensaje.color = ft.Colors.RED

        if p_page:
            p_page.update()

    encabezado = ft.Container(
        bgcolor=AZUL,
        padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Editar pedido" if editando else "Nuevo pedido",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: regresar(),
                ),
            ],
        ),
    )

    columna_izquierda = ft.Column(
        controls=[cliente_dropdown, producto_dropdown, vendedor_dropdown],
        spacing=15,
    )
    columna_derecha = ft.Column(
        controls=[cantidad_input, total_input, boton_calcular, estado_dropdown],
        spacing=10,
    )

    cuerpo = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Modifica los datos del pedido" if editando else "Captura los datos del nuevo pedido",
                    size=14,
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Row(
                    controls=[columna_izquierda, columna_derecha],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
        height=420,
    )

    pie = ft.Container(
        padding=ft.Padding.only(left=30, right=30, bottom=20, top=5),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton("Cancelar", icon=ft.Icons.CLOSE, on_click=lambda e: regresar()),
                ft.ElevatedButton(
                    "Guardar cambios" if editando else "Registrar pedido",
                    icon=ft.Icons.SAVE,
                    bgcolor=AZUL,
                    color=ft.Colors.WHITE,
                    on_click=guardar_pedido,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Container(
        width=720,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26, offset=ft.Offset(0, 4)),
        content=ft.Column(controls=[encabezado, cuerpo, pie], spacing=0),
    )