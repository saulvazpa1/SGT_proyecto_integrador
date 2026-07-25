import flet as ft

def administrador(page: ft.Page):
    page.title = "Administrador"

    page.add(
        ft.Column(
            controls = [
                ft.Text(
                    "Panel de administrador",
                    size = 30,
                    weight = ft.FontWeight.BOLD
                )
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )