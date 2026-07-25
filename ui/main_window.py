import flet as ft

from ui.dashborad import mostrar_dashboard
from ui.usuario_view import usuarios_view
#@from usuario_view import mostrar_gestion_usuarios

def main(page: ft.Page):
    page.title = "COSMOS - Sistema Administrativo"
    page.window_width = 1250
    page.window_height = 720
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50

    def route_change(route):
        page.clean()
        
        if page.route == "/login" or page.route == "/":
            usuarios_view(page)
        elif page.route == "/dashboard":
            mostrar_dashboard(page)
        elif page.route == "/usuarios":
            usuarios_view(page)

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main)