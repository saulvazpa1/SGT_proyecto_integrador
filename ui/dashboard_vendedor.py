import flet as ft
import math
import flet.canvas as cv

from dao.cliente_dao import ClienteDAO
from dao.pedido_dao import PedidoDAO


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


# 🔷 GRÁFICA DE BARRAS
def _grafica_barras(titulo, categorias, serie1, serie2):
    alto_maximo = 140
    valores = serie1 + serie2
    valor_maximo = max(valores) if valores else 1

    grupos = []
    for i, nombre in enumerate(categorias):
        alto1 = (serie1[i] / valor_maximo) * alto_maximo
        alto2 = (serie2[i] / valor_maximo) * alto_maximo

        grupos.append(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(width=20, height=alto1, bgcolor=ft.Colors.INDIGO_300),
                            ft.Container(width=20, height=alto2, bgcolor=ft.Colors.PINK_400),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        spacing=4,
                    ),
                    ft.Text(nombre, size=12),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    return ft.Container(
        expand=True,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                ft.Row(controls=grupos, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ],
        ),
    )


# 🔷 GRÁFICA DE PASTEL
def _grafica_pastel(titulo, secciones):
    total = sum(valor for valor, _, _ in secciones) or 1

    formas = []
    angulo_actual = -math.pi / 2

    for valor, color, _ in secciones:
        barrido = (valor / total) * 2 * math.pi
        formas.append(
            cv.Arc(
                x=0,
                y=0,
                width=180,
                height=180,
                start_angle=angulo_actual,
                sweep_angle=barrido,
                use_center=True,
                paint=ft.Paint(style=ft.PaintingStyle.FILL, color=color),
            )
        )
        angulo_actual += barrido

    lienzo = cv.Canvas(width=180, height=180, shapes=formas)

    leyenda = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(width=10, height=10, bgcolor=color),
                    ft.Text(f"{etiqueta} ({valor})"),
                ]
            )
            for valor, color, etiqueta in secciones
        ]
    )

    return ft.Container(
        expand=True,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                ft.Row([lienzo, leyenda], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )


# 🔷 DASHBOARD PRINCIPAL
def dashboard_vendedor(page=None):

    # 🔹 Datos
    try:
        clientes = ClienteDAO().obtener_todos()
    except:
        clientes = []

    try:
        pedidos = PedidoDAO().obtener_todos()
    except:
        pedidos = []

    total_clientes = len(clientes)
    total_pedidos = len(pedidos)

    estados_finales = {"Entregado", "Completado", "Cancelado"}
    pendientes = sum(
        1 for p in pedidos if str(getattr(p, "pedido_estado", "")) not in estados_finales
    )

    try:
        total_vendido = sum(float(getattr(p, "pedido_total", 0) or 0) for p in pedidos)
    except:
        total_vendido = 0

    # 🔹 ROLES (CORREGIDO)
    admins = 0
    vendedores = 0
    produccion = 0

    for c in clientes:
        rol = str(getattr(c, "rol_id", "")).lower()
        if "admin" in rol:
            admins += 1
        elif "vendedor" in rol:
            vendedores += 1
        elif "produccion" in rol:
            produccion += 1

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

    # 🔹 Gráficas
    grafica_barras = _grafica_barras(
        "Crecimiento",
        ["Ene", "Feb", "Mar"],
        [2, 4, 6],
        [10, 15, 20],
    )

    secciones = []
    if admins:
        secciones.append((admins, ft.Colors.PURPLE_300, "Admin"))
    if vendedores:
        secciones.append((vendedores, ft.Colors.INDIGO_300, "Vendedor"))
    if produccion:
        secciones.append((produccion, ft.Colors.TEAL_300, "Producción"))

    if not secciones:
        secciones = [(1, ft.Colors.GREY_300, "Sin datos")]

    grafica_pastel = _grafica_pastel("Roles", secciones)

    # 🔹 Layout final
    return ft.Column(
        controls=[
            tarjetas,
            ft.Row(
                controls=[grafica_barras, grafica_pastel],
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        spacing=25,
    )