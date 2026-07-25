import flet as ft

def mostrar_dashboard(page: ft.Page):
    page.clean()

    def ir_a_usuarios(e):
        page.go("/usuarios")

    dashboard = ft.Row(
        expand=True,
        controls=[
            # Menú Lateral
            ft.Container(
                width=260,
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=20,
                content=ft.Column([
                    ft.Text("COSMOS", size=28, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.BLUE_GREY_700),
                    ft.ElevatedButton("Inicio", icon=ft.Icons.HOME, width=220, bgcolor=ft.Colors.BLUE_600),
                    ft.ElevatedButton("Inventario", icon=ft.Icons.INVENTORY, width=220),
                    ft.ElevatedButton("Pedidos", icon=ft.Icons.SHOPPING_CART, width=220),
                    ft.ElevatedButton("Finanzas", icon=ft.Icons.ATTACH_MONEY, width=220),
                    ft.ElevatedButton("Usuarios", icon=ft.Icons.PEOPLE, width=220, on_click=ir_a_usuarios),
                    ft.ElevatedButton("Reportes", icon=ft.Icons.BAR_CHART, width=220),
                    ft.ElevatedButton("Cerrar sesión", icon=ft.Icons.LOGOUT, width=220, on_click=lambda e: page.go("/login")),
                ], spacing=8)
            ),
            
            # Contenido Principal
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column([
                    ft.Text("Panel Administrador", size=28, weight=ft.FontWeight.BOLD),
                    
                    ft.Row([
                        ft.Card(content=ft.Container(padding=15, content=ft.Column([ft.Text("Pedidos\n20"), ft.Text("+15% este mes", color="green")]))),
                        ft.Card(content=ft.Container(padding=15, content=ft.Column([ft.Text("Ganancias\n$25,000"), ft.Text("+10% este mes", color="green")]))),
                        ft.Card(content=ft.Container(padding=15, content=ft.Column([ft.Text("Producción\n250")]))),
                        ft.Card(content=ft.Container(padding=15, content=ft.Column([ft.Text("Inventario\n85%")]))),
                    ], spacing=15),

                    ft.Row([
                        ft.Container(expand=2, content=ft.Card(content=ft.Text("Ventas Mensuales - Gráfico"))),
                        ft.Container(expand=1, content=ft.Card(content=ft.Text("Estado de Producción"))),
                    ])
                ], scroll=ft.ScrollMode.AUTO)
            )
        ]
    )
    page.add(dashboard)