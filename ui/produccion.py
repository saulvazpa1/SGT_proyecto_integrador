import flet as ft

def produccion(page: ft.Page):
    page.title = "Producción"

    page.add(
        ft.Column(
            controls = [
                ft.Text(
                    "Panel de producción",
                    size = 30,
                    weight = ft.FontWeight.BOLD
                )
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )