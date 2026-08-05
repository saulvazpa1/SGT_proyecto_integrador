import flet as ft
from ui.dashboard_vendedor import dashboard_vendedor
from ui.cliente_list import clientes_list
from ui.pedido_list import pedidos_list
from ui.producto_catalogo_vendedor import catalogo_productos_vendedor
from ui.colores import *
from ui.notificaciones_list import mostrar_panel_notificaciones
from ui.notificaciones import contar_no_leidas


def main_window_vendedor(page: ft.Page, on_logout=None):
    page.title = "Sistema Gestor de Inventario Textil"
    page.bgcolor = FONDO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family="Segoe UI")
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    contenido = ft.Container(
        padding=30,
        expand=True,
    )

    menu_activo = "Inicio"

    # Badge de notificaciones
    badge_no_leidas = ft.Container(
        top=2,
        right=2,
        width=16,
        height=16,
        border_radius=8,
        bgcolor=ft.Colors.RED_600,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("0", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        visible=False,
    )

    def actualizar_badge_notificaciones():
        try:
            cantidad = contar_no_leidas()
        except Exception:
            cantidad = 0

        if cantidad > 0:
            badge_no_leidas.content.value = str(cantidad) if cantidad <= 9 else "9+"
            badge_no_leidas.visible = True
        else:
            badge_no_leidas.visible = False
        page.update()

    def click_notificaciones(e=None):
        mostrar_panel_notificaciones(page, al_cerrar=actualizar_badge_notificaciones)

    boton_notificaciones = ft.Stack(
        width=40,
        height=40,
        controls=[
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS,
                tooltip="Notificaciones",
                on_click=click_notificaciones,
            ),
            badge_no_leidas,
        ],
    )

    # Barra superior
    barra_superior = ft.Container(
        height=65,
        bgcolor=ft.Colors.GREY_100,
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Sistema Gestor de Inventario Textil",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_900,
                ),
                ft.Row(
                    controls=[
                        boton_notificaciones,
                        ft.CircleAvatar(
                            content=ft.Text("V"),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            radius=18,
                        ),
                        ft.Text("Vendedor", weight=ft.FontWeight.BOLD),
                    ],
                ),
            ],
        ),
    )

    def item_menu(texto, icono, accion, es_logout=False):
        activo = menu_activo == texto

        if es_logout:
            color_icono = ft.Colors.RED_400
            color_texto = ft.Colors.RED_400
            bg = None
            barra = ft.Colors.TRANSPARENT
        elif activo:
            color_icono = ft.Colors.BLUE_600
            color_texto = ft.Colors.BLUE_700
            bg = ft.Colors.BLUE_50
            barra = ft.Colors.BLUE_600
        else:
            color_icono = ft.Colors.BLUE_GREY_600
            color_texto = ft.Colors.BLUE_GREY_700
            bg = None
            barra = ft.Colors.TRANSPARENT

        return ft.Container(
            height=46,
            border_radius=10,
            on_click=accion,
            ink=True,
            content=ft.Row(
                spacing=0,
                controls=[
                    ft.Container(
                        width=4,
                        height=28,
                        bgcolor=barra,
                        border_radius=4,
                        margin=ft.Margin(left=0, top=9, right=0, bottom=9),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=bg,
                        border_radius=10,
                        padding=ft.Padding.only(left=12, right=12, top=10, bottom=10),
                        content=ft.Row(
                            spacing=12,
                            controls=[
                                ft.Icon(icono, size=20, color=color_icono),
                                ft.Text(
                                    texto,
                                    size=14,
                                    color=color_texto,
                                    weight=ft.FontWeight.W_600 if activo else ft.FontWeight.W_500,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    # Vistas
    def inicio():
        return ft.Column(
            controls=[dashboard_vendedor(page)],
            spacing=20,
            expand=True,
        )

    def mostrar_inicio(e=None):
        nonlocal menu_activo
        menu_activo = "Inicio"
        contenido.content = inicio()
        reconstruir_menu()
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_clientes(e=None):
        nonlocal menu_activo
        menu_activo = "Clientes"
        contenido.content = clientes_list(page)
        reconstruir_menu()
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_pedidos(e=None):
        nonlocal menu_activo
        menu_activo = "Pedidos"
        contenido.content = pedidos_list(page, puede_editar=True)
        reconstruir_menu()
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_catalogo(e=None):
        nonlocal menu_activo
        menu_activo = "Catálogo de Productos"
        contenido.content = catalogo_productos_vendedor(page)
        reconstruir_menu()
        page.update()
        actualizar_badge_notificaciones()

    def cerrar_sesion(e=None):
        def confirmar_cierre(e):
            page.pop_dialog()
            if on_logout:
                on_logout()
            else:
                page.window.destroy()

        def cancelar_cierre(e):
            page.pop_dialog()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cerrar sesión"),
            content=ft.Text("¿Seguro que deseas cerrar sesión y salir de la aplicación?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_cierre),
                ft.ElevatedButton(
                    "Cerrar sesión",
                    icon=ft.Icons.LOGOUT,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=confirmar_cierre,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialogo_confirmacion)

    # Menú lateral 
    menu_lateral = ft.Container(
        width=230,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border(right=ft.BorderSide(1, ft.Colors.BLUE_GREY_100)),
        padding=ft.Padding.only(left=12, right=12, top=16, bottom=16),
        content=ft.Column(
            spacing=4,
            expand=True,
        ),
    )

    def reconstruir_menu():
        menu_lateral.content.controls = [
            ft.Container(
                padding=ft.Padding.only(left=8, right=8, top=4, bottom=12),
                content=ft.Image(
                    src="logo.png",
                    width=130,
                    height=55,
                    fit="contain",
                ),
            ),

            ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),

            ft.Container(height=8),

            item_menu("Inicio", ft.Icons.HOME_OUTLINED, mostrar_inicio),
            item_menu("Clientes", ft.Icons.PERSON_OUTLINE, mostrar_clientes),
            item_menu("Pedidos", ft.Icons.SHOPPING_CART_OUTLINED, mostrar_pedidos),
            item_menu("Catálogo de Productos", ft.Icons.INVENTORY_2_OUTLINED, mostrar_catalogo),

            ft.Container(expand=True),

            ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),

            ft.Container(height=6),

            item_menu("Cerrar sesión", ft.Icons.LOGOUT, cerrar_sesion, es_logout=True),
        ]

    reconstruir_menu()

    # Layout
    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Column(
                expand=True,
                controls=[
                    barra_superior,
                    contenido,
                ],
            ),
        ],
        expand=True,
        spacing=0,
    )

    page.add(layout)
    mostrar_inicio()