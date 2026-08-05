import flet as ft
import math
import flet.canvas as cv

from dao.cliente_dao import ClienteDAO
from dao.pedido_dao import PedidoDAO
from dao.producto_dao import ProductoDAO


# 🔷 TARJETA KPI
def _tarjeta_kpi(titulo, valor, subtitulo, color, icono):
    return ft.Container(
        width=220,
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


# 🔷 GRÁFICA DE PASTEL
def _grafica_pastel(titulo, secciones, tamano=170):
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
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Row(
                    controls=[lienzo, leyenda],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=25,
                ),
            ],
            spacing=15,
        ),
    )


# 🔷 GRÁFICA DE BARRAS (RANKING)
def _grafica_barras_ranking(titulo, items, color=ft.Colors.INDIGO_400):
    valor_maximo = max((v for _, v in items), default=1) or 1

    filas = []
    for etiqueta, valor in items:
        ancho_proporcional = (valor / valor_maximo) * 260

        filas.append(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(etiqueta, size=13, color=ft.Colors.BLUE_GREY_800),
                            ft.Text(str(valor), size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        width=max(ancho_proporcional, 4),
                        height=10,
                        bgcolor=color,
                        border_radius=5,
                    ),
                ],
                spacing=4,
            )
        )

    if not filas:
        filas = [ft.Text("Aún no hay pedidos registrados", size=13, color=ft.Colors.BLUE_GREY_400)]

    return ft.Container(
        expand=True,
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Column(controls=filas, spacing=14),
            ],
            spacing=15,
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
    """Intenta obtener un nombre legible del producto; si no existe, usa el id."""
    for atributo in ("producto_nombre", "nombre", "producto_descripcion"):
        valor = getattr(producto, atributo, None)
        if valor:
            return str(valor)
    return str(getattr(producto, "producto_id", producto))


# 🔷 DASHBOARD PRINCIPAL
def dashboard_vendedor(page=None):

    # 🔹 Datos reales
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

    # 🔹 KPI
    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Clientes", total_clientes, "Registrados", ft.Colors.BLUE_400, ft.Icons.PEOPLE),
            _tarjeta_kpi("Pedidos", total_pedidos, "Total", ft.Colors.INDIGO_400, ft.Icons.SHOPPING_CART),
            _tarjeta_kpi("Pendientes", pendientes, "Por completar", ft.Colors.AMBER_400, ft.Icons.WARNING),
            _tarjeta_kpi("Total vendido", f"${total_vendido:,.2f}", "Ingresos", ft.Colors.GREEN_400, ft.Icons.ATTACH_MONEY),
        ],
        wrap=True,
        spacing=20,
    )

    # 🔹 Pedidos por estado (real)
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

    # 🔹 Top 5 productos más vendidos (real)
    mapa_nombres = {str(getattr(prod, "producto_id", "")): _nombre_producto(prod) for prod in productos}

    ventas_por_producto = {}
    for p in pedidos:
        producto_id = str(getattr(p, "producto_id", ""))
        cantidad = getattr(p, "pedido_cantidad", 0) or 0
        etiqueta = mapa_nombres.get(producto_id, producto_id or "Producto")
        ventas_por_producto[etiqueta] = ventas_por_producto.get(etiqueta, 0) + cantidad

    top_productos = sorted(ventas_por_producto.items(), key=lambda item: item[1], reverse=True)[:5]

    grafica_top_productos = _grafica_barras_ranking(
        "Top 5 productos más vendidos (por unidades pedidas)",
        top_productos,
        color=ft.Colors.PINK_400,
    )

    # 🔹 Layout final
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
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )