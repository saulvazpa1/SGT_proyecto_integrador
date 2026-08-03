import flet as ft
from ui.dashboard_vendedor import dashboard_vendedor
from ui.cliente_list import clientes_list
from ui.pedido_list import pedidos_list
from ui.producto_catalogo_vendedor import catalogo_productos_vendedor
from ui.pedido_pendiente import pedidos_pendientes


from ui.produccion_list import produccion_list
from ui.colores import *


def main_window_produccion(page: ft.Page, on_logout=None):
    page.title = "Sistema Gestor de Inventario Textil - Producción"
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

    def mostrar_ordenes_produccion(e=None):
        nonlocal menu_activo
        menu_activo = "Órdenes"
        contenido.content = produccion_list(page)
        reconstruir_menu()
        page.update()

    def mostrar_productos(e=None):
        nonlocal menu_activo
        menu_activo = "Productos"
        contenido.content = catalogo_productos_vendedor(page)
        reconstruir_menu()
        page.update()

    def mostrar_pedidos_pendientes(e=None):
        nonlocal menu_activo
        menu_activo = "Pendientes"
        contenido.content = pedidos_pendientes(page)
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
    

    #  Barra Superior 
    barra_superior = ft.Container(
        height=65,
        bgcolor=ft.Colors.WHITE,
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Módulo de Producción Textil",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_900,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS,
                            tooltip="Notificaciones",
                        ),
                        ft.CircleAvatar(
                            content=ft.Text("P"),
                            bgcolor=ft.Colors.ORANGE_800,
                            color=ft.Colors.WHITE,
                            radius=18,
                        ),
                        ft.Text(
                            "Área Producción",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
            ],
        ),
    )

    menu_lateral = ft.Container(
        width=220,
        bgcolor=ft.Colors.WHITE,
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
                "Órdenes",
                ft.Icons.PRECISION_MANUFACTURING,
                mostrar_ordenes_produccion,
            ),

            item_menu(
                "Productos",
                ft.Icons.INVENTORY_2_OUTLINED,
                mostrar_productos,
            ),

            item_menu(
                "Pendientes",
                ft.Icons.ASSIGNMENT_LATE_OUTLINED,
                mostrar_pedidos_pendientes,
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


    #  Layout General 

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