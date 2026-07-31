import flet as ft
from dao.ordenes_produccion_dao import OrdenProduccionDAO
from ui.produccion_form import orden_produccion_form


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


def produccion_list(page: ft.Page):

    todas_las_ordenes = []
    ordenes_filtradas = []

    TODOS_KEY = "__TODOS__"

    tabla = ft.DataTable(
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
                    "Pedido",
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
                    "Encargado",
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
                    "Estado",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Inicio",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Entrega",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
           
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    buscador = ft.TextField(
        label="Buscar orden",
        hint_text="Busca por producto o encargado...",
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
        nonlocal todas_las_ordenes
        try:
            todas_las_ordenes = OrdenProduccionDAO().obtener_todos()
            mensaje.value = ""

            estados_unicos = sorted({
                str(o.produccion_estado) for o in todas_las_ordenes if o.produccion_estado
            })
            filtro.options = [
                ft.dropdown.Option(key=TODOS_KEY, text="Todos"),
                *[ft.dropdown.Option(key=estado, text=estado) for estado in estados_unicos],
            ]
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"

    def abrir_editar(produccion_id):
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
        def eliminar_confirmado(e):
            try:
                OrdenProduccionDAO().eliminar(produccion_id)
                page.pop_dialog()
                cargar_desde_bd()
                aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
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
                
            ]
        )

    def aplicar_filtro(texto="", tipo_filtro=TODOS_KEY):
        nonlocal ordenes_filtradas
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = tipo_filtro or TODOS_KEY

        resultado = []
        for orden in todas_las_ordenes:
            if opcion_filtro != TODOS_KEY and str(orden.produccion_estado) != opcion_filtro:
                continue

            campos = f"{orden.producto_id} {orden.encargado_produccion_id}".lower()
            if not texto_busqueda or texto_busqueda in campos:
                resultado.append(orden)

        ordenes_filtradas = resultado
        tabla.rows = [construir_fila(o) for o in ordenes_filtradas]

        if page:
            page.update()

    buscador.on_change = lambda e: aplicar_filtro(texto=e.control.value, tipo_filtro=filtro.value)

    def cambiar_filtro(e):
        aplicar_filtro(texto=buscador.value, tipo_filtro=e.control.value)

    filtro.on_select = cambiar_filtro

    cargar_desde_bd()
    aplicar_filtro(texto="", tipo_filtro=TODOS_KEY)

    def abrir_agregar(e):
        def cerrar_dialogo():
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)

        dialogo = ft.AlertDialog(
            modal=True,
            content=orden_produccion_form(cerrar_dialogo, page=page),
        )
        page.show_dialog(dialogo)

    

    return ft.Column(
        controls=[
            ft.Text("Producción", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro,],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )