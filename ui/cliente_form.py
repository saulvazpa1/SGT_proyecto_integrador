import flet as ft
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO
from ui.colores import *
from ui.validaciones import validar_nombre, validar_correo, validar_telefono


def cliente_form(regresar, cliente=None, page=None):
    editando = cliente is not None

    nombre_input = ft.TextField(
        label="Nombre",
        hint_text="Ingrese el nombre completo",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_nombre", "") if editando else "",
    )

    correo_input = ft.TextField(
        label="Correo (opcional)",
        hint_text="ejemplo@correo.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_correo", "") if editando else "",
    )

    telefono_input = ft.TextField(
        label="Teléfono",
        hint_text="10 dígitos",
        prefix_icon=ft.Icons.PHONE_OUTLINED,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_telefono", "") if editando else "",
    )

    calle_input = ft.TextField(
        label="Calle",
        hint_text="Nombre de la calle",
        prefix_icon=ft.Icons.HOME_OUTLINED,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_calle", "") if editando else "",
    )

    numero_input = ft.TextField(
        label="Número",
        hint_text="No.",
        prefix_icon=ft.Icons.NUMBERS,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=str(getattr(cliente, "cliente_numero", "")) if editando else "",
    )

    municipio_input = ft.TextField(
        label="Municipio",
        hint_text="Municipio",
        prefix_icon=ft.Icons.LOCATION_CITY,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_municipio", "") if editando else "",
    )

    estado_input = ft.TextField(
        label="Estado",
        hint_text="Estado",
        prefix_icon=ft.Icons.MAP_OUTLINED,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=getattr(cliente, "cliente_estado", "") if editando else "",
    )

    codigopostal_input = ft.TextField(
        label="Código postal",
        hint_text="C.P.",
        prefix_icon=ft.Icons.MARKUNREAD_MAILBOX_OUTLINED,
        width=320,
        border_radius=10,
        filled=True,
        bgcolor=BLANCO,
        border_color=BORDE,
        focused_border_color=AZUL,
        cursor_color=AZUL,
        value=str(getattr(cliente, "cliente_codigopostal", "")) if editando else "",
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

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

        validaciones = [
            validar_nombre(nombre, campo="Nombre"),
            validar_correo(correo, obligatorio=False),
            validar_telefono(telefono),
            validar_nombre(calle, campo="Calle"),
            validar_nombre(municipio, campo="Municipio"),
            validar_nombre(estado, campo="Estado"),
        ]

        for es_valido, texto_error in validaciones:
            if not es_valido:
                mensaje.value = texto_error
                mensaje.color = ft.Colors.RED
                if p_page:
                    p_page.update()
                return

        if not numero:
            mensaje.value = "El número es obligatorio"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if not numero.isdigit():
            mensaje.value = "El número solo debe contener dígitos"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if not codigopostal:
            mensaje.value = "El código postal es obligatorio"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if not codigopostal.isdigit() or len(codigopostal) != 5:
            mensaje.value = "El código postal debe tener exactamente 5 dígitos"
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
                dao.actualizar(cliente_actualizado)
                regresar(f"Cliente '{nombre}' actualizado correctamente")
                return

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
            regresar(f"Cliente '{nombre}' registrado correctamente")
            return

        except Exception as error:
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

    columna_izquierda = ft.Column(
        controls=[
            nombre_input,
            correo_input,
            telefono_input,
            calle_input,
        ],
        spacing=15,
    )

    columna_derecha = ft.Column(
        controls=[
            numero_input,
            municipio_input,
            estado_input,
            codigopostal_input,
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
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Row(
                    controls=[columna_izquierda, columna_derecha],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
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
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            controls=[encabezado, cuerpo, pie],
            spacing=0,
        ),
    )