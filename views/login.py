import flet as ft

class LoginView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = "#E8F5E9"
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=450,
                    padding=40,
                    bgcolor="white",
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.BLACK26,
                        offset=ft.Offset(0, 4),
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=90,
                                color=ft.Colors.GREEN,
                            ),
                            ft.Text(
                                "Sistema de Gestión Textil",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Iniciar Sesión",
                                size=18,
                                color=ft.Colors.GREY,
                            ),
                            ft.TextField(
                                label="Usuario",
                                prefix_icon=ft.Icons.PERSON,
                            ),
                            ft.TextField(
                                label="Contraseña",
                                password=True,
                                can_reveal_password=True,
                                prefix_icon=ft.Icons.LOCK,
                            ),
                            ft.ElevatedButton(
                                "Iniciar sesión",
                                width=300,
                                height=45,
                            ),
                        ],
                    ),
                )
            ],
        )