import flet as ft
import asyncio
import time
from dao.usuario_dao import UsuarioDAO
from ui.main_window import main_window
from ui.main_window_vendedor import main_window_vendedor
from ui.main_window_produccion import main_window_produccion
from ui.colores import *


def main_login(page: ft.Page):
    page.title = "SGPT - Inicio de sesión"
    page.bgcolor = FONDO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family="Segoe UI")

    page.window.maximized = True
    page.window.resizable = True
    page.window.min_width = 1000
    page.window.min_height = 650
    page.bgcolor = "#f2f2f2"

    logo = ft.Column(
        controls=[
            ft.Image(
                src="logo.png",
                width=280,
                height=340
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    correo = ft.TextField(
        label="Correo",
        hint_text="ejemplo@gmail.com",
        width=340,
        height=55,
        prefix_icon=ft.Icons.EMAIL
    )

    password = ft.TextField(
        label="Contraseña",
        width=340,
        height=55,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK
    )

    mensaje = ft.Text(color="red")

    
    cargando = ft.ProgressRing(
        width=20,
        height=20,
        stroke_width=3,
        color=ft.Colors.WHITE,
        visible=False,
    )

    texto_boton = ft.Text(
        "Iniciar sesión",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    contenido_boton = ft.Row(
        controls=[cargando, texto_boton],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    boton = ft.ElevatedButton(
        content=contenido_boton,
        width=340,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=AZUL,
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )

    def volver_al_login():
        page.rol_id_actual = None
        page.usuario_id_actual = None
        page.usuario_nombre_actual = None
        page.clean()
        main_login(page)

    def pantalla_cargando(texto="Cargando tu panel..."):
        page.clean()
        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    controls=[
                        ft.ProgressRing(width=42, height=42, stroke_width=4, color=AZUL),
                        ft.Text(texto, size=16, color=ft.Colors.BLUE_GREY_600),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
            )
        )
        page.update()

    async def iniciar(e):

       
        cargando.visible = True
        texto_boton.value = "Iniciando sesión..."
        boton.disabled = True
        mensaje.value = ""
        page.update()

        try:
            usuario_dao = UsuarioDAO()

            correo_limpio = (correo.value or "").strip()
            password_limpio = (password.value or "").strip()

            usuario = usuario_dao.iniciar_sesion(
                correo_limpio,
                password_limpio
            )

            if usuario:
                print("Rol:", usuario.rol_id)
                mensaje.value = f"Bienvenido {usuario.usuario_nombre}"
                mensaje.color = "green"

                page.rol_id_actual = usuario.rol_id
                page.usuario_id_actual = usuario.usuario_id
                page.usuario_nombre_actual = usuario.usuario_nombre

                # Pantalla de carga breve antes de mostrar el panel
                pantalla_cargando(f"Bienvenido {usuario.usuario_nombre}, cargando tu panel...")
                await asyncio.sleep(2.4)

                page.clean()

                if usuario.rol_id == 1:
                    main_window(page, on_logout=volver_al_login)
                elif usuario.rol_id == 2:
                    main_window_vendedor(page, on_logout=volver_al_login)
                elif usuario.rol_id == 3:
                    main_window_produccion(page, on_logout=volver_al_login)
                return
            else:
                mensaje.value = "Correo o contraseña incorrectos"
                mensaje.color = "red"

        except Exception as ex:
            mensaje.value = f"Error: {ex}"
            mensaje.color = "red"

        finally:
            
            cargando.visible = False
            texto_boton.value = "Iniciar sesión"
            boton.disabled = False
            page.update()

    boton.on_click = iniciar

    formulario = ft.Column(
        controls=[
            ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                size=70, 
                color="blue"
            ),
            ft.Text(
                "Bienvenido",
                size=32,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Ingresa tus datos para acceder al sistema",
                size=16,
                color=ft.Colors.GREY_500,
                weight=ft.FontWeight.NORMAL
            ),
            correo,
            password,
            boton,
            mensaje
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=logo
                ),
                ft.VerticalDivider(
                    width=2,
                    color="#CFCFCF"
                ),
                ft.Container(
                    expand=1,
                    alignment=ft.Alignment.CENTER,
                    content=formulario
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER   
        )
    )