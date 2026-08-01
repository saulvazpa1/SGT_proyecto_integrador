import flet as ft
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO


def cliente_form(regresar, cliente=None, page=None):
    editando = cliente is not None

    nombre_input = ft.TextField(
        label="Nombre:",
        width=320,
        border_radius=6,
        value=getattr(cliente, "cliente_nombre", "") if editando else "",
    )

    correo_input = ft.TextField(
        label="Correo (opcional):",
        width=320,
        border_radius=6,
        value=getattr(cliente, "cliente_correo", "") if editando else "",
    )

    telefono_input = ft.TextField(
        label="Teléfono:",
        width=320,
        border_radius=6,
        value=getattr(cliente, "cliente_telefono", "") if editando else "",
    )

  
    calle_input = ft.TextField(
        label="Calle:",
        width=210,
        border_radius=6,
        value=getattr(cliente, "cliente_calle", "") if editando else "",
    )

    numero_input = ft.TextField(
        label="Número:",
        width=210,
        border_radius=6,
        value=str(getattr(cliente, "cliente_numero", "")) if editando else "",
    )

    municipio_input = ft.TextField(
        label="Municipio:",
        width=210,
        border_radius=6,
        value=getattr(cliente, "cliente_municipio", "") if editando else "",
    )

    estado_input = ft.TextField(
        label="Estado:",
        width=210,
        border_radius=6,
        value=getattr(cliente, "cliente_estado", "") if editando else "",
    )

    codigopostal_input = ft.TextField(
        label="Código postal:",
        width=210,
        border_radius=6,
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
        bgcolor=ft.Colors.LIGHT_BLUE_500,
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
                    color=ft.Colors.BLUE_GREY_600,
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
                    bgcolor=ft.Colors.LIGHT_BLUE_500,
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
            controls=[
                encabezado,
                cuerpo,
                pie,
            ],
            spacing=0,
        ),
    )