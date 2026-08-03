import flet as ft
from ui.dashboard_vendedor import dashboard_vendedor
from ui.cliente_list import clientes_list
from ui.pedido_list import pedidos_list
from ui.producto_catalogo_vendedor import catalogo_productos_vendedor
from ui.colores import *


def main_window_vendedor(page: ft.Page, on_logout=None):
    page.title = "Sistema Gestor de Inventario Textil"
    page.bgcolor = FONDO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        font_family="Segoe UI"
    )
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50

    contenido = ft.Container(
        padding=30,
        expand=True,
    )

    menu_activo = "Inicio"

    def item_menu(texto, icono, accion):
        activo = menu_activo == texto

        return ft.Container(
            height=48,
            on_click=accion,
            ink=True,
            content=ft.Row(
                spacing=0,
                controls=[
                    ft.Container(
                        width=4,
                        bgcolor=ft.Colors.BLUE if activo else ft.Colors.TRANSPARENT,
                        border_radius=5,
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.BLUE_50 if activo else None,
                        padding=12,
                        content=ft.Row(
                            spacing=12,
                            controls=[
                                ft.Icon(
                                    icono,
                                    color=ft.Colors.BLUE if activo else ft.Colors.GREY_700,
                                ),
                                ft.Text(
                                    texto,
                                    color=ft.Colors.BLUE if activo else ft.Colors.GREY_700,
                                    weight=ft.FontWeight.BOLD if activo else ft.FontWeight.NORMAL,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def inicio():
        return ft.Column(
        controls=[
            dashboard_vendedor(page)
        ],
        expand=True
    )

    def mostrar_inicio(e=None):
        nonlocal menu_activo
        menu_activo = "Inicio"
        contenido.content = inicio()
        reconstruir_menu()
        page.update()

    def mostrar_clientes(e=None):
        nonlocal menu_activo
        menu_activo = "Clientes"
        contenido.content = clientes_list(page)
        reconstruir_menu()
        page.update()

    def mostrar_pedidos(e=None):
        nonlocal menu_activo
        menu_activo = "Pedidos"
        contenido.content = pedidos_list(page)
        reconstruir_menu()
        page.update()

    def mostrar_catalogo(e=None):
        nonlocal menu_activo
        menu_activo = "Catálogo"
        contenido.content = catalogo_productos_vendedor(page)
        reconstruir_menu()
        page.update()

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
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                            tooltip="Notificaciones",
                            icon_size=25,
                            icon_color=ft.Colors.BLUE_GREY_700,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                padding=8,
                            ),
                        ),
                        ft.CircleAvatar(
                            radius=18,
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            content=ft.Text(
                                "V",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                        ft.Text(
                            "Vendedor",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                )
            ],
        ),
    )

    menu_lateral = ft.Container(
        width=220,
        bgcolor=FONDO,
        padding=20,
        content=ft.Column(
            spacing=8,
            expand=True,
        ),
    )

    def reconstruir_menu():
        menu_lateral.content.controls = [
            ft.Image(
                src="logo.png",
                width=120,
                height=60,
                fit="contain",
            ),

            ft.Divider(),

            item_menu(
                "Inicio",
                ft.Icons.HOME_OUTLINED,
                mostrar_inicio,
            ),

            item_menu(
                "Clientes",
                ft.Icons.PERSON_OUTLINE,
                mostrar_clientes,
            ),

            item_menu(
                "Pedidos",
                ft.Icons.SHOPPING_CART_OUTLINED,
                mostrar_pedidos,
            ),

            item_menu(
                "Catálogo",
                ft.Icons.INVENTORY_2_OUTLINED,
                mostrar_catalogo,
            ),

            ft.Container(expand=True),

            ft.Divider(),

            item_menu(
                "Cerrar sesión",
                ft.Icons.LOGOUT,
                cerrar_sesion,
            ),
        ]
    reconstruir_menu()

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
    )

    page.add(layout)
    mostrar_inicio()