import flet as ft
from ui.dashboard_vendedor import dashboard_vendedor
from ui.cliente_list import clientes_list
from ui.pedido_list import pedidos_list
from ui.producto_catalogo_vendedor import catalogo_productos_vendedor
from ui.pedido_pendiente import pedidos_pendientes

from ui.produccion_list import produccion_list


def main_window_produccion(page: ft.Page):
    page.title = "Sistema Gestor de Inventario Textil - Producción"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50

    contenido = ft.Container(
        padding=30,
        expand=True,
    )

    
    def inicio():
        return ft.Column(
            controls=[dashboard_vendedor(page)],
            spacing=20,
            expand=True,
        )

    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()

    def mostrar_ordenes_produccion(e=None):
        # Muestra la vista/tabla general de producción
        contenido.content = produccion_list(page)
        page.update()

    def mostrar_productos(e=None):
        contenido.content = catalogo_productos_vendedor(page)
        page.update()

    def mostrar_pedidos_pendientes(e=None):
       contenido.content =pedidos_pendientes(page)
       page.update()

    def cerrar_sesion(e=None):
            def confirmar_cierre(e):
                page.pop_dialog()
                page.window.close()
    
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
        width=240,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Image(
                    src="logo.png",
                    width=120,
                    height=60,
                    fit="contain",
                ),
                ft.Text(
                    "PRODUCCIÓN",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_200,
                ),
                ft.Divider(color=ft.Colors.BLUE_GREY_700),
                ft.ElevatedButton(
                    " Dashboard",
                    icon=ft.Icons.DASHBOARD,
                    width=200,
                    on_click=mostrar_inicio,
                ),
                ft.ElevatedButton(
                    " Órdenes Producción",
                    icon=ft.Icons.PRECISION_MANUFACTURING,
                    width=200,
                    on_click=mostrar_ordenes_produccion,
                ),
                ft.ElevatedButton(
                    " Productos",
                    icon=ft.Icons.INVENTORY_2,
                    width=200,
                    on_click=mostrar_productos,
                ),
                ft.ElevatedButton(
                    " Pedidos Pendientes",
                    icon=ft.Icons.ASSIGNMENT_LATE,
                    width=200,
                    on_click=mostrar_pedidos_pendientes,
                ),
                ft.Container(expand=True),
                ft.Divider(color=ft.Colors.BLUE_GREY_700),
                ft.ElevatedButton(
                    "Cerrar sesión",
                    icon=ft.Icons.LOGOUT,
                    width=200,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                    on_click=cerrar_sesion,
                ),
            ],
            spacing=12,
            expand=True,
        ),
    )

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