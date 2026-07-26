import flet as ft
from ui.usuario_list import usuarios_list
from ui.dashboard_admin import dashboard_admin
from ui.rol_list import roles_list
from ui.producto_list import productos_list
from ui.pedido_list import pedidos_list
from ui.orden_produccion_list import produccion_list


def main_window(page: ft.Page):
    page.title = "Sistema Gestor de Inventario Textil"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50

   
    contenido = ft.Container(
        padding=30,
        expand=True,
    )

    # Barra superior de la aplicación
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
                            content=ft.Text("A"),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            radius=18,
                        ),
                        ft.Text(
                            "Administrador",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
            ],
        ),
    )

    # Vistas disponibles
    def inicio():
        return ft.Column(
            controls=[dashboard_admin(page)],
            spacing=20,
            expand=True,
        )

    # Funciones de navegación
    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()

    def mostrar_usuarios(e=None):
      
        contenido.content = usuarios_list(page)
        page.update()

    def mostrar_roles(e=None):
        contenido.content = roles_list(page)   
        page.update()

    def mostrar_productos(e=None):
            contenido.content = productos_list(page)   
            page.update()
    def mostrar_pedido(e=None):
        contenido.content = pedidos_list(page)   
        page.update()
    def mostrar_orden_produccion(e=None):
        contenido.content = produccion_list(page)   
        page.update()
        

    # Menú lateral
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
                    "Usuarios",
                    icon=ft.Icons.PEOPLE,
                    width=180,
                    on_click=mostrar_usuarios,
                ),
                ft.ElevatedButton(
                    "Roles",
                    icon=ft.Icons.SECURITY,
                    width=180,
                    on_click=mostrar_roles,
                ),
                ft.ElevatedButton(
                    "Productos",
                    icon=ft.Icons.INVENTORY,
                    width=180,
                    on_click=mostrar_productos,
                ),
                ft.ElevatedButton(
                    "Pedidos",
                    icon=ft.Icons.SHOPPING_CART,
                    width=180,
                    on_click=mostrar_pedido,
                ),
                ft.ElevatedButton(
                    "Producción",
                    icon=ft.Icons.PRECISION_MANUFACTURING,
                    width=180,
                     on_click=mostrar_orden_produccion
                ),
            ],
            spacing=15,
        ),
    )

    # Layout general dividiendo menú y vista activa
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
    
    # Carga la vista inicial al abrir la app
    mostrar_inicio()