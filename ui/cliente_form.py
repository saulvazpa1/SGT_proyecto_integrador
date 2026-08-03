from turtle import color

import flet as ft
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO
from ui.colores import *



def cliente_form(regresar, cliente=None, page=None):
    editando = cliente is not None

    nombre_input = ft.TextField(
        label="Nombre",
        hint_text="Ingrese el nombre completo",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        expand=True,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_nombre", "") if editando else "",
    )
    correo_input = ft.TextField(
        label="Correo (opcional):",
        hint_text="ejemplo@correo.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        width=320,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_correo", "") if editando else "",
    )

    telefono_input = ft.TextField(
        label="Teléfono:",
        hint_text="10 dígitos",
        prefix_icon=ft.Icons.PHONE_OUTLINED,
        width=320,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_telefono", "") if editando else "",
    )

    # --- Campos de domicilio ---
    calle_input = ft.TextField(
        label="Calle:",
        hint_text="Nombre de la calle",
        prefix_icon=ft.Icons.HOME_OUTLINED,
        width=210,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_calle", "") if editando else "",
    )

    numero_input = ft.TextField(
        label="Número:",
        hint_text="No.",
        prefix_icon=ft.Icons.NUMBERS,
        width=210,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=str(getattr(cliente, "cliente_numero", "")) if editando else "",
    )

    municipio_input = ft.TextField(
        label="Municipio:",
        hint_text="Municipio",
        prefix_icon=ft.Icons.LOCATION_CITY,
        width=210,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_municipio", "") if editando else "",
    )

    estado_input = ft.TextField(
        label="Estado:",
        hint_text="Estado",
        width=210,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_estado", "") if editando else "",
    )

    codigopostal_input = ft.TextField(
        label="Código postal:",
        hint_text="C.P.",
        prefix_icon=ft.Icons.MARKUNREAD_MAILBOX_OUTLINED,
        width=210,
        border_radius=6,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=str(getattr(cliente, "cliente_codigopostal", "")) if editando else "",
    )

    seccion_domicilio = ft.Container(
        padding=15,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Text("Domicilio", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
                ft.Row(
                    controls=[
                        calle_input,
                        numero_input,
                        municipio_input,
                        estado_input,
                        codigopostal_input,
                    ],
                    wrap=True,
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def mostrar_notificacion(titulo, mensaje, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            bgcolor=color,
            content=ft.Text(f"{titulo}: {mensaje}", color=ft.Colors.WHITE),
            open=True,
        )
        page.update()

        toast = ft.Container(
            width=430,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=1,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 4),
            ),
            animate_opacity=300,
            content=ft.Row(
                spacing=0,
                controls=[
                    ft.Container(
                        width=60,
                        height=80,
                        bgcolor=color + "_100",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(
                            ft.Icons.ERROR if color == ft.Colors.RED else ft.Icons.CHECK_CIRCLE,
                            color=color,
                            size=30,
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        padding=15,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    titulo,
                                    weight=ft.FontWeight.BOLD,
                                    size=17,
                                ),
                                ft.Text(
                                    mensaje,
                                    size=13,
                                    color=ft.Colors.GREY_700,
                                ),
                            ],
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda e: cerrar_toast(),
                    ),
                ],
            ),
        )

        def cerrar_toast():
            page.overlay.remove(toast)
            page.update()

        overlay_toast = ft.Container(
            alignment=ft.Alignment.TOP_RIGHT,
            padding=20,
            content=toast,
        )

        page.overlay.append(overlay_toast)
        page.update()

        def cerrar_toast():
            if overlay_toast in page.overlay:
                page.overlay.remove(overlay_toast)
                page.update()


    def guardar_cliente(e):
        p_page = page or e.page

        nombre = (nombre_input.value or "").strip()
        correo = (correo_input.value or "").strip()
        telefono = (telefono_input.value or "").strip()
        calle = (calle_input.value or "").strip()
        numero = (numero_input.value or "").strip()
        municipio = (municipio_input.value or "").strip()
        estado = (estado_input.value or "").strip()
        codigopostal = (codigopostal_input.value or "").strip()

        if not nombre or not telefono or not calle or not numero or not municipio or not estado or not codigopostal:
            mensaje.value = "Todos los campos son obligatorios (excepto correo)"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            dao = ClienteDAO()

            if editando:
                cliente_actualizado = Cliente(
                    cliente_id=cliente.cliente_id,
                    cliente_nombre=nombre,
                    cliente_correo=correo,
                    cliente_telefono=telefono,
                    cliente_calle=calle,
                    cliente_numero=numero,
                    cliente_municipio=municipio,
                    cliente_estado=estado,
                    cliente_codigopostal=codigopostal,
                )

            nuevo_id = dao.obtener_ultimo_id() + 1
            nuevo_cliente = Cliente(
                cliente_id=nuevo_id,
                cliente_nombre=nombre,
                cliente_correo=correo,
                cliente_telefono=telefono,
                cliente_calle=calle,
                cliente_numero=numero,
                cliente_municipio=municipio,
                cliente_estado=estado,
                cliente_codigopostal=codigopostal,
            )
            dao.insertar(nuevo_cliente)

            mostrar_notificacion(
                "Cliente registrado",
                f"{nombre} se registró correctamente."
            )

            #regresar()

        except Exception as error:
            mostrar_notificacion(
                "Error",
                str(error),
                ft.Colors.RED,
            )

            mensaje.value = f"Error al guardar el cliente: {error}"
            mensaje.color = ft.Colors.RED

            mensaje.value = f"Error al guardar el cliente: {error}"
            mensaje.color = ft.Colors.RED

        if p_page:
            p_page.update()

    encabezado = ft.Container(
        bgcolor=AZUL,
        padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Editar cliente" if editando else "Registrar nuevo cliente",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: regresar(),
                ),
            ],
        ),
    )

    columna_datos = ft.Column(
        controls=[
            nombre_input,
            correo_input,
            telefono_input,
        ],
        spacing=15,
    )

    cuerpo = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Modifica los datos del cliente" if editando else "Captura los datos del nuevo cliente",
                    size=14,
                    color=AZUL,
                ),
                columna_datos,
                seccion_domicilio,
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
        height=500,
    )

    pie = ft.Container(
        padding=ft.Padding.only(left=30, right=30, bottom=20, top=5),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    on_click=lambda e: regresar(),
                ),
                ft.ElevatedButton(
                    "Guardar cambios" if editando else "Registrar cliente",
                    icon=ft.Icons.SAVE,
                    bgcolor=AZUL,
                    color=ft.Colors.WHITE,
                    on_click=guardar_cliente,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Container(
        width=720,
        height=620,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                encabezado,
                ft.Container(
                    expand=True,
                    content=cuerpo,
                ),
                pie,
            ],
        ),
    )
