import flet as ft
from dao.cliente_dao import ClienteDAO
from ui.cliente_form import cliente_form
from ui.colores import *


def clientes_list(page: ft.Page):

    todos_los_clientes = []
    clientes_filtrados = []
    pagina_actual = 1
    filas_por_pagina = 5

    tabla = ft.DataTable(
        show_checkbox_column=False,
        column_spacing=45,
        horizontal_margin=20,
        divider_thickness=1,
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
                    "Nombre",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Teléfono",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Correo",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Domicilio",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Acciones",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
                ),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    buscador = ft.TextField(
        label="Buscar cliente",
        hint_text="Escribe el nombre del cliente...",
        prefix_icon=ft.Icons.SEARCH,
        width=300,
        value="",
    )

    def cargar_desde_bd():
        nonlocal todos_los_clientes
        try:
            todos_los_clientes = ClienteDAO().obtener_todos()
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"
            mensaje.color = ft.Colors.RED

    def abrir_editar(cliente):
        def cerrar_editar(texto_exito=None):
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value)
            if texto_exito:
                mensaje.value = texto_exito
                mensaje.color = ft.Colors.GREEN
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            content=cliente_form(cerrar_editar, cliente=cliente, page=page),
        )
        page.show_dialog(dialogo)

    def confirmar_eliminar(cliente):
        def eliminar_confirmado(e):
            nombre_cliente = getattr(cliente, "cliente_nombre", "")
            try:
                ClienteDAO().eliminar(cliente.cliente_id)
                page.pop_dialog()
                cargar_desde_bd()
                aplicar_filtro(texto=buscador.value)
                mensaje.value = f"Cliente '{nombre_cliente}' eliminado correctamente"
                mensaje.color = ft.Colors.GREEN
                page.update()
            except Exception as ex:
                page.pop_dialog()
                mensaje.value = f"Error al eliminar cliente: {ex}"
                mensaje.color = ft.Colors.RED
                page.update()

        def cancelar_eliminar(e):
            page.pop_dialog()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Seguro que deseas eliminar al cliente '{getattr(cliente, 'cliente_nombre', '')}'? "
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

    def construir_fila(cliente):
        calle = getattr(cliente, "cliente_calle", "")
        numero = getattr(cliente, "cliente_numero", "")
        municipio = getattr(cliente, "cliente_municipio", "")
        estado = getattr(cliente, "cliente_estado", "")
        cp = getattr(cliente, "cliente_codigopostal", "")

        domicilio_texto = f"{calle} #{numero}, {municipio}, {estado}, C.P. {cp}"

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(getattr(cliente, "cliente_id", "")))),
                ft.DataCell(ft.Text(str(getattr(cliente, "cliente_nombre", "")))),
                ft.DataCell(ft.Text(str(getattr(cliente, "cliente_telefono", "")))),
                ft.DataCell(ft.Text(str(getattr(cliente, "cliente_correo", "")))),
                ft.DataCell(ft.Text(domicilio_texto)),
                ft.DataCell(
                    ft.Row(
                        alignment=ft.Alignment(0, 0),
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                icon_color=ft.Colors.BLUE,
                                icon_size=20,
                                on_click=lambda e, c=cliente: abrir_editar(c),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                icon_color=ft.Colors.RED,
                                icon_size=20,
                                on_click=lambda e, c=cliente: confirmar_eliminar(c),
                            ),
                        ],
                    )
                )
            ]
        )

    def total_paginas():
        if not clientes_filtrados:
            return 1
        paginas = len(clientes_filtrados) // filas_por_pagina
        if len(clientes_filtrados) % filas_por_pagina:
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
            construir_fila(c)
            for c in clientes_filtrados[inicio:fin]
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

        # Botones numéricos
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

    def aplicar_filtro(texto=""):
        nonlocal clientes_filtrados, pagina_actual
        texto_busqueda = (texto or "").strip().lower()

        resultado = []
        for cliente in todos_los_clientes:
            nombre = str(getattr(cliente, "cliente_nombre", "")).lower()
            if not texto_busqueda or texto_busqueda in nombre:
                resultado.append(cliente)

        clientes_filtrados = resultado
        pagina_actual = 1
        render_pagina()

    buscador.on_change = lambda e: aplicar_filtro(texto=e.control.value)

    cargar_desde_bd()
    aplicar_filtro(texto="")

    def abrir_agregar(e):
        def cerrar_dialogo(texto_exito=None):
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value)
            if texto_exito:
                mensaje.value = texto_exito
                mensaje.color = ft.Colors.GREEN
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            content=cliente_form(cerrar_dialogo, page=page),
        )
        page.show_dialog(dialogo)

    boton_agregar = ft.ElevatedButton(
        "Agregar cliente",
        bgcolor=AZUL,
        color=ft.Colors.WHITE,
        icon=ft.Icons.ADD,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=20,
        ),
        on_click=abrir_agregar,
    )

    return ft.Column(
        controls=[
            ft.Text("Gestión de Clientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    buscador,
                    boton_agregar,
                ],
            ),
            tabla,
            paginador,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )