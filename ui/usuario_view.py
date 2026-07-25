import flet as ft

def usuarios_view(page: ft.Page):
    
    def abrir_modal_registro(e):
        modal_registro = dialog_registrar_usuario(page)
        page.overlay.append(modal_registro)
        modal_registro.open = True
        page.update()

    tabla_usuarios = ft.Container(
        border=ft.Border.all(1, "#E2E8F0"),
        border_radius=ft.BorderRadius.all(10),
        bgcolor=ft.Colors.WHITE,
        padding=10,
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color="#7F8C8D")),
                ft.DataColumn(ft.Text("Nombre completo", weight=ft.FontWeight.BOLD, color="#7F8C8D")),
                ft.DataColumn(ft.Text("Correo", weight=ft.FontWeight.BOLD, color="#7F8C8D")),
                ft.DataColumn(ft.Text("Teléfono", weight=ft.FontWeight.BOLD, color="#7F8C8D")),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color="#7F8C8D")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("1")),
                        ft.DataCell(ft.Text("Juan Carlos Pérez")),
                        ft.DataCell(ft.Text("juan.perez@cosmos.com")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("5512345678", color="#0056B3", size=12),
                                bgcolor="#E6F0FA",
                                # ← Corregido
                                border_radius=ft.BorderRadius.all(5)
                            )
                        ),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT_ROUNDED, icon_color="#7F8C8D", icon_size=18)),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("2")),
                        ft.DataCell(ft.Text("Ana María Gómez")),
                        ft.DataCell(ft.Text("ana.gomez@cosmos.com")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("5587654321", color="#0056B3", size=12),
                                bgcolor="#E6F0FA",
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),   # ← Corregido
                                border_radius=ft.BorderRadius.all(5)
                            )
                        ),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT_ROUNDED, icon_color="#7F8C8D", icon_size=18)),
                    ]
                )
            ],
            expand=True
        )
    )

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Gestión de Usuarios", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor="#00A2E8",
                padding=12,
                border_radius=8,
                alignment=ft.alignment.center_left,
            ),
            ft.Container(height=10),
            
            ft.Row(
                controls=[
                    ft.TextField(
                        hint_text="Buscar por nombre",
                        prefix_icon=ft.Icons.SEARCH,
                        width=300,
                        border_color="#CBD5E1",
                        border_radius=8,
                        height=45,
                    ),
                    ft.Dropdown(
                        hint_text="Filtrar por Rol",
                        value="Administrador",
                        options=[
                            ft.dropdown.Option("Administrador"),
                            ft.dropdown.Option("Encargado de Inventario"),
                            ft.dropdown.Option("Encargado de Producción"),
                            ft.dropdown.Option("Trabajador"),
                            ft.dropdown.Option("Vendedor"),
                        ],
                        width=250,
                        height=45,
                    ),
                    ft.ElevatedButton(
                        "Agregar usuario",
                        icon=ft.Icons.ADD,
                        color=ft.Colors.WHITE,
                        bgcolor="#00A2E8",
                        on_click=abrir_modal_registro
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Container(height=15),
            tabla_usuarios
        ],
        spacing=10,
        expand=True
    )


def dialog_registrar_usuario(page: ft.Page):
    def cerrar_modal(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        content=ft.Container(
            width=650,
            padding=20,
            content=ft.Column([
                ft.Text("Registrar nuevo usuario", size=20, weight=ft.FontWeight.BOLD),
                # ... (puedes pegar aquí el resto del formulario si quieres)
                ft.Row([
                    ft.OutlinedButton("Cancelar", on_click=cerrar_modal),
                    ft.ElevatedButton("Guardar usuario", bgcolor="#00A2E8", color="white")
                ], alignment=ft.MainAxisAlignment.END)
            ])
        ),
        modal=True
    )
    return dialog