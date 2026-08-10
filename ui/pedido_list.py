import flet as ft
from dao.pedido_dao import PedidoDAO
from database.conexion import Conexion
from ui.pedido_form import pedido_form
from ui.colores import *
from ui.componentes import mostrar_notificacion
from ui.notificaciones import agregar_notificacion


def pedidos_list(page: ft.Page, puede_editar: bool = True):
    """
    puede_editar=True  -> se ven los botones Agregar / Editar / Eliminar (Vendedor)
    puede_editar=False -> solo lectura, sin esos botones (Administrador y demás roles)
    """

    todos_los_pedidos = []
    pedidos_filtrados = []

    mapa_clientes = {}
    mapa_vendedores = {}
    mapa_productos = {}

    TODOS_KEY = "__TODOS__"

    columnas = [
        ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Vendedor", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, size=16)),
        ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD, size=16)),
    ]
    columnas.append(ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, size=16)))

    tabla = ft.DataTable(
        show_checkbox_column=False,
        columns=columnas,
        rows=[],
    )

    buscador = ft.TextField(
        label="Buscar pedido",
        hint_text="Busca por cliente, vendedor o producto...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    filtro = ft.Dropdown(
        label="Filtrar por estado",
        width=220,
        value=TODOS_KEY,
        options=[ft.dropdown.Option(key=TODOS_KEY, text="Todos")],
    )

    def cargar_catalogos():
        """Carga nombres de clientes, vendedores y productos para mostrarlos en vez del ID crudo."""
        nonlocal mapa_clientes, mapa_vendedores, mapa_productos
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT cliente_id, cliente_nombre FROM clientes")
            mapa_clientes = {str(cid): nombre for cid, nombre in cursor.fetchall()}

            cursor.execute("SELECT usuario_id, usuario_nombre, usuario_apellidop FROM usuarios")
            mapa_vendedores = {
                str(uid): f"{nombre} {apellido}".strip()
                for uid, nombre, apellido in cursor.fetchall()
            }

            cursor.execute("SELECT producto_id, producto_nombre FROM productos")
            mapa_productos = {str(pid): nombre for pid, nombre in cursor.fetchall()}

            cursor.close()
            conexion.close()
        except Exception as ex:
            mostrar_notificacion(page, "Error de conexión", str(ex), "error")

    def nombre_cliente(pedido):
        nombre = mapa_clientes.get(str(pedido.cliente_id))
        return f"#{pedido.cliente_id} — {nombre}" if nombre else f"#{pedido.cliente_id}"

    def nombre_vendedor(pedido):
        nombre = mapa_vendedores.get(str(pedido.vendedor_id))
        return f"#{pedido.vendedor_id} — {nombre}" if nombre else f"#{pedido.vendedor_id}"

    def nombre_producto(pedido):
        nombre = mapa_productos.get(str(pedido.producto_id))
        return f"#{pedido.producto_id} — {nombre}" if nombre else f"#{pedido.producto_id}"

    def cargar_desde_bd():
        nonlocal todos_los_pedidos
        try:
            todos_los_pedidos = PedidoDAO().obtener_todos()

            estados_unicos = sorted({str(p.pedido_estado) for p in todos_los_pedidos})
            filtro.options = [
                ft.dropdown.Option(key=TODOS_KEY, text="Todos"),
                *[ft.dropdown.Option(key=estado, text=estado) for estado in estados_unicos],
            ]
        except Exception as ex:
            mostrar_notificacion(page, "Error de conexión", str(ex), "error")

    def abrir_agregar(e):
        def cerrar_dialogo(texto_exito=None):
            page.pop_dialog()
            cargar_catalogos()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
            if texto_exito:
                agregar_notificacion(texto_exito)
                mostrar_notificacion(page, "Se guardó correctamente", texto_exito, "exito")

        dialogo = ft.AlertDialog(
            modal=True,
            content=pedido_form(cerrar_dialogo, page=page),
        )
        page.show_dialog(dialogo)

    def ver_detalles(pedido):
        try:
            total_texto = f"${float(pedido.pedido_total):,.2f}"
        except (TypeError, ValueError):
            total_texto = f"${pedido.pedido_total}"

        def cerrar(e=None):
            page.pop_dialog()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Pedido #{pedido.pedido_id}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Cliente: {nombre_cliente(pedido)}"),
                    ft.Text(f"Vendedor: {nombre_vendedor(pedido)}"),
                    ft.Text(f"Producto: {nombre_producto(pedido)}"),
                    ft.Text(f"Cantidad: {pedido.pedido_cantidad}"),
                    ft.Text(f"Total: {total_texto}"),
                    ft.Text(f"Estado: {pedido.pedido_estado}"),
                    ft.Text(f"Fecha: {pedido.pedido_fecha}"),
                ],
                spacing=8,
                tight=True,
            ),
            actions=[ft.TextButton("Cerrar", on_click=cerrar)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialogo)

    def abrir_editar(pedido):
     
        try:
            pedido_completo = PedidoDAO().obtener_por_id(pedido.pedido_id)
        except Exception as ex:
            mostrar_notificacion(page, "Error al cargar el pedido", str(ex), "error")
            return

        if pedido_completo is None:
            mostrar_notificacion(page, "No se encontró el pedido", "", "error")
            return

        def cerrar_dialogo(texto_exito=None):
            page.pop_dialog()
            cargar_catalogos()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
            if texto_exito:
                agregar_notificacion(texto_exito)
                mostrar_notificacion(page, "Se guardó correctamente", texto_exito, "exito")

        dialogo = ft.AlertDialog(
            modal=True,
            content=pedido_form(cerrar_dialogo, pedido=pedido_completo, page=page),
        )
        page.show_dialog(dialogo)

    def confirmar_eliminar(pedido):
        def eliminar_confirmado(e):
            try:
                PedidoDAO().eliminar(pedido.pedido_id)
                page.pop_dialog()
                cargar_desde_bd()
                aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)

                texto = f"Pedido #{pedido.pedido_id} eliminado"
                agregar_notificacion(texto)
                mostrar_notificacion(page, "Pedido eliminado", texto, "error")
            except Exception as ex:
                page.pop_dialog()
                mostrar_notificacion(page, "Error al eliminar", str(ex), "error")

        def cancelar_eliminar(e):
            page.pop_dialog()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Seguro que deseas eliminar el pedido #{pedido.pedido_id}? "
                "Esta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminar),
                ft.ElevatedButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=eliminar_confirmado,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialogo_confirmacion)

    filas_por_pagina = 5
    pagina_actual = 1

    def total_paginas():
        if not pedidos_filtrados:
            return 1
        paginas = len(pedidos_filtrados) // filas_por_pagina
        if len(pedidos_filtrados) % filas_por_pagina:
            paginas += 1
        return max(paginas, 1)

    paginador = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    def render_pagina():
        inicio = (pagina_actual - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina

        tabla.rows = [
            construir_fila(p)
            for p in pedidos_filtrados[inicio:fin]
        ]

        paginador.controls.clear()

        paginador.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                disabled=pagina_actual == 1,
                on_click=ir_pagina_anterior,
            )
        )

        for i in range(1, total_paginas() + 1):
            paginador.controls.append(
                ft.Container(
                    width=36,
                    height=36,
                    border_radius=8,
                    bgcolor=AZUL if i == pagina_actual else "#D9DCE3",
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=lambda e, p=i: cambiar_pagina(p),
                    content=ft.Text(
                        str(i),
                        color="white" if i == pagina_actual else "black",
                        weight=ft.FontWeight.BOLD,
                    ),
                )
            )

        paginador.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                disabled=pagina_actual == total_paginas(),
                on_click=ir_pagina_siguiente,
            )
        )

        page.update()

    def ir_pagina_anterior(e):
        nonlocal pagina_actual
        if pagina_actual > 1:
            pagina_actual -= 1
            render_pagina()

    def ir_pagina_siguiente(e):
        nonlocal pagina_actual
        if pagina_actual < total_paginas():
            pagina_actual += 1
            render_pagina()

    def cambiar_pagina(numero):
        nonlocal pagina_actual
        pagina_actual = numero
        render_pagina()

    def construir_fila(pedido):
        try:
            total_texto = f"${float(pedido.pedido_total):,.2f}"
        except (TypeError, ValueError):
            total_texto = f"${pedido.pedido_total}"

        celdas = [
            ft.DataCell(ft.Text(str(pedido.pedido_id))),
            ft.DataCell(ft.Text(nombre_cliente(pedido))),
            ft.DataCell(ft.Text(nombre_vendedor(pedido))),
            ft.DataCell(ft.Text(nombre_producto(pedido))),
            ft.DataCell(ft.Text(str(pedido.pedido_cantidad))),
            ft.DataCell(ft.Text(total_texto)),
            ft.DataCell(ft.Text(str(pedido.pedido_estado))),
            ft.DataCell(ft.Text(str(pedido.pedido_fecha))),
        ]

        if puede_editar:
            celdas.append(
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar",
                            icon_color=ft.Colors.BLUE_700,
                            bgcolor=ft.Colors.BLUE_50,
                            style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                             ),
                            on_click=lambda e, p=pedido: abrir_editar(p),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_700,
                            bgcolor=ft.Colors.RED_50,
                            tooltip="Eliminar",
                            style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                             ),
                            on_click=lambda e, p=pedido: confirmar_eliminar(p),
                        ),
                    ])
                )
            )
        else:
            celdas.append(
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY,
                        icon_color=ft.Colors.BLUE_GREY_400,
                        tooltip="Ver detalles",
                        on_click=lambda e, p=pedido: ver_detalles(p),
                    )
                )
            )

        return ft.DataRow(cells=celdas)

    def aplicar_filtro(texto="", tipo_filtro=TODOS_KEY):
        nonlocal pedidos_filtrados, pagina_actual
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = tipo_filtro or TODOS_KEY

        resultado = []
        for pedido in todos_los_pedidos:
            if opcion_filtro != TODOS_KEY and str(pedido.pedido_estado) != opcion_filtro:
                continue

            campos = " ".join([
                nombre_cliente(pedido),
                nombre_vendedor(pedido),
                nombre_producto(pedido),
            ]).lower()

            if not texto_busqueda or texto_busqueda in campos:
                resultado.append(pedido)

        pedidos_filtrados = resultado
        pagina_actual = 1
        render_pagina()

    buscador.on_change = lambda e: aplicar_filtro(
        texto=e.control.value,
        tipo_filtro=filtro.value
    )

    def cambiar_filtro(e):
        aplicar_filtro(
            texto=buscador.value,
            tipo_filtro=e.control.value
        )

    filtro.on_select = cambiar_filtro

    cargar_catalogos()
    cargar_desde_bd()
    aplicar_filtro(texto="", tipo_filtro=TODOS_KEY)

    controles_encabezado = [buscador, filtro]
    if puede_editar:
        controles_encabezado.append(
            ft.ElevatedButton(
                "Agregar pedido",
                bgcolor=AZUL,
                color=ft.Colors.WHITE,
                icon=ft.Icons.ADD,
                tooltip="Agregar pedido",
                on_click=abrir_agregar,
            )
        )
    else:
        controles_encabezado.append(
            ft.Container(
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                bgcolor=ft.Colors.BLUE_GREY_100,
                border_radius=8,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCK, size=16, color=ft.Colors.BLUE_GREY_600),
                        ft.Text("Solo lectura", color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                ),
            )
        )

    return ft.Column(
        controls=[
            ft.Text("Pedidos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=controles_encabezado,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=20,
            ),
            tabla,
            paginador,
        ],
        spacing=20,
        expand=True,
    )