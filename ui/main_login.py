import flet as ft
import subprocess
import sys
from ui.administrador import administrador
from ui.vendedor import vendedor
from ui.produccion import produccion
from dao.usuario_dao import UsuarioDAO

def main_login(page: ft.Page):
    page.title = "SGPT - Inicio de sesión"
    page.window.width = 1000
    page.window.height = 600
    page.window.resizable = False
    page.bgcolor = "#f2f2f2"

    logo = ft.Column(
        controls = [
            ft.Image(
                src = "logo.png",
                width = 280,
                height = 340
            ),
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
    )
    
    correo = ft.TextField(
        label = "Correo",
        hint_text = "Ejemplo@gmail.com",
        width = 340,
        height = 55,
        prefix_icon = ft.Icons.EMAIL
    )

    password = ft.TextField(
        label = "Contraseña",
        width = 340,
        height = 55,
        password = True,
        can_reveal_password = True,
        prefix_icon = ft.Icons.LOCK
    )

    mensaje = ft.Text(color="red")

    def iniciar(e):
        usuario_dao = UsuarioDAO()

        usuario = usuario_dao.iniciar_sesion(
            correo.value,
            password.value
        )

        if usuario:
            print("Rol:", usuario.rol_id)
            print(type(usuario.rol_id))
            mensaje.value = f"Bienvenido {usuario.usuario_nombre}"
            mensaje.color = "green"

            if usuario.rol_id == 1:
                page.clean()
                administrador(page)

            elif usuario.rol_id == 2:
                page.clean()
                vendedor(page)
            elif usuario.rol_id == 3:
                page.clean()
                produccion(page)
        else:
            mensaje.value = "Correo o contraseña incorrectos"
            mensaje.color = "red"
        page.update()

    boton = ft.ElevatedButton(
        on_click = iniciar,
        content = ft.Text(
            "Iniciar sesión",
            size = 16,
            weight = ft.FontWeight.BOLD,
            color = "white",
        ),
        width = 340,
        height = 50,
        style = ft.ButtonStyle(
            bgcolor = "#1E88E5",
            shape = ft.RoundedRectangleBorder(radius=8)
        ),
    )

    formulario = ft.Column(
        controls = [
            ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                size = 70, 
                color = "blue"
            ),
            ft.Text(
                "Bienvenido",
                size = 32,
                weight = ft.FontWeight.BOLD
            ),
            correo,
            password,
            boton,
            mensaje
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        spacing = 20
    )

    page.add(
        ft.Row(
            controls = [
                ft.Container(
                    expand = True,
                    alignment = ft.alignment.Alignment(0,0),
                    content = logo
                ),
                ft.VerticalDivider(
                    width = 2,
                    color = "#CFCFCF"
                ),
                ft.Container(
                    expand = 1,
                    alignment = ft.alignment.Alignment(0,0),
                    content = formulario
                )
            ],
            expand=True,
            vertical_alignment = ft.CrossAxisAlignment.CENTER   
        )
    )