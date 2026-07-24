import flet as ft

def vendedor(page: ft.Page):
    page.title = "Vendedor"

    page.add(
        ft.Column(
            controls = [
                ft.Text(
                    "Panel de vendedor",
                    size = 30,
                    weight = ft.FontWeight.BOLD
                )
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )