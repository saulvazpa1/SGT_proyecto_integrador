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

    #  Notificaciones:
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
                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                tooltip="Notificaciones",
                icon_size=25,
                icon_color=ft.Colors.BLUE_GREY_700,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=8,
                ),
                on_click=click_notificaciones,
            ),
            badge_no_leidas,
        ],
    )

    def inicio():
        return ft.Column(
            controls=[dashboard_vendedor(page)],
            spacing=20,
            expand=True,
        )

    # FIX: ahora TODAS las funciones de navegación refrescan el badge, no solo Pedidos.
    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_clientes(e=None):
        contenido.content = clientes_list(page)
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_pedidos(e=None):
        contenido.content = pedidos_list(page)
        page.update()
        actualizar_badge_notificaciones()

    def mostrar_catalogo(e=None):
        contenido.content = catalogo_productos_vendedor(page)
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
                        boton_notificaciones,
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