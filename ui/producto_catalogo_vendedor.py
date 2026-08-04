import flet as ft
from dao.producto_dao import ProductoDAO
from ui.producto_form import _obtener_categorias
from ui.colores import *


def catalogo_productos_vendedor(page: ft.Page):

    todos_los_productos = []
    productos_filtrados = []
    pagina_actual = 1
    filas_por_pagina = 5

    TODAS_KEY = "__TODAS__"

    categorias_disponibles = _obtener_categorias()

    tabla = ft.DataTable(
        show_checkbox_column=False,
        column_spacing=25,
        horizontal_margin=10,
        divider_thickness=1,
        heading_row_height=55,
        data_row_min_height=55,
        data_row_max_height=55,
        columns=[
            ft.DataColumn(
                ft.Container(
                    width=80,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("ID", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
            ft.DataColumn(
                ft.Container(
                    width=220,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("Nombre", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
            ft.DataColumn(
                ft.Container(
                    width=180,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("Categoría", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
            ft.DataColumn(
                ft.Container(
                    width=120,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("Precio", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
            ft.DataColumn(
                ft.Container(
                    width=120,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("Stock", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
            ft.DataColumn(
                ft.Container(
                    width=150,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("Color", weight=ft.FontWeight.BOLD, size=16),
                )
            ),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    buscador = ft.TextField(
        label="Buscar producto",
        hint_text="Escribe el nombre del producto...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    filtro = ft.Dropdown(
        label="Filtrar por categoría",
        width=220,
        value=TODAS_KEY,
        options=[
            ft.dropdown.Option(key=TODAS_KEY, text="Todas"),
            *[ft.dropdown.Option(key=nombre, text=nombre) for _, nombre in categorias_disponibles],
        ],
    )

    def cargar_desde_bd():
        nonlocal todos_los_productos
        try:
            todos_los_productos = ProductoDAO().obtener_todos()
            mensaje.value = ""
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"

    def construir_fila(producto):
        categoria = getattr(producto, "producto_categoria", "")
        nombre = getattr(producto, "producto_nombre", "")
        precio = getattr(producto, "producto_precio", 0)
        stock = getattr(producto, "producto_stock", "")
        color = getattr(producto, "producto_color", "")

        try:
            precio_texto = f"${float(precio):,.2f}"
        except (TypeError, ValueError):
            precio_texto = f"${precio}"

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Container(
                        width=80,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(str(producto.producto_id)),
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        width=220,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(str(nombre)),
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        width=180,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(str(categoria)),
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        width=120,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(precio_texto),
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        width=120,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(str(stock)),
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        width=150,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(str(color)),
                    )
                ),
            ]
        )

    def total_paginas():
        if not productos_filtrados:
            return 1
        paginas = len(productos_filtrados) // filas_por_pagina
        if len(productos_filtrados) % filas_por_pagina:
            paginas += 1
        return max(paginas, 1)

    paginador = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    def render_pagina():
        inicio = (pagina_actual - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina

        tabla.rows = [
            construir_fila(p)
            for p in productos_filtrados[inicio:fin]
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


    def aplicar_filtro(texto="", tipo_filtro=TODAS_KEY):
        nonlocal productos_filtrados, pagina_actual
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = tipo_filtro or TODAS_KEY

        resultado = []
        for producto in todos_los_productos:
            categoria = str(getattr(producto, "producto_categoria", ""))

            if opcion_filtro != TODAS_KEY and categoria != opcion_filtro:
                continue

            nombre = str(getattr(producto, "producto_nombre", "")).lower()
            if not texto_busqueda or texto_busqueda in nombre:
                resultado.append(producto)

        productos_filtrados = resultado
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
    aplicar_filtro(texto="", tipo_filtro=TODAS_KEY)

    return ft.Column(
        controls=[
            ft.Text("Catálogo de Productos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            tabla,
            paginador,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )