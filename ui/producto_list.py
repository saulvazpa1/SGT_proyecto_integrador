import flet as ft
from dao.producto_dao import ProductoDAO
from ui.producto_form import producto_form, _obtener_categorias
from ui.colores import *

def productos_list(page: ft.Page):

    todos_los_productos = []
    productos_filtrados = []
    pagina_actual = 1
    filas_por_pagina = 5

    TODAS_KEY = "__TODAS__"

    categorias_disponibles = _obtener_categorias()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Color", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Acciones")),
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

    contenedor_paginas = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
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
        except:
            precio_texto = f"${precio}"

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(producto.producto_id))),
                ft.DataCell(ft.Text(str(nombre))),
                ft.DataCell(ft.Text(str(categoria))),
                ft.DataCell(ft.Text(precio_texto)),
                ft.DataCell(ft.Text(str(stock))),
                ft.DataCell(ft.Text(str(color))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, p=producto: abrir_editar(p)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                      on_click=lambda e, p=producto: confirmar_eliminar(p)),
                    ])
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

  
    def ir_a_pagina(pagina):
        nonlocal pagina_actual
        pagina_actual = pagina
        render_pagina()

    def construir_paginador():
        contenedor_paginas.controls.clear()

        total = total_paginas()

        for i in range(1, total + 1):
            contenedor_paginas.controls.append(
                ft.Container(
                    content=ft.Text(
                        str(i),
                        color=ft.Colors.WHITE if i == pagina_actual else ft.Colors.BLACK
                    ),
                    bgcolor=ft.Colors.BLUE if i == pagina_actual else ft.Colors.GREY_300,
                    border_radius=8,
                    width=40,
                    height=40,
                    alignment=ft.Alignment(0, 0),  # 👈 SOLUCIÓN
                    on_click=lambda e, p=i: ir_a_pagina(p),
                )
            )

    def render_pagina():
        inicio = (pagina_actual - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina

        tabla.rows = [construir_fila(p) for p in productos_filtrados[inicio:fin]]

        texto_pagina.value = f"Página {pagina_actual} de {total_paginas()}"
        boton_anterior.disabled = pagina_actual <= 1
        boton_siguiente.disabled = pagina_actual >= total_paginas()

        construir_paginador()  # 👈 NUEVO

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

    texto_pagina = ft.Text("Página 1 de 1")

    boton_anterior = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        on_click=ir_pagina_anterior,
        disabled=True,
    )

    boton_siguiente = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        on_click=ir_pagina_siguiente,
        disabled=True,
    )

    def aplicar_filtro(texto="", tipo_filtro=TODAS_KEY):
        nonlocal productos_filtrados, pagina_actual

        texto_busqueda = (texto or "").lower()

        resultado = []
        for producto in todos_los_productos:
            categoria = str(getattr(producto, "producto_categoria", ""))

            if tipo_filtro != TODAS_KEY and categoria != tipo_filtro:
                continue

            nombre = str(getattr(producto, "producto_nombre", "")).lower()
            if not texto_busqueda or texto_busqueda in nombre:
                resultado.append(producto)

        productos_filtrados = resultado
        pagina_actual = 1
        render_pagina()

    buscador.on_change = lambda e: aplicar_filtro(e.control.value, filtro.value)
    filtro.on_select = lambda e: aplicar_filtro(buscador.value, e.control.value)

    cargar_desde_bd()
    aplicar_filtro()

    return ft.Column(
        controls=[
            ft.Text("Gestión de Productos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla,

            ft.Row(
                controls=[
                    boton_anterior,
                    contenedor_paginas,
                    boton_siguiente
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),

            mensaje,
        ],
        spacing=20,
        expand=True,
    )