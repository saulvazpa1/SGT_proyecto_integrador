import math
import flet as ft
import flet.canvas as cv
from dao.usuario_dao import UsuarioDAO


def _tarjeta_kpi(titulo, valor, subtitulo, color):
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
                        ft.Icon(ft.Icons.PEOPLE_OUTLINED, size=16, color=ft.Colors.BLUE_GREY_300),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(str(valor), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text(subtitulo, size=12, color=ft.Colors.BLUE_GREY_500),
            ],
            spacing=4,
        ),
    )


def _grafica_barras(titulo, categorias, serie1, serie2, color1=ft.Colors.INDIGO_300, color2=ft.Colors.PINK_400):
    """
    categorias: lista de nombres (ej. ["Ene", "Feb", "Mar"])
    serie1 / serie2: listas de números, mismo largo que categorias
    """
    alto_maximo = 140
    valor_maximo = max(serie1 + serie2) or 1

    grupos = []
    for i, nombre in enumerate(categorias):
        alto1 = (serie1[i] / valor_maximo) * alto_maximo
        alto2 = (serie2[i] / valor_maximo) * alto_maximo

        grupos.append(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(width=20, height=alto1, bgcolor=color1, border_radius=ft.BorderRadius.only(top_left=4, top_right=4)),
                            ft.Container(width=20, height=alto2, bgcolor=color2, border_radius=ft.BorderRadius.only(top_left=4, top_right=4)),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        spacing=4,
                    ),
                    ft.Text(nombre, size=12, color=ft.Colors.BLUE_GREY_600),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            )
        )

    leyenda = ft.Row(
        controls=[
            ft.Row([ft.Container(width=10, height=10, bgcolor=color1, border_radius=5), ft.Text("Nuevos", size=12)], spacing=5),
            ft.Row([ft.Container(width=10, height=10, bgcolor=color2, border_radius=5), ft.Text("Activos", size=12)], spacing=5),
        ],
        spacing=20,
    )

    return ft.Container(
        expand=True,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                leyenda,
                ft.Row(controls=grupos, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ],
            spacing=15,
        ),
    )


def _grafica_pastel(titulo, secciones, tamano=180):
    """
    secciones: lista de tuplas (valor, color, etiqueta)
    """
    total = sum(valor for valor, _, _ in secciones) or 1

    formas = []
    angulo_actual = -math.pi / 2  # empieza arriba
    for valor, color, _ in secciones:
        barrido = (valor / total) * 2 * math.pi
        formas.append(
            cv.Arc(
                x=0,
                y=0,
                width=tamano,
                height=tamano,
                start_angle=angulo_actual,
                sweep_angle=barrido,
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


def dashboard_admin(page=None):
    
    try:
        usuarios = UsuarioDAO().obtener_todos()
    except Exception:
        usuarios = []

    total_usuarios = len(usuarios)
    
    # Conteo por estado
    activos = sum(1 for u in usuarios if bool(getattr(u, "usuario_estado", True)))
    inactivos = total_usuarios - activos
    porcentaje_activos = int((activos / total_usuarios) * 100) if total_usuarios > 0 else 0

   
    admins = sum(1 for u in usuarios if getattr(u, "rol_id", None) == 1)
    vendedores = sum(1 for u in usuarios if getattr(u, "rol_id", None) == 2)
    produccion = sum(1 for u in usuarios if getattr(u, "rol_id", None) == 3)

    # --- Tarjetas KPI ---
    tarjetas = ft.Row(
        controls=[
            _tarjeta_kpi("Total Usuarios", total_usuarios, "Registrados en BD", ft.Colors.BLUE_400),
            _tarjeta_kpi("Activos", activos, f"{porcentaje_activos}% del total", ft.Colors.GREEN_400),
            _tarjeta_kpi("Inactivos", inactivos, "Usuarios deshabilitados", ft.Colors.AMBER_400),
            _tarjeta_kpi("Administradores", admins, "Acceso total", ft.Colors.PURPLE_400),
        ],
        wrap=True,
        spacing=20,
    )

    # --- Gráfica de barras ---
    grafica_barras = _grafica_barras(
        "Crecimiento de Usuarios",
        categorias=["Ene", "Feb", "Mar"],
        serie1=[2, 4, 6],
        serie2=[10, 15, 20],
    )

    # --- Gráfica de pastel por Distribución de Roles ---
    secciones_roles = []
    if admins > 0:
        secciones_roles.append((admins, ft.Colors.PURPLE_300, "Admin"))
    if vendedores > 0:
        secciones_roles.append((vendedores, ft.Colors.INDIGO_300, "Vendedor"))
    if produccion > 0:
        secciones_roles.append((produccion, ft.Colors.TEAL_300, "Producción"))

    if not secciones_roles:
        secciones_roles = [(1, ft.Colors.GREY_300, "Sin datos")]

    grafica_pastel = _grafica_pastel(
        "Distribución por Roles",
        secciones=secciones_roles,
    )

    return ft.Column(
        controls=[
            tarjetas,
            ft.Row(
                controls=[grafica_barras, grafica_pastel],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
        spacing=25,
    )