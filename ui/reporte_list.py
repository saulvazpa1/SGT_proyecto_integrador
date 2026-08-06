import os
import flet as ft
from ui.componentes import mostrar_notificacion
from ui.reporte_form import generar_reporte_inventario, generar_reporte_ventas


def _tarjeta_reporte(titulo, descripcion, icono, color, on_click):
    return ft.Container(
        width=320,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1.5, color),
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Icon(icono, size=32, color=color),
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text(descripcion, size=12, color=ft.Colors.BLUE_GREY_500),
                ft.ElevatedButton(
                    "Generar PDF",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    on_click=on_click,
                ),
            ],
            spacing=10,
        ),
    )


def reportes_list(page: ft.Page):

    def _generar(generador, nombre_reporte, e=None):
        try:
            ruta = generador()
            mostrar_notificacion(page, f"{nombre_reporte} generado", f"Guardado en: {ruta}", "exito")
            try:
                os.startfile(ruta)  # abre el PDF automáticamente (Windows)
            except Exception:
                pass
        except Exception as ex:
            mostrar_notificacion(page, "Error al generar el reporte", str(ex), "error")

    tarjetas = ft.Row(
        controls=[
            _tarjeta_reporte(
                "Inventario de Productos",
                "Listado completo de productos, con precio, stock y el valor total de tu inventario.",
                ft.Icons.INVENTORY_2,
                ft.Colors.TEAL_400,
                lambda e: _generar(generar_reporte_inventario, "Reporte de inventario", e),
            ),
            _tarjeta_reporte(
                "Ventas y Pedidos",
                "Listado de todos los pedidos, con sus totales, estados e ingresos generados.",
                ft.Icons.SHOPPING_CART,
                ft.Colors.INDIGO_400,
                lambda e: _generar(generar_reporte_ventas, "Reporte de ventas", e),
            ),
        ],
        wrap=True,
        spacing=20,
    )

    return ft.Column(
        controls=[
            ft.Text("Reportes", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Genera reportes en PDF ",
                size=13,
                color=ft.Colors.BLUE_GREY_600,
            ),
            tarjetas,
        ],
        spacing=20,
        expand=True,
    )