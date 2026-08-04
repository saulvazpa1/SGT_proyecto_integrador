import flet as ft
from dao.ordenes_produccion_dao import OrdenProduccionDAO
from ui.produccion_form import orden_produccion_form
from ui.notificaciones import agregar_notificacion
from ui.componentes import mostrar_notificacion


def _color_estado(estado):
    estado_normalizado = (estado or "").lower()
    if "pendiente" in estado_normalizado:
        return ft.Colors.AMBER_700, ft.Colors.AMBER_50
    if "cancelado" in estado_normalizado:
        return ft.Colors.RED_700, ft.Colors.RED_50
    if "completado" in estado_normalizado or "entregado" in estado_normalizado:
        return ft.Colors.GREEN_700, ft.Colors.GREEN_50
    if "corte" in estado_normalizado or "costura" in estado_normalizado or "acabado" in estado_normalizado or "proceso" in estado_normalizado:
        return ft.Colors.BLUE_700, ft.Colors.BLUE_50
    return ft.Colors.BLUE_GREY_700, ft.Colors.BLUE_GREY_50


def _chip_estado(estado):
    color_texto, color_fondo = _color_estado(estado)
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        bgcolor=color_fondo,
        border_radius=20,
        content=ft.Text(str(estado), size=12, color=color_texto, weight=ft.FontWeight.BOLD),
    )

pagina_actual = 1
filas_por_pagina = 5

def produccion_list(page: ft.Page):

    rol_id_actual = getattr(page, "rol_id_actual", None)
    puede_gestionar = rol_id_actual != 1

    todas_las_ordenes = []
    ordenes_filtradas = []

    pagina_actual = 1
    filas_por_pagina = 5

    TODOS_KEY = "__TODOS__"

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Pedido", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Encargado", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Inicio", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Entrega", weight=ft.FontWeight.BOLD, size=16)),
            ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, size=16)),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    buscador = ft.TextField(
        label="Buscar orden",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
    )

    filtro = ft.Dropdown(
        label="Filtrar por estado",
        width=220,
        value=TODOS_KEY,
        options=[ft.dropdown.Option(key=TODOS_KEY, text="Todos")],
    )

    paginador = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )


    def total_paginas():
        if not ordenes_filtradas:
            return 1
        paginas = len(ordenes_filtradas) // filas_por_pagina
        if len(ordenes_filtradas) % filas_por_pagina:
            paginas += 1
        return paginas
    def abrir_editar(produccion_id):
        if not puede_gestionar:
            return
        try:
            orden_completa = OrdenProduccionDAO().obtener_por_id(produccion_id)
        except Exception as ex:
            mensaje.value = f"Error al cargar la orden: {ex}"
            page.update()
            return

        if orden_completa is None:
            mensaje.value = "No se encontró la orden seleccionada"
            page.update()
            return

        def cerrar_editar():
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)

        dialogo = ft.AlertDialog(
            modal=True,
            content=orden_produccion_form(cerrar_editar, orden=orden_completa, page=page),
        )
        page.show_dialog(dialogo)

    def confirmar_eliminar(produccion_id):
        if not puede_gestionar:
            return

        def eliminar_confirmado(e):
            try:
                OrdenProduccionDAO().eliminar(produccion_id)
                page.pop_dialog()
                cargar_desde_bd()
                aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)

                texto = f"Orden #{produccion_id} eliminada"
                agregar_notificacion(texto)
                mostrar_notificacion(page, "Orden eliminada", texto, "error")
            except Exception as ex:
                page.pop_dialog()
                mensaje.value = f"Error al eliminar: {ex}"
                page.update()

        def cancelar_eliminar(e):
            page.pop_dialog()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Seguro que deseas eliminar la orden de producción #{produccion_id}? "
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

    def construir_fila(orden):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(orden.produccion_id))),
                ft.DataCell(ft.Text(f"#{orden.pedido_id}")),
                ft.DataCell(ft.Text(str(orden.producto_id))),
                ft.DataCell(ft.Text(str(orden.encargado_produccion_id))),
                ft.DataCell(ft.Text(str(orden.produccion_cantidad))),
                ft.DataCell(_chip_estado(orden.produccion_estado)),
                ft.DataCell(ft.Text(str(orden.fecha_inicio))),
                ft.DataCell(ft.Text(str(orden.fecha_entrega) if orden.fecha_entrega else "—")),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE_700,
                                bgcolor=ft.Colors.BLUE_50,
                                tooltip="Editar",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e, pid=orden.produccion_id: abrir_editar(pid),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_700,
                                bgcolor=ft.Colors.RED_50,
                                tooltip="Eliminar",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e, pid=orden.produccion_id: confirmar_eliminar(pid),
                            ),
                        ] if puede_gestionar else [
                            ft.Icon(ft.Icons.VISIBILITY, color=ft.Colors.BLUE_GREY_300, tooltip="Solo lectura"),
                        ],
                        spacing=8,
                    )
                ),
            ]
        )

    def render_pagina():
        inicio = (pagina_actual - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina

        tabla.rows = [
            construir_fila(o)
            for o in ordenes_filtradas[inicio:fin]
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

        # ➡️
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

    def aplicar_filtro(texto="", tipo_filtro=TODOS_KEY):
        nonlocal ordenes_filtradas, pagina_actual

        texto_busqueda = (texto or "").lower()

        resultado = []
        for orden in todas_las_ordenes:
            if tipo_filtro != TODOS_KEY and str(orden.produccion_estado) != tipo_filtro:
                continue

            campos = f"{orden.producto_id} {orden.encargado_produccion_id}".lower()
            if not texto_busqueda or texto_busqueda in campos:
                resultado.append(orden)

        ordenes_filtradas = resultado
        pagina_actual = 1
        render_pagina()

    def cargar_desde_bd():
        nonlocal todas_las_ordenes
        try:
            todas_las_ordenes = OrdenProduccionDAO().obtener_todos()

            estados = sorted({str(o.produccion_estado) for o in todas_las_ordenes if o.produccion_estado})
            filtro.options = [
                ft.dropdown.Option(key=TODOS_KEY, text="Todos"),
                *[ft.dropdown.Option(key=e, text=e) for e in estados],
            ]
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"


    def abrir_agregar(e):
        if not puede_gestionar:
            return

        def cerrar_dialogo():
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)

    buscador.on_change = lambda e: aplicar_filtro(e.control.value, filtro.value)
    filtro.on_change = lambda e: aplicar_filtro(buscador.value, e.control.value)

    controles_derecha = [buscador, filtro]

    if puede_gestionar:
        boton_agregar = ft.ElevatedButton(
            "Nueva orden",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.LIGHT_BLUE_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=abrir_agregar,
        )
        controles_derecha.append(boton_agregar)
    else:
        controles_derecha.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                bgcolor=ft.Colors.BLUE_GREY_50,
                border_radius=8,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCK_OUTLINE, size=16, color=ft.Colors.BLUE_GREY_400),
                        ft.Text("Solo lectura", size=13, color=ft.Colors.BLUE_GREY_500),
                    ],
                    spacing=6,
                ),
            )
        )

    cargar_desde_bd()
    aplicar_filtro()

    return ft.Column(
        controls=[
            ft.Text("Producción", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro],
                controls=controles_derecha,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla,
            paginador,
            mensaje,
        ],
        expand=True,
    )