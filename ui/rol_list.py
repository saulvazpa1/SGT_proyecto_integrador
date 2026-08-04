import flet as ft
from dao.rol_dao import RolDAO
from dao.usuario_dao import UsuarioDAO

ANCHO_ID = 60
ANCHO_ROL = 260
ANCHO_PERMISOS = 500


def _icono_para_rol(nombre_rol):
    nombre_normalizado = (nombre_rol or "").lower()
    if "administrador" in nombre_normalizado:
        return ft.Icons.ADMIN_PANEL_SETTINGS, ft.Colors.PURPLE_400
    if "vendedor" in nombre_normalizado:
        return ft.Icons.SHOPPING_CART, ft.Colors.BLUE_400
    if "produccion" in nombre_normalizado or "producción" in nombre_normalizado:
        return ft.Icons.PRECISION_MANUFACTURING, ft.Colors.TEAL_400
    if "inventario" in nombre_normalizado:
        return ft.Icons.INVENTORY_2, ft.Colors.AMBER_600
    if "trabajador" in nombre_normalizado:
        return ft.Icons.ENGINEERING, ft.Colors.INDIGO_400
    return ft.Icons.PERSON, ft.Colors.BLUE_GREY_400


def _tarjeta_resumen_rol(nombre_rol, cantidad_usuarios, color, icono):
    return ft.Container(
        width=210,
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1.5, color),
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(nombre_rol, size=13, color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.BOLD),
                        ft.Icon(icono, size=18, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(str(cantidad_usuarios), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text(
                    "usuario" if cantidad_usuarios == 1 else "usuarios",
                    size=12,
                    color=ft.Colors.BLUE_GREY_500,
                ),
            ],
            spacing=4,
        ),
    )


def _chips_permisos(permisos_texto):
    permisos = [p.strip() for p in str(permisos_texto or "").split(",") if p.strip()]
    if not permisos:
        return ft.Text("—", size=12, color=ft.Colors.BLUE_GREY_400)

    return ft.Row(
        controls=[
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                bgcolor=ft.Colors.BLUE_GREY_50,
                border_radius=20,
                content=ft.Text(permiso, size=12, color=ft.Colors.BLUE_GREY_700),
            )
            for permiso in permisos
        ],
        wrap=True,
        spacing=6,
        run_spacing=6,
    )


def _fila_encabezado():
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=10),
        content=ft.Row(
            controls=[
                ft.Container(width=ANCHO_ID, content=ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.Container(width=ANCHO_ROL, content=ft.Text("Rol", weight=ft.FontWeight.BOLD)),
                ft.Container(width=ANCHO_PERMISOS, content=ft.Text("Permisos", weight=ft.FontWeight.BOLD)),
            ],
        ),
    )


def _fila_rol(rol):
    icono, color = _icono_para_rol(rol.rol_nombre)
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=12),
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.BLUE_GREY_100)),
        content=ft.Row(
            controls=[
                ft.Container(width=ANCHO_ID, content=ft.Text(str(rol.rol_id))),
                ft.Container(
                    width=ANCHO_ROL,
                    content=ft.Row(
                        controls=[ft.Icon(icono, size=18, color=color), ft.Text(str(rol.rol_nombre))],
                        spacing=8,
                    ),
                ),
                ft.Container(width=ANCHO_PERMISOS, content=_chips_permisos(rol.rol_permisos)),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )


def rol_list(page: ft.Page):

    todos_los_roles = []

    TODOS_KEY = "__TODOS__"

    mensaje = ft.Text("", color=ft.Colors.RED)

    buscador = ft.TextField(
        label="Buscar rol",
        hint_text="Escribe el nombre del rol...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    filtro = ft.Dropdown(
        label="Filtrar por rol",
        width=250,
        value=TODOS_KEY,
        options=[ft.dropdown.Option(key=TODOS_KEY, text="Todos")],
    )

    tarjetas_container = ft.Row(spacing=20, wrap=True)
    filas_container = ft.Column(spacing=0)

    def cargar_desde_bd():
        nonlocal todos_los_roles
        try:
            todos_los_roles = RolDAO().obtener_todos()
            mensaje.value = ""
        except Exception as ex:
            mensaje.value = f"Error BD: {ex}"
            return

        try:
            usuarios = UsuarioDAO().obtener_todos()
        except Exception:
            usuarios = []

        conteo_por_rol = {}
        for u in usuarios:
            nombre_rol_usuario = str(getattr(u, "rol_id", "") or "").strip()
            conteo_por_rol[nombre_rol_usuario] = conteo_por_rol.get(nombre_rol_usuario, 0) + 1

        tarjetas_container.controls = []
        for rol in todos_los_roles:
            icono, color = _icono_para_rol(rol.rol_nombre)
            cantidad = conteo_por_rol.get(rol.rol_nombre, 0)
            tarjetas_container.controls.append(
                _tarjeta_resumen_rol(rol.rol_nombre, cantidad, color, icono)
            )

        filtro.options = [
            ft.dropdown.Option(key=TODOS_KEY, text="Todos"),
            *[ft.dropdown.Option(key=rol.rol_nombre, text=rol.rol_nombre) for rol in todos_los_roles],
        ]

    def aplicar_filtro(texto="", tipo_filtro=TODOS_KEY):
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = tipo_filtro or TODOS_KEY

        filas = []
        for rol in todos_los_roles:
            if opcion_filtro != TODOS_KEY and rol.rol_nombre != opcion_filtro:
                continue

            nombre = str(rol.rol_nombre).lower()
            if not texto_busqueda or texto_busqueda in nombre:
                filas.append(_fila_rol(rol))

        filas_container.controls = filas
        if page:
            page.update()

    buscador.on_change = lambda e: aplicar_filtro(texto=e.control.value, tipo_filtro=filtro.value)

    def cambiar_filtro(e):
        aplicar_filtro(texto=buscador.value, tipo_filtro=e.control.value)

    filtro.on_select = cambiar_filtro

    cargar_desde_bd()
    aplicar_filtro(texto="", tipo_filtro=TODOS_KEY)

    return ft.Column(
        controls=[
            ft.Text("Roles del sistema", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Estos roles están definidos en la base de datos y determinan qué puede hacer cada usuario.",
                size=13,
                color=ft.Colors.BLUE_GREY_600,
            ),
            tarjetas_container,
            ft.Row(controls=[buscador, filtro], spacing=20),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                border_radius=8,
                content=ft.Column(
                    controls=[_fila_encabezado(), ft.Divider(height=1, color=ft.Colors.BLUE_GREY_200), filas_container],
                    spacing=0,
                ),
            ),
            mensaje,
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )