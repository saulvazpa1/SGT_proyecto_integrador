import flet as ft
from dao.cliente_dao import ClienteDAO
from dao.pedido_dao import PedidoDAO


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


def dashboard_vendedor(page=None):

    try:
        clientes = ClienteDAO().obtener_todos()
    except Exception:
        clientes = []

    try:
        pedidos = PedidoDAO().obtener_todos()
    except Exception:
        pedidos = []

    total_clientes = len(clientes)
    total_pedidos = len(pedidos)

    estados_finales = {"Entregado", "Completado", "Cancelado"}
    pendientes = sum(
        1 for p in pedidos if str(getattr(p, "pedido_estado", "")) not in estados_finales
    )

    try:
        total_vendido = sum(float(getattr(p, "pedido_total", 0) or 0) for p in pedidos)
    except (TypeError, ValueError):
        total_vendido = 0

    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Clientes", total_clientes, "Registrados", ft.Colors.BLUE_400, ft.Icons.PEOPLE_OUTLINED),
            _tarjeta_kpi("Pedidos", total_pedidos, "Total generados", ft.Colors.INDIGO_400, ft.Icons.SHOPPING_CART_OUTLINED),
            _tarjeta_kpi("Pendientes", pendientes, "Por completar", ft.Colors.AMBER_400, ft.Icons.PENDING_ACTIONS),
            _tarjeta_kpi("Total vendido", f"${total_vendido:,.2f}", "Suma de pedidos", ft.Colors.GREEN_400, ft.Icons.ATTACH_MONEY),
        ],
        wrap=True,
        spacing=20,
    )

    return ft.Column(
        controls=[tarjetas],
        spacing=25,
    )