import flet as ft
from dao.pedido_dao import PedidoDAO
from ui.colores import *


def pedidos_pendientes(page: ft.Page, estado_objetivo: str = "Pendiente"):

    todos_los_pedidos = []
    pedidos_filtrados = []

    pagina_actual = 1
    filas_por_pagina = 5

    tabla = ft.DataTable(
        show_checkbox_column=False,
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Vendedor", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    buscador = ft.TextField(
        label="Buscar en pendientes",
        hint_text="Busca por cliente, vendedor o producto...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
    )

    contador = ft.Text(
        f"0 pedidos {estado_objetivo.lower()}",
        size=14,
        color=ft.Colors.BLUE_GREY_600,
    )

    paginador = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # ---------------- FUNCIONES ---------------- #

    def total_paginas():
        if not pedidos_filtrados:
            return 1
        paginas = len(pedidos_filtrados) // filas_por_pagina
        if len(pedidos_filtrados) % filas_por_pagina:
            paginas += 1
        return paginas

    def construir_fila(pedido):
        try:
            total_texto = f"${float(pedido.pedido_total):,.2f}"
        except:
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
                on_click=lambda e: cambiar_pagina(pagina_actual - 1),
            )
        )

        for i in range(1, total_paginas() + 1):
            activo = i == pagina_actual

            paginador.controls.append(
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE if activo else ft.Colors.GREY_200,
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda e, p=i: cambiar_pagina(p),
                    content=ft.Text(
                        str(i),
                        color="white" if activo else "black",
                        weight=ft.FontWeight.BOLD,
                    ),
                )
            )

        paginador.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                disabled=pagina_actual == total_paginas(),
                on_click=lambda e: cambiar_pagina(pagina_actual + 1),
            )
        )

        page.update()

    def cambiar_pagina(numero):
        nonlocal pagina_actual
        pagina_actual = numero
        render_pagina()

    def aplicar_filtro(texto=""):
        nonlocal pedidos_filtrados, pagina_actual

        texto_busqueda = (texto or "").lower()

        resultado = []
        for pedido in todos_los_pedidos:
            if str(pedido.pedido_estado) != estado_objetivo:
                continue

            campos = f"{pedido.cliente_id} {pedido.vendedor_id} {pedido.producto_id}".lower()

            if not texto_busqueda or texto_busqueda in campos:
                resultado.append(pedido)

        pedidos_filtrados = resultado
        pagina_actual = 1
        contador.value = f"{len(pedidos_filtrados)} pedidos {estado_objetivo.lower()}"
        render_pagina()

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
        if e:
            mensaje.value = "Panel actualizado"
            mensaje.color = ft.Colors.GREEN

    # ---------------- EVENTOS ---------------- #

    buscador.on_change = lambda e: aplicar_filtro(e.control.value)

    boton_refrescar = ft.ElevatedButton(
        "Actualizar",
        bgcolor=AZUL,
        color=ft.Colors.WHITE,
        icon=ft.Icons.REFRESH,
        on_click=refrescar,
    )

    # ---------------- INIT ---------------- #

    refrescar()

    return ft.Column(
        controls=[
            ft.Text("Panel de producción — Pedidos pendientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, boton_refrescar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            contador,
            tabla,
            paginador,  # 👈 AQUÍ
            mensaje,
        ],
        spacing=20,
        expand=True,
    )