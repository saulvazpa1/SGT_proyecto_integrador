import flet as ft
from dao.pedido_dao import PedidoDAO
from ui.pedido_form import pedido_form
from ui.colores import *


def pedidos_list(page: ft.Page):

    todos_los_pedidos = []
    pedidos_filtrados = []

    TODOS_KEY = "__TODOS__"

    tabla = ft.DataTable(
        show_checkbox_column=False,
        columns=[
            ft.DataColumn(
                ft.Text(
                    "ID",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Cliente",
                    weight=ft.FontWeight.BOLD,
                    size=16,                    
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Vendedor",
                    weight=ft.FontWeight.BOLD,
                    size=16,                    
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Producto",
                    weight=ft.FontWeight.BOLD,
                    size=16,                    
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Cantidad",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Total",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Estado",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Fecha",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

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
            mensaje.value = f"Error BD: {ex}"
            mensaje.color = ft.Colors.RED

    def abrir_agregar(e):
        def cerrar_dialogo(texto_exito=None):
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
            if texto_exito:
                mensaje.value = texto_exito
                mensaje.color = ft.Colors.GREEN
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            content=pedido_form(cerrar_dialogo, page=page),
        )
        page.show_dialog(dialogo)

    def construir_fila(pedido):
        try:
            total_texto = f"${float(pedido.pedido_total):,.2f}"
        except (TypeError, ValueError):
            total_texto = f"${pedido.pedido_total}"

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(pedido.pedido_id))),
                ft.DataCell(ft.Text(str(pedido.cliente_id))),
                ft.DataCell(ft.Text(str(pedido.vendedor_id))),
                ft.DataCell(ft.Text(str(pedido.producto_id))),
                ft.DataCell(ft.Text(str(pedido.pedido_cantidad))),
                ft.DataCell(ft.Text(total_texto)),
                ft.DataCell(ft.Text(str(pedido.pedido_estado))),
                ft.DataCell(ft.Text(str(pedido.pedido_fecha))),
            ]
        )

    def aplicar_filtro(texto="", tipo_filtro=TODOS_KEY):
        nonlocal pedidos_filtrados
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = tipo_filtro or TODOS_KEY

        resultado = []
        for pedido in todos_los_pedidos:
            if opcion_filtro != TODOS_KEY and str(pedido.pedido_estado) != opcion_filtro:
                continue

            campos = " ".join([
                str(pedido.cliente_id),
                str(pedido.vendedor_id),
                str(pedido.producto_id),
            ]).lower()

            if not texto_busqueda or texto_busqueda in campos:
                resultado.append(pedido)

        pedidos_filtrados = resultado
        tabla.rows = [construir_fila(p) for p in pedidos_filtrados]

        if page:
            page.update()

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

    cargar_desde_bd()
    aplicar_filtro(texto="", tipo_filtro=TODOS_KEY)

    boton_agregar = ft.ElevatedButton(
        "Agregar pedido",
        bgcolor=AZUL,
        color=ft.Colors.WHITE,
        icon=ft.Icons.ADD,
        on_click=abrir_agregar,
    )

    return ft.Column(
        controls=[
            ft.Text("Pedidos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro, boton_agregar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=20,
            ),
            tabla,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )