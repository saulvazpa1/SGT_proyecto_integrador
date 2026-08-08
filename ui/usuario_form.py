import flet as ft
from database.conexion import Conexion
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from ui.validaciones import validar_nombre, validar_correo, validar_password, validar_telefono

def _obtener_roles():
    """ (rol_id, rol_nombre) """
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT rol_id, rol_nombre FROM roles ORDER BY rol_nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas 


def usuario_form(regresar, usuario=None):
    editando = usuario is not None

    roles = _obtener_roles()  
    nombre_a_id = {nombre: str(rid) for rid, nombre in roles}

    nombre_input = ft.TextField(
        label="Nombre",
        hint_text="Ej: Juan",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=320,
        border_radius=6,
        value=usuario.usuario_nombre if editando else "",
    )

    apellidop_input = ft.TextField(
        label="Apellido paterno",
        hint_text="Ej: Pérez",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        width=320,
        border_radius=6,
        value=getattr(usuario, "usuario_apellidop", "") if editando else "",
    )

    apellidom_input = ft.TextField(
        label="Apellido materno",
        hint_text="Opcional (Ej: López)",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        width=320,
        border_radius=6,
        value=getattr(usuario, "usuario_apellidom", "") if editando else "",
    )

    telefono_input = ft.TextField(
        label="Teléfono",
        hint_text="Ej. 10 dígitos",
        prefix_icon=ft.Icons.PHONE_OUTLINED,
        width=320,
        border_radius=6,
        value=usuario.usuario_telefono if editando else "",
    )

    correo_input = ft.TextField(
        label="Correo electrónico",
        hint_text="Ej: correo@ejemplo.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        width=320,
        border_radius=6,
        value=usuario.usuario_correo if editando else "",
    )

    password_input = ft.TextField(
        label="Contraseña" if not editando else "Nueva contraseña",
        hint_text="Mínimo 8 caracteres" if not editando else "Déjalo vacío si no cambiarás la contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        width=320,
        border_radius=6,
        password=True,
        can_reveal_password=True,
        value="",
    )

    valor_inicial_rol = None
    if editando:
        nombre_rol_actual = str(getattr(usuario, "rol_id", ""))
        valor_inicial_rol = nombre_a_id.get(nombre_rol_actual)

   
    rol_dropdown = ft.Dropdown(
        label="Rol",
        hint_text="Selecciona un rol",
        width=320,
        value=valor_inicial_rol,
        options=[
            ft.dropdown.Option(key=str(rid), text=nombre)
            for rid, nombre in roles
        ],
    )

    rol_campo = ft.Row(
        controls=[
            
            rol_dropdown,
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    mensaje = ft.Text("", color=ft.Colors.RED)

    def guardar_usuario(e):
        nombre = (nombre_input.value or "").strip()
        apellidop = (apellidop_input.value or "").strip()
        apellidom = (apellidom_input.value or "").strip()
        telefono = (telefono_input.value or "").strip()
        correo = (correo_input.value or "").strip()
        password = password_input.value or ""
        rol_id_seleccionado = rol_dropdown.value

        validaciones = [
            validar_nombre(nombre, campo="Nombre"),
            validar_nombre(apellidop, campo="Apellido paterno"),
            validar_nombre(apellidom, campo="Apellido materno", obligatorio=False),
            validar_correo(correo),
            validar_telefono(telefono),
            validar_password(password, obligatorio=not editando),
        ]

        for es_valido, texto_error in validaciones:
            if not es_valido:
                mensaje.value = texto_error
                mensaje.color = ft.Colors.RED
                e.page.update()
                return

        if not rol_id_seleccionado:
            mensaje.value = "Selecciona un rol"
            mensaje.color = ft.Colors.RED
            e.page.update()
            return

        try:
            dao = UsuarioDAO()

            if editando:
                password_final = password if password else getattr(usuario, "usuario_password", "")

                usuario_actualizado = Usuario(
                    usuario_id=usuario.usuario_id,
                    usuario_nombre=nombre,
                    usuario_apellidop=apellidop,
                    usuario_apellidom=apellidom,
                    usuario_telefono=telefono,
                    usuario_correo=correo,
                    usuario_password=password_final,
                    rol_id=int(rol_id_seleccionado),
                )
                dao.actualizar(usuario_actualizado)
                regresar(f"Usuario '{nombre}' actualizado correctamente")
                return

            nuevo_id = dao.obtener_ultimo_id() + 1
            nuevo_usuario = Usuario(
                usuario_id=nuevo_id,
                usuario_nombre=nombre,
                usuario_apellidop=apellidop,
                usuario_apellidom=apellidom,
                usuario_telefono=telefono,
                usuario_correo=correo,
                usuario_password=password,
                rol_id=int(rol_id_seleccionado),
            )
            dao.insertar(nuevo_usuario)
            regresar(f"Usuario '{nombre}' registrado correctamente")
            return

        except Exception as error:
            mensaje.value = f"Error al guardar el usuario: {error}"
            mensaje.color = ft.Colors.RED

        e.page.update()

    encabezado = ft.Container(
        bgcolor=ft.Colors.LIGHT_BLUE_500,
        padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Editar usuario" if editando else "Registrar nuevo usuario",
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
            apellidop_input,
            apellidom_input,
            correo_input,
        ],
        spacing=15,
    )

    columna_derecha = ft.Column(
        controls=[
            password_input,
            telefono_input,
            rol_campo,
        ],
        spacing=15,
    )

    cuerpo = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Modifica los datos del usuario" if editando else "Captura los datos del nuevo usuario",
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
                    "Guardar cambios" if editando else "Registrar usuario",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.LIGHT_BLUE_500,
                    color=ft.Colors.WHITE,
                    on_click=guardar_usuario,
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