import math
import flet as ft
import flet.canvas as cv
from dao.usuario_dao import UsuarioDAO
from dao.producto_dao import ProductoDAO
from dao.pedido_dao import PedidoDAO


def _tarjeta_kpi(titulo, valor, subtitulo, color, icono=ft.Icons.INSIGHTS, on_click=None):
    return ft.Container(
        width=210,
        padding=18,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        ink=on_click is not None,
        on_click=on_click,
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
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color=ft.Colors.BLUE_GREY_200) if on_click else ft.Container(),
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
                    ft.Text(
                        f"{etiqueta} — {round((valor / total) * 100)}% ({valor})",
                        size=12,
                        color=ft.Colors.BLUE_GREY_700,
                    ),
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


def dashboard_admin(
    page=None,
    on_ir_usuarios=None,
    on_ir_productos=None,
    on_ir_pedidos=None,
    on_ir_administradores=None,
):

    try:
        usuarios = UsuarioDAO().obtener_todos()
    except Exception:
        usuarios = []

    try:
        productos = ProductoDAO().obtener_todos()
    except Exception:
        productos = []

    try:
        pedidos = PedidoDAO().obtener_todos()
    except Exception:
        pedidos = []

    total_usuarios = len(usuarios)
    total_productos = len(productos)
    total_pedidos = len(pedidos)

    try:
        ingresos_totales = sum(float(p.pedido_total or 0) for p in pedidos)
    except Exception:
        ingresos_totales = 0
    ingresos_texto = f"${ingresos_totales:,.2f}"

    conteo_por_rol = {}
    for u in usuarios:
        nombre_rol = str(getattr(u, "rol_id", "") or "Sin rol").strip()
        conteo_por_rol[nombre_rol] = conteo_por_rol.get(nombre_rol, 0) + 1

    admins = conteo_por_rol.get("Administrador", 0)

 
    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Usuarios", total_usuarios, "Registrados en el sistema", ft.Colors.BLUE_400, ft.Icons.PEOPLE_OUTLINED, on_click=on_ir_usuarios),
            _tarjeta_kpi("Productos", total_productos, "En catálogo", ft.Colors.TEAL_400, ft.Icons.INVENTORY_2_OUTLINED, on_click=on_ir_productos),
            _tarjeta_kpi("Pedidos", total_pedidos, "Registrados en total", ft.Colors.ORANGE_400, ft.Icons.SHOPPING_CART_OUTLINED, on_click=on_ir_pedidos),
            _tarjeta_kpi("Ingresos", ingresos_texto, "Suma de todos los pedidos", ft.Colors.GREEN_400, ft.Icons.PAID_OUTLINED, on_click=on_ir_pedidos),
            _tarjeta_kpi("Administradores", admins, "Acceso total", ft.Colors.PURPLE_400, ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED, on_click=on_ir_administradores),
        ],
        wrap=True,
        spacing=16,
        run_spacing=16,
    )

    
    secciones_roles = [
        (cantidad, _PALETA[i % len(_PALETA)], nombre_rol)
        for i, (nombre_rol, cantidad) in enumerate(conteo_por_rol.items())
        if cantidad > 0
    ]
    if not secciones_roles:
        secciones_roles = [(1, ft.Colors.GREY_300, "Sin datos")]

    grafica_roles = _grafica_pastel("Distribución por roles", secciones_roles)

    
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

   
    ventas_por_producto = {}
    for p in pedidos:
        nombre_producto = str(getattr(p, "producto_id", "Producto"))
        cantidad = getattr(p, "pedido_cantidad", 0) or 0
        ventas_por_producto[nombre_producto] = ventas_por_producto.get(nombre_producto, 0) + cantidad

    top_productos = sorted(ventas_por_producto.items(), key=lambda item: item[1], reverse=True)[:5]

    grafica_top_productos = _grafica_barras_ranking(
        "Top 5 productos más vendidos (por unidades pedidas)",
        top_productos,
        color=ft.Colors.INDIGO_400,
    )

    return ft.Column(
        controls=[
            tarjetas,
            ft.Row(
                controls=[grafica_roles, grafica_estados],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
            grafica_top_productos,
        ],
        spacing=24,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )