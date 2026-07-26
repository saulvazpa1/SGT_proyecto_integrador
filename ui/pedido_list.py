import flet as ft
from dao.pedido_dao import PedidoDAO


def pedidos_list(page: ft.Page):

    todos_los_pedidos = []
    pedidos_filtrados = []

    TODOS_KEY = "__TODOS__"

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Vendedor")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Fecha")),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

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
            mensaje.value = ""

           
            estados_unicos = sorted({str(p.pedido_estado) for p in todos_los_pedidos})
            filtro.options = [
                ft.dropdown.Option(key=TODOS_KEY, text="Todos"),
                *[ft.dropdown.Option(key=estado, text=estado) for estado in estados_unicos],
            ]
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"

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

    return ft.Column(
        controls=[
            ft.Text("Pedidos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            tabla,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )