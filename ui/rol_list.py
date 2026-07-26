import flet as ft
from dao.rol_dao import RolDAO


def roles_list(page: ft.Page):

    todos_los_roles = []

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del rol")),
            ft.DataColumn(ft.Text("Permisos")),
        ],
        rows=[],
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    buscador = ft.TextField(
        label="Buscar rol",
        hint_text="Escribe el nombre del rol...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    def cargar_desde_bd():
        nonlocal todos_los_roles
        try:
            todos_los_roles = RolDAO().obtener_todos()
            mensaje.value = ""
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"

    def aplicar_filtro(texto=""):
        texto_busqueda = (texto or "").strip().lower()

        filas = []
        for rol in todos_los_roles:
            nombre = str(rol.rol_nombre).lower()
            if not texto_busqueda or texto_busqueda in nombre:
                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(rol.rol_id))),
                            ft.DataCell(ft.Text(str(rol.rol_nombre))),
                            ft.DataCell(ft.Text(str(rol.rol_permisos))),
                        ]
                    )
                )

        tabla.rows = filas
        if page:
            page.update()

    buscador.on_change = lambda e: aplicar_filtro(texto=e.control.value)

    cargar_desde_bd()
    aplicar_filtro(texto="")

    return ft.Column(
        controls=[
            ft.Text("Roles del sistema", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Estos roles están definidos en la base de datos y determinan qué puede hacer cada usuario.",
                size=13,
                color=ft.Colors.BLUE_GREY_600,
            ),
            buscador,
            tabla,
            mensaje,
        ],
        spacing=20,
        expand=True,
    )