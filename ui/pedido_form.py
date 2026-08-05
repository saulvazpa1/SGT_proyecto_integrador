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

    # ---------- DROPDOWNS (limpios) ----------
    cliente_dropdown = ft.Dropdown(
        label="Cliente",
        hint_text="Selecciona un cliente",
        width=320,
        border_radius=6,
        value=str(pedido.cliente_id) if editando else None,
        options=[ft.dropdown.Option(key=str(cid), text=nombre) for cid, nombre in clientes],
    )

    producto_dropdown = ft.Dropdown(
        label="Producto",
        hint_text="Selecciona un producto",
        width=320,
        border_radius=6,
        value=str(pedido.producto_id) if editando else None,
        options=[ft.dropdown.Option(key=str(pid), text=nombre) for pid, nombre, _ in productos],
    )

    vendedor_dropdown = ft.Dropdown(
        label="Vendedor",
        hint_text="Selecciona un vendedor",
        width=320,
        border_radius=6,
        value=str(pedido.vendedor_id) if editando else None,
        options=[ft.dropdown.Option(key=str(uid), text=nombre) for uid, nombre in vendedores],
    )

    estados_disponibles = list(ESTADOS_SUGERIDOS)
    if editando and pedido.pedido_estado and pedido.pedido_estado not in estados_disponibles:
        estados_disponibles = [pedido.pedido_estado] + estados_disponibles

    estado_dropdown = ft.Dropdown(
        label="Estado",
        hint_text="Selecciona el estado",
        width=320,
        border_radius=6,
        value=pedido.pedido_estado if editando else "Pendiente",
        options=[ft.dropdown.Option(key=e, text=e) for e in estados_disponibles],
    )

    # ---------- CANTIDAD CON CONTADOR ----------
    cantidad_input = ft.TextField(
        value=str(pedido.pedido_cantidad) if editando else "1",
        width=70,
        text_align=ft.TextAlign.CENTER,
        border_radius=6,
    )

    def _leer_cantidad():
        try:
            return int(cantidad_input.value)
        except (TypeError, ValueError):
            return 1

    def decrementar_cantidad(e):
        nuevo = max(1, _leer_cantidad() - 1)
        cantidad_input.value = str(nuevo)
        if page:
            page.update()

    def incrementar_cantidad(e):
        cantidad_input.value = str(_leer_cantidad() + 1)
        if page:
            page.update()

    contador_cantidad = ft.Column(
        controls=[
            ft.Text("Cantidad:", size=12, color=ft.Colors.BLUE_GREY_700),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                        icon_size=22,
                        tooltip="Quitar uno",
                        on_click=decrementar_cantidad,
                    ),
                    cantidad_input,
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                        icon_size=22,
                        tooltip="Agregar uno",
                        on_click=incrementar_cantidad,
                    ),
                ],
                spacing=5,
            ),
        ],
        spacing=2,
        width=320,
    )

    # ---------- TOTAL ----------
    total_input = ft.TextField(
        label="Total",
        hint_text="Se calcula automáticamente",
        width=320,
        border_radius=6,
        prefix=ft.Text("$ "),
        value=str(pedido.pedido_total) if editando else "",
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    def calcular_total(e):
        producto_id = producto_dropdown.value
        try:
            cantidad = int(cantidad_input.value or 1)
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
        total_input.value = f"{round(precio * cantidad, 2):.2f}"
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

        if not cliente_dropdown.value:
            mensaje.value = "Selecciona un cliente"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if not producto_dropdown.value:
            mensaje.value = "Selecciona un producto"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if not vendedor_dropdown.value:
            mensaje.value = "Selecciona un vendedor"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            cantidad_num = int(cantidad_input.value)
        except ValueError:
            mensaje.value = "La cantidad debe ser un número entero"
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

        try:
            total_num = float(total_input.value or 0)
        except ValueError:
            mensaje.value = "El total no es válido. Usa el botón Calcular total"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if total_num <= 0:
            mensaje.value = "El total debe ser mayor a 0. Calcula el total primero."
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

    # ---------- ENCABEZADO ----------
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

    # ---------- COLUMNAS ----------
    columna_izquierda = ft.Column(
        controls=[
            cliente_dropdown,
            producto_dropdown,
            vendedor_dropdown,
        ],
        spacing=15,
    )

    columna_derecha = ft.Column(
        controls=[
            contador_cantidad,
            total_input,
            boton_calcular,
            estado_dropdown,
        ],
        spacing=12,
    )

    # ---------- CUERPO ----------
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
    )

    # ---------- PIE ----------
    pie = ft.Container(
        padding=ft.Padding.only(left=30, right=30, bottom=20, top=5),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    on_click=lambda e: regresar(),
                ),
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
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            controls=[encabezado, cuerpo, pie],
            spacing=0,
        ),
    )