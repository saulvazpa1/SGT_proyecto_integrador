import math
import flet as ft
import flet.canvas as cv
from dao.ordenes_produccion_dao import OrdenProduccionDAO
from dao.pedido_dao import PedidoDAO


def _tarjeta_kpi(titulo, valor, subtitulo, color, icono=ft.Icons.PRECISION_MANUFACTURING):
    return ft.Container(
        width=200,
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1.5, color),
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(titulo, size=13, color=ft.Colors.BLUE_GREY_700),
                        ft.Icon(icono, size=16, color=ft.Colors.BLUE_GREY_300),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(str(valor), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text(subtitulo, size=12, color=ft.Colors.BLUE_GREY_500),
            ],
            spacing=4,
        ),
    )


def _grafica_pastel(titulo, secciones, tamano=180):
    """secciones: lista de tuplas (valor, color, etiqueta)"""
    total = sum(valor for valor, _, _ in secciones) or 1

    formas = []
    angulo_actual = -math.pi / 2
    for valor, color, _ in secciones:
        barrido = (valor / total) * 2 * math.pi
        formas.append(
            cv.Arc(
                x=0, y=0, width=tamano, height=tamano,
                start_angle=angulo_actual, sweep_angle=barrido,
                use_center=True,
                paint=ft.Paint(style=ft.PaintingStyle.FILL, color=color),
            )
        )
        angulo_actual += barrido

    lienzo = cv.Canvas(width=tamano, height=tamano, shapes=formas)

    leyenda = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(width=10, height=10, bgcolor=color, border_radius=5),
                    ft.Text(f"{etiqueta} ({valor})", size=12),
                ],
                spacing=5,
            )
            for valor, color, etiqueta in secciones
        ],
        spacing=6,
    )

    return ft.Container(
        expand=True,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Row(
                    controls=[lienzo, leyenda],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
            ],
            spacing=15,
        ),
    )


_COLORES_ESTADO = {
    "pendiente": ft.Colors.AMBER_400,
    "cancelado": ft.Colors.RED_400,
    "completado": ft.Colors.GREEN_400,
    "entregado": ft.Colors.TEAL_400,
}
_PALETA_RESPALDO = [ft.Colors.BLUE_400, ft.Colors.INDIGO_400, ft.Colors.PURPLE_400, ft.Colors.CYAN_400]


def _color_para_estado(estado, indice_respaldo):
    estado_normalizado = (estado or "").lower()
    for clave, color in _COLORES_ESTADO.items():
        if clave in estado_normalizado:
            return color
    return _PALETA_RESPALDO[indice_respaldo % len(_PALETA_RESPALDO)]


def dashboard_produccion(page=None):

    try:
        ordenes = OrdenProduccionDAO().obtener_todos()
    except Exception:
        ordenes = []

    try:
        pedidos = PedidoDAO().obtener_todos()
    except Exception:
        pedidos = []

    total_ordenes = len(ordenes)

    conteo_por_estado = {}
    for o in ordenes:
        estado = str(getattr(o, "produccion_estado", "") or "Sin estado").strip()
        conteo_por_estado[estado] = conteo_por_estado.get(estado, 0) + 1

    def _contar(*palabras_clave):
        total = 0
        for estado, cantidad in conteo_por_estado.items():
            estado_norm = estado.lower()
            if any(palabra in estado_norm for palabra in palabras_clave):
                total += cantidad
        return total

    pendientes = _contar("pendiente")
    en_proceso = _contar("corte", "costura", "acabado", "proceso")
    completadas = _contar("completado", "entregado")

    pedidos_pendientes = sum(1 for p in pedidos if "pendiente" in str(getattr(p, "pedido_estado", "")).lower())

    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Órdenes totales", total_ordenes, "Registradas en el sistema", ft.Colors.BLUE_400),
            _tarjeta_kpi("Pendientes", pendientes, "Por iniciar", ft.Colors.AMBER_400, ft.Icons.HOURGLASS_EMPTY),
            _tarjeta_kpi("En proceso", en_proceso, "Corte, costura o acabado", ft.Colors.INDIGO_400, ft.Icons.AUTORENEW),
            _tarjeta_kpi("Completadas", completadas, "Listas o entregadas", ft.Colors.GREEN_400, ft.Icons.CHECK_CIRCLE),
            _tarjeta_kpi("Pedidos sin atender", pedidos_pendientes, "Esperando orden de producción", ft.Colors.RED_400, ft.Icons.PENDING_ACTIONS),
        ],
        wrap=True,
        spacing=20,
    )

    secciones_estado = [
        (cantidad, _color_para_estado(estado, i), estado)
        for i, (estado, cantidad) in enumerate(conteo_por_estado.items())
        if cantidad > 0
    ]
    if not secciones_estado:
        secciones_estado = [(1, ft.Colors.GREY_300, "Sin datos")]

    grafica_estado = _grafica_pastel("Órdenes por estado", secciones_estado)

    return ft.Column(
        controls=[
            tarjetas,
            ft.Row(controls=[grafica_estado], alignment=ft.MainAxisAlignment.START),
        ],
        spacing=25,
    )