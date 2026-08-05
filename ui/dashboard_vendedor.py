import math
import flet as ft
import flet.canvas as cv

from dao.cliente_dao import ClienteDAO
from dao.pedido_dao import PedidoDAO
from dao.producto_dao import ProductoDAO


def _tarjeta_kpi(titulo, valor, subtitulo, color, icono=ft.Icons.INSIGHTS):
    return ft.Container(
        width=210,
        padding=18,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.15, color),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(icono, size=18, color=color),
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Container(height=10),
                ft.Text(
                    str(valor),
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_900,
                ),
                ft.Text(titulo, size=13, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700),
                ft.Text(subtitulo, size=11, color=ft.Colors.BLUE_GREY_400),
            ],
            spacing=2,
        ),
    )


def _grafica_pastel(titulo, secciones, tamano=160):
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
                    ft.Text(f"{etiqueta} ({valor})", size=12, color=ft.Colors.BLUE_GREY_700),
                ],
                spacing=8,
            )
            for valor, color, etiqueta in secciones
        ],
        spacing=8,
    )

    return ft.Container(
        expand=True,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Container(height=8),
                ft.Row(
                    controls=[lienzo, leyenda],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
            ],
            spacing=10,
        ),
    )


def _grafica_barras_ranking(titulo, items, color=ft.Colors.INDIGO_400):
    valor_maximo = max((v for _, v in items), default=1) or 1

    filas = []
    for etiqueta, valor in items:
        ancho_proporcional = (valor / valor_maximo) * 280

        filas.append(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                etiqueta,
                                size=13,
                                color=ft.Colors.BLUE_GREY_800,
                                expand=True,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                str(valor),
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_900,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        width=max(ancho_proporcional, 6),
                        height=9,
                        bgcolor=color,
                        border_radius=6,
                    ),
                ],
                spacing=5,
            )
        )

    if not filas:
        filas = [ft.Text("Aún no hay pedidos registrados", size=13, color=ft.Colors.BLUE_GREY_400)]

    return ft.Container(
        expand=True,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Container(height=8),
                ft.Column(controls=filas, spacing=16),
            ],
            spacing=10,
        ),
    )


_PALETA = [
    ft.Colors.PURPLE_300,
    ft.Colors.INDIGO_300,
    ft.Colors.TEAL_300,
    ft.Colors.ORANGE_300,
    ft.Colors.PINK_300,
    ft.Colors.CYAN_300,
]


def _nombre_producto(producto):
    for atributo in ("producto_nombre", "nombre", "producto_descripcion"):
        valor = getattr(producto, atributo, None)
        if valor:
            return str(valor)
    return str(getattr(producto, "producto_id", producto))


def dashboard_vendedor(page=None):

    try:
        clientes = ClienteDAO().obtener_todos()
    except Exception:
        clientes = []

    try:
        pedidos = PedidoDAO().obtener_todos()
    except Exception:
        pedidos = []

    try:
        productos = ProductoDAO().obtener_todos()
    except Exception:
        productos = []

    total_clientes = len(clientes)
    total_pedidos = len(pedidos)

    estados_finales = {"Entregado", "Completado", "Cancelado"}
    pendientes = sum(
        1 for p in pedidos if str(getattr(p, "pedido_estado", "")) not in estados_finales
    )

    try:
        total_vendido = sum(float(getattr(p, "pedido_total", 0) or 0) for p in pedidos)
    except Exception:
        total_vendido = 0

    # Tarjetas KPI 
    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Clientes", total_clientes, "Registrados", ft.Colors.BLUE_400, ft.Icons.PEOPLE_OUTLINED),
            _tarjeta_kpi("Pedidos", total_pedidos, "Total registrados", ft.Colors.INDIGO_400, ft.Icons.SHOPPING_CART_OUTLINED),
            _tarjeta_kpi("Pendientes", pendientes, "Por completar", ft.Colors.AMBER_400, ft.Icons.WARNING_AMBER_ROUNDED),
            _tarjeta_kpi("Total vendido", f"${total_vendido:,.2f}", "Ingresos generados", ft.Colors.GREEN_400, ft.Icons.ATTACH_MONEY),
        ],
        wrap=True,
        spacing=16,
        run_spacing=16,
    )

    # Pedidos por estado
    conteo_por_estado = {}
    for p in pedidos:
        estado = str(getattr(p, "pedido_estado", "") or "Sin estado").strip()
        conteo_por_estado[estado] = conteo_por_estado.get(estado, 0) + 1

    secciones_estado = [
        (cantidad, _PALETA[i % len(_PALETA)], estado)
        for i, (estado, cantidad) in enumerate(conteo_por_estado.items())
        if cantidad > 0
    ]
    if not secciones_estado:
        secciones_estado = [(1, ft.Colors.GREY_300, "Sin datos")]

    grafica_estados = _grafica_pastel("Pedidos por estado", secciones_estado)

    # Top 5 productos
    mapa_nombres = {
        str(getattr(prod, "producto_id", "")): _nombre_producto(prod)
        for prod in productos
    }

    ventas_por_producto = {}
    for p in pedidos:
        producto_id = str(getattr(p, "producto_id", ""))
        cantidad = getattr(p, "pedido_cantidad", 0) or 0
        etiqueta = mapa_nombres.get(producto_id, producto_id or "Producto")
        ventas_por_producto[etiqueta] = ventas_por_producto.get(etiqueta, 0) + cantidad

    top_productos = sorted(ventas_por_producto.items(), key=lambda item: item[1], reverse=True)[:5]

    grafica_top_productos = _grafica_barras_ranking(
        "Top 5 productos más vendidos (por unidades)",
        top_productos,
        color=ft.Colors.PINK_400,
    )

    return ft.Column(
        controls=[
            tarjetas,
            ft.Row(
                controls=[grafica_estados, grafica_top_productos],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
        ],
        spacing=24,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )