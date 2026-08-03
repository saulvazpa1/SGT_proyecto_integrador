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

    filas_por_pagina = 10
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

        # Flecha izquierda
        paginador.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                disabled=pagina_actual == 1,
                on_click=ir_pagina_anterior,
            )
        )

        # Botones de páginas
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

        # Flecha derecha
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

        nonlocal pagina_actual

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
            paginador,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )