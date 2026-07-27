import flet as ft
from ui.dashboard_vendedor import dashboard_vendedor
from ui.cliente_list import clientes_list
from ui.pedido_list import pedidos_list
from ui.producto_catalogo_vendedor import catalogo_productos_vendedor


def main_window_vendedor(page: ft.Page, on_logout=None):
    page.title = "Sistema Gestor de Inventario Textil"
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

    def mostrar_clientes(e=None):
        contenido.content = clientes_list(page)
        page.update()

    def mostrar_pedidos(e=None):
        contenido.content = pedidos_list(page)
        page.update()

    def mostrar_catalogo(e=None):
        contenido.content = catalogo_productos_vendedor(page)
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
        bgcolor=ft.Colors.WHITE,
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
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS,
                            tooltip="Notificaciones",
                        ),
                        ft.CircleAvatar(
                            content=ft.Text("V"),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            radius=18,
                        ),
                        ft.Text(
                            "Vendedor",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
            ],
        ),
    )

    menu_lateral = ft.Container(
        width=220,
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
                ft.Divider(color=ft.Colors.BLUE_GREY_700),
                ft.ElevatedButton(
                    "Inicio",
                    icon=ft.Icons.HOME,
                    width=180,
                    on_click=mostrar_inicio,
                ),
                ft.ElevatedButton(
                    "Clientes",
                    icon=ft.Icons.PERSON,
                    width=180,
                    on_click=mostrar_clientes,
                ),
                ft.ElevatedButton(
                    "Pedidos",
                    icon=ft.Icons.SHOPPING_CART,
                    width=180,
                    on_click=mostrar_pedidos,
                ),
                ft.ElevatedButton(
                    "Catálogo de Productos",
                    icon=ft.Icons.INVENTORY,
                    width=180,
                    on_click=mostrar_catalogo,
                ),
                ft.Container(expand=True),
                ft.Divider(color=ft.Colors.BLUE_GREY_700),
                ft.ElevatedButton(
                    "Cerrar sesión",
                    icon=ft.Icons.LOGOUT,
                    width=180,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                    on_click=cerrar_sesion,
                ),
            ],
            spacing=15,
            expand=True,
        ),
    )

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