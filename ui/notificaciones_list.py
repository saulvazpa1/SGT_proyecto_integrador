import flet as ft
from ui.notificaciones import (
    obtener_notificaciones,
    marcar_todas_leidas,
    eliminar_notificacion,
    eliminar_todas_las_notificaciones,
)


def _icono_para_mensaje(mensaje):
    texto = (mensaje or "").lower()
    if "eliminad" in texto or "cancelad" in texto:
        return ft.Icons.CANCEL, ft.Colors.RED_600, ft.Colors.RED_50
    if "actualizad" in texto or "modificad" in texto:
        return ft.Icons.EDIT_NOTIFICATIONS, ft.Colors.AMBER_700, ft.Colors.AMBER_50
    return ft.Icons.INVENTORY_2, ft.Colors.BLUE_700, ft.Colors.BLUE_50


def _tarjeta_notificacion(notif, on_eliminar):
    icono, color_icono, color_fondo = _icono_para_mensaje(notif["mensaje"])

    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=4, vertical=14),
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.BLUE_GREY_100)),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=34,
                    height=34,
                    border_radius=17,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=color_fondo,
                    content=ft.Icon(icono, size=18, color=color_icono),
                ),
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Sin leer",
                                    size=11,
                                    color=ft.Colors.BLUE_600,
                                    weight=ft.FontWeight.BOLD,
                                    visible=not notif["leida"],
                                ),
                                ft.Text(notif["fecha"], size=12, color=ft.Colors.BLUE_GREY_400),
                            ],
                        ),
                        ft.Text(
                            notif["mensaje"],
                            size=14,
                            color=ft.Colors.BLUE_GREY_800,
                            weight=ft.FontWeight.BOLD if not notif["leida"] else ft.FontWeight.NORMAL,
                        ),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    icon_color=ft.Colors.BLUE_GREY_300,
                    tooltip="Eliminar",
                    on_click=lambda e, nid=notif["id"]: on_eliminar(nid),
                ),
            ],
            spacing=12,
        ),
    )


def mostrar_panel_notificaciones(page: ft.Page, al_cerrar=None):
    """
    Abre el panel de notificaciones como un overlay (AlertDialog), sin
    reemplazar el contenido de la pantalla. Se marca todo como leído al
    abrirlo.
    """

    lista_container = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    mensaje_vacio = ft.Text(
        "No tienes notificaciones",
        size=13,
        color=ft.Colors.BLUE_GREY_400,
        visible=False,
    )

    def cerrar_dialogo(e=None):
        page.pop_dialog()
        if al_cerrar:
            al_cerrar()

    def recargar():
        notifs = obtener_notificaciones()

        if not notifs:
            lista_container.controls = []
            mensaje_vacio.visible = True
        else:
            mensaje_vacio.visible = False
            lista_container.controls = [
                _tarjeta_notificacion(n, on_eliminar_una) for n in notifs
            ]

        page.update()

    def on_eliminar_una(notificacion_id):
        eliminar_notificacion(notificacion_id)
        recargar()

    def on_borrar_todo(e):
        eliminar_todas_las_notificaciones()
        recargar()

    marcar_todas_leidas()
    if al_cerrar:
        al_cerrar()

    encabezado = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Notificaciones", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Container(
                width=32,
                height=32,
                border_radius=16,
                bgcolor=ft.Colors.RED_500,
                alignment=ft.Alignment.CENTER,
                content=ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=ft.Colors.WHITE,
                    icon_size=16,
                    on_click=cerrar_dialogo,
                ),
            ),
        ],
    )

    pie = ft.Container(
        padding=ft.Padding.only(top=10),
        content=ft.OutlinedButton(
            "Borrar todo",
            icon=ft.Icons.DELETE_SWEEP,
            style=ft.ButtonStyle(
                color=ft.Colors.RED_700,
                side=ft.BorderSide(1, ft.Colors.RED_200),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=on_borrar_todo,
        ),
    )

    contenido_panel = ft.Container(
        width=460,
        bgcolor=ft.Colors.WHITE,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=25, color=ft.Colors.BLACK26, offset=ft.Offset(0, 6)),
        content=ft.Column(
            controls=[
                encabezado,
                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),
                ft.Container(
                    height=380,
                    content=ft.Column(controls=[lista_container, mensaje_vacio], scroll=ft.ScrollMode.AUTO),
                ),
                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),
                pie,
            ],
            spacing=14,
            tight=True,
        ),
    )

    dialogo = ft.AlertDialog(
        modal=True,
        content=contenido_panel,
        content_padding=0,
        bgcolor=ft.Colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=14),
    )

    page.show_dialog(dialogo)
    recargar()