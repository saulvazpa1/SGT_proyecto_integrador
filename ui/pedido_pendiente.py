import flet as ft
from dao.pedido_dao import PedidoDAO
from ui.colores import *


def pedidos_pendientes(page: ft.Page, estado_objetivo: str = "Pendiente"):
    """
    Panel de órdenes de producción: muestra únicamente los pedidos
    cuyo estado coincide con `estado_objetivo` (por defecto "Pendiente").
    Es una vista de solo lectura pensada para el área de producción.
    """

    todos_los_pedidos = []
    pedidos_filtrados = []

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
        label="Buscar en pendientes",
        hint_text="Busca por cliente, vendedor o producto...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    contador = ft.Text(
        f"0 pedidos {estado_objetivo.lower()}",
        size=14,
        color=ft.Colors.BLUE_GREY_600,
    )

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

    def aplicar_filtro(texto=""):
        nonlocal pedidos_filtrados
        texto_busqueda = (texto or "").strip().lower()

        resultado = []
        for pedido in todos_los_pedidos:
            if str(pedido.pedido_estado) != estado_objetivo:
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
        contador.value = f"{len(pedidos_filtrados)} pedidos {estado_objetivo.lower()}"

        if page:
            page.update()

    def cargar_desde_bd():
        nonlocal todos_los_pedidos
        try:
            todos_los_pedidos = PedidoDAO().obtener_todos()
            mensaje.value = ""
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"
            mensaje.color = ft.Colors.RED

    def refrescar(e=None):
        cargar_desde_bd()
        aplicar_filtro(texto=buscador.value)
        if e is not None:
            mensaje.value = "Panel actualizado"
            mensaje.color = ft.Colors.GREEN
            page.update()

    buscador.on_change = lambda e: aplicar_filtro(texto=e.control.value)

    boton_refrescar = ft.ElevatedButton(
        "Actualizar",
        bgcolor=AZUL,
        color=ft.Colors.WHITE,
        icon=ft.Icons.REFRESH,
        on_click=refrescar,
    )

    # Carga inicial
    refrescar()

    return ft.Column(
        controls=[
            ft.Text("Panel de producción — Pedidos pendientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, boton_refrescar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=20,
            ),
            contador,
            tabla,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )