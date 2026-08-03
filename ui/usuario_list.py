import flet as ft
from dao.usuario_dao import UsuarioDAO
from ui.usuario_form import usuario_form
from ui.colores import *
from ui.componentes import mostrar_notificacion


def usuarios_list(page: ft.Page):

    todos_los_usuarios = []
    usuarios_filtrados = []
    pagina_actual = 1
    filas_por_pagina = 5

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    "ID",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Nombre",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Teléfono",
                    weight=ft.FontWeight.BOLD,
                    size=16,            
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Correo",
                    weight=ft.FontWeight.BOLD,
                    size=16,
               )
            ),
            ft.DataColumn(
                ft.Text(
                    "Contraseña",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Rol",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Acciones",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                )
            ),
        ],
        rows=[],
    )

    buscador = ft.TextField(
        label="Buscar usuario",
        hint_text="Escribe el nombre del usuario...",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        value="",
    )

    filtro = ft.Dropdown(
        label="Filtrar por Rol",
        width=200,
        value="Todos",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Vendedor"),
            ft.dropdown.Option("Encargado de produccion"),
        ],
    )

    def cargar_desde_bd():
        nonlocal todos_los_usuarios
        try:
            dao = UsuarioDAO()
            todos_los_usuarios = dao.obtener_todos()
        except Exception as ex:
            mostrar_notificacion(page, "Error de conexión", str(ex), "error")

    def abrir_editar(usuario):
        def cerrar_editar(texto_exito=None):
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
            if texto_exito:
                mostrar_notificacion(page, "Se guardó correctamente", texto_exito, "exito")

        dialogo = ft.AlertDialog(
            modal=True,
            content=usuario_form(cerrar_editar, usuario=usuario),
        )
        page.show_dialog(dialogo)

    def confirmar_eliminar(usuario):
        def eliminar_confirmado(e):
            nombre_usuario = getattr(usuario, "usuario_nombre", "")
            try:
                UsuarioDAO().eliminar(usuario.usuario_id)
                page.pop_dialog()
                cargar_desde_bd()
                aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
                mostrar_notificacion(page, "Se eliminó correctamente", f"El usuario '{nombre_usuario}' fue eliminado", "exito")
            except Exception as ex:
                page.pop_dialog()
                mostrar_notificacion(page, "Error al eliminar", str(ex), "error")

        def cancelar_eliminar(e):
            page.pop_dialog()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Seguro que deseas eliminar al usuario '{getattr(usuario, 'usuario_nombre', '')}'? "
                "Esta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminar),
                ft.ElevatedButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=eliminar_confirmado,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialogo_confirmacion)

    def construir_fila(usuario):
        rol_nombre = str(getattr(usuario, "rol_id", "")) or "Sin rol"

        password_raw = str(getattr(usuario, "usuario_password", getattr(usuario, "usuario_contrasena", "*****")))
        password_oculta = "•" * len(password_raw) if password_raw != "*****" else "*****"

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(getattr(usuario, "usuario_id", "")))),
                ft.DataCell(ft.Text(str(getattr(usuario, "usuario_nombre", "")))),
                ft.DataCell(ft.Text(str(getattr(usuario, "usuario_telefono", "")))),
                ft.DataCell(ft.Text(str(getattr(usuario, "usuario_correo", "")))),
                ft.DataCell(ft.Text(password_oculta)),
                ft.DataCell(ft.Text(rol_nombre)),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar",
                            on_click=lambda e, u=usuario: abrir_editar(u),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar",
                            on_click=lambda e, u=usuario: confirmar_eliminar(u),
                        ),
                    ])
                ),
            ]
        )

    def total_paginas():
        if not usuarios_filtrados:
            return 1
        paginas = len(usuarios_filtrados) // filas_por_pagina
        if len(usuarios_filtrados) % filas_por_pagina:
            paginas += 1
        return max(paginas, 1)

    def render_pagina():
        inicio = (pagina_actual - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina
        tabla.rows = [construir_fila(u) for u in usuarios_filtrados[inicio:fin]]

        texto_pagina.value = f"Página {pagina_actual} de {total_paginas()}"
        boton_anterior.disabled = pagina_actual <= 1
        boton_siguiente.disabled = pagina_actual >= total_paginas()

        if page:
            page.update()

    def ir_pagina_anterior(e):
        nonlocal pagina_actual
        if pagina_actual > 1:
            pagina_actual -= 1
            render_pagina()

    def ir_pagina_siguiente(e):
        nonlocal pagina_actual
        if pagina_actual < total_paginas():
            pagina_actual += 1
            render_pagina()

    texto_pagina = ft.Text("Página 1 de 1")
    boton_anterior = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        tooltip="Página anterior",
        on_click=ir_pagina_anterior,
        disabled=True,
    )
    boton_siguiente = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        tooltip="Página siguiente",
        on_click=ir_pagina_siguiente,
        disabled=True,
    )

    def aplicar_filtro(texto="", tipo_filtro="Todos"):
        nonlocal usuarios_filtrados, pagina_actual
        texto_busqueda = (texto or "").strip().lower()
        opcion_filtro = (tipo_filtro or "Todos").strip()

        resultado = []
        for usuario in todos_los_usuarios:
            rol_nombre = str(getattr(usuario, "rol_id", ""))

            # 1. Filtros de Rol (Dropdown)
            if opcion_filtro == "Administrador" and rol_nombre != "Administrador":
                continue
            if opcion_filtro == "Vendedor" and rol_nombre != "Vendedor":
                continue
            if opcion_filtro == "Encargado de produccion" and rol_nombre != "Encargado de produccion":
                continue

            # 2. Filtro por texto
            nombre = str(getattr(usuario, "usuario_nombre", "")).lower()

            if not texto_busqueda or texto_busqueda in nombre:
                resultado.append(usuario)

        usuarios_filtrados = resultado
        pagina_actual = 1
        render_pagina()

    buscador.on_change = lambda e: aplicar_filtro(
        texto=e.control.value,
        tipo_filtro=filtro.value
    )

    def cambiar_filtro(e):
        aplicar_filtro(
            texto=buscador.value,
            tipo_filtro=e.control.value
        )

    filtro.on_select = cambiar_filtro

    # Carga inicial
    cargar_desde_bd()
    aplicar_filtro(texto="", tipo_filtro="Todos")

    # Botón Agregar
    def abrir_agregar(e):
        def cerrar_dialogo(texto_exito=None):
            page.pop_dialog()
            cargar_desde_bd()
            aplicar_filtro(texto=buscador.value, tipo_filtro=filtro.value)
            if texto_exito:
                mostrar_notificacion(page, "Se guardó correctamente", texto_exito, "exito")

        dialogo = ft.AlertDialog(
            modal=True,
            content=usuario_form(cerrar_dialogo),
        )
        page.show_dialog(dialogo)

    boton_agregar = ft.ElevatedButton(
        "Agregar usuario",
        bgcolor=AZUL,
        color=ft.Colors.WHITE,
        icon=ft.Icons.ADD,
        on_click=abrir_agregar,
    )

    return ft.Column(
        controls=[
            ft.Text("Gestión de Usuarios", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[buscador, filtro, boton_agregar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla,
            ft.Row(
                controls=[boton_anterior, texto_pagina, boton_siguiente],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=20,
        expand=True,
    )