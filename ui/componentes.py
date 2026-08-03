import threading
import flet as ft
from ui.notificaciones import obtener_notificaciones, contar_no_leidas, marcar_todas_leidas


def mostrar_notificacion(page: ft.Page, titulo: str, subtitulo: str = "", tipo: str = "exito", duracion: float = 4.0):
    """
    Muestra una notificación flotante en la esquina superior derecha,
    cerca del icono de notificaciones. Se oculta sola después de 'duracion' segundos.
    tipo: 'exito' | 'error'
    """
    estilos = {
        "exito": {
            "bgcolor_icono": ft.Colors.GREEN_50,
            "color_icono": ft.Colors.GREEN_600,
            "icono": ft.Icons.CHECK_CIRCLE,
        },
        "error": {
            "bgcolor_icono": ft.Colors.RED_50,
            "color_icono": ft.Colors.RED_600,
            "icono": ft.Icons.ERROR,
        },
    }
    estilo = estilos.get(tipo, estilos["exito"])

    icono = ft.Container(
        width=36,
        height=36,
        border_radius=18,
        alignment=ft.Alignment.CENTER,
        bgcolor=estilo["bgcolor_icono"],
        content=ft.Icon(icon=estilo["icono"], size=20, color=estilo["color_icono"]),
    )

    contenedor = ft.Container(
        top=75,
        right=20,
        width=380,
        padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        icono,
                        ft.Column(
                            controls=[
                                ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD),
                                ft.Text(subtitulo, size=12, color=ft.Colors.BLUE_GREY_400),
                            ],
                            spacing=2,
                            tight=True,
                        ),
                    ],
                    spacing=12,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=18,
                    icon_color=ft.Colors.BLUE_GREY_300,
                ),
            ],
        ),
    )

    ya_cerrado = {"valor": False}

    def cerrar(e=None):
        if ya_cerrado["valor"]:
            return
        ya_cerrado["valor"] = True
        if contenedor in page.overlay:
            page.overlay.remove(contenedor)
            page.update()

    contenedor.content.controls[1].on_click = cerrar

    page.overlay.append(contenedor)
    page.update()

    temporizador = threading.Timer(duracion, cerrar)
    temporizador.daemon = True
    temporizador.start()


def abrir_notificaciones(page: ft.Page):
    """
    Se conecta al icono de la campana en main_window.py.
    Consulta las notificaciones reales guardadas en la base de datos
    (ver ui/notificaciones.py) y muestra la más reciente como toast,
    indicando cuántas más hay sin leer. Al abrir, marca todas como leídas.
    """
    notifs = obtener_notificaciones()

    if not notifs:
        mostrar_notificacion(page, "Notificaciones", "No tienes notificaciones nuevas", "exito")
        return

    ultima = notifs[0]
    no_leidas = contar_no_leidas()

    subtitulo = ultima["mensaje"]
    if no_leidas > 1:
        subtitulo += f"  (+{no_leidas - 1} más)"

    mostrar_notificacion(page, "Notificaciones", subtitulo, "exito")
    marcar_todas_leidas()