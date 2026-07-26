from datetime import datetime
import flet as ft
from database.conexion import Conexion
from models.orden_produccion import OrdenProduccion
from dao.ordenes_produccion_dao import OrdenProduccionDAO


ESTADOS_SUGERIDOS = [
    "Pendiente",
    "En corte",
    "En costura",
    "En acabado",
    "Completado",
    "Entregado",
    "Cancelado",
]


def _obtener_pedidos():
    """(pedido_id, 'Pedido #N - Cliente')"""
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.pedido_id, c.cliente_nombre
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.cliente_id
        ORDER BY p.pedido_id DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [(pid, f"Pedido #{pid} — {nombre}") for pid, nombre in filas]


def _obtener_productos():
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT producto_id, producto_nombre FROM productos ORDER BY producto_nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def _obtener_encargados():
    """
   
    (para no dejar el formulario sin opciones).
    """
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT u.usuario_id, u.usuario_nombre, u.usuario_apellidop
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.rol_id
        WHERE r.rol_nombre ILIKE %s
        ORDER BY u.usuario_nombre
    """, ('%producci%',))
    filas = cursor.fetchall()

    if not filas:
        cursor.execute("SELECT usuario_id, usuario_nombre, usuario_apellidop FROM usuarios ORDER BY usuario_nombre")
        filas = cursor.fetchall()

    cursor.close()
    conexion.close()
    return [(uid, f"{nombre} {apellido}".strip()) for uid, nombre, apellido in filas]


def _parsear_fecha(texto):
    """Acepta 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM'. Regresa datetime o lanza ValueError."""
    texto = (texto or "").strip()
    for formato in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido: '{texto}' (usa AAAA-MM-DD o AAAA-MM-DD HH:MM)")


def orden_produccion_form(regresar, orden=None, page=None):
    editando = orden is not None

    pedidos = _obtener_pedidos()
    productos = _obtener_productos()
    encargados = _obtener_encargados()

    pedido_dropdown = ft.Dropdown(
        label="Pedido:",
        width=320,
        value=str(orden.pedido_id) if editando else None,
        options=[ft.dropdown.Option(key=str(pid), text=texto) for pid, texto in pedidos],
    )

    producto_dropdown = ft.Dropdown(
        label="Producto a fabricar:",
        width=320,
        value=str(orden.producto_id) if editando else None,
        options=[ft.dropdown.Option(key=str(pid), text=nombre) for pid, nombre in productos],
    )

    encargado_dropdown = ft.Dropdown(
        label="Encargado de producción:",
        width=320,
        value=str(orden.encargado_produccion_id) if editando else None,
        options=[ft.dropdown.Option(key=str(uid), text=nombre) for uid, nombre in encargados],
    )

    estados_disponibles = list(ESTADOS_SUGERIDOS)
    if editando and orden.produccion_estado and orden.produccion_estado not in estados_disponibles:
        estados_disponibles = [orden.produccion_estado] + estados_disponibles

    estado_dropdown = ft.Dropdown(
        label="Estado:",
        width=320,
        value=orden.produccion_estado if editando else "Pendiente",
        options=[ft.dropdown.Option(key=e, text=e) for e in estados_disponibles],
    )

    cantidad_input = ft.TextField(
        label="Cantidad a producir:",
        width=320,
        border_radius=6,
        value=str(orden.produccion_cantidad) if editando else "",
    )

    fecha_inicio_input = ft.TextField(
        label="Fecha de inicio (AAAA-MM-DD):",
        width=320,
        border_radius=6,
        value=orden.fecha_inicio.strftime("%Y-%m-%d") if editando and orden.fecha_inicio else datetime.now().strftime("%Y-%m-%d"),
    )

    fecha_entrega_input = ft.TextField(
        label="Fecha de entrega (opcional):",
        width=320,
        border_radius=6,
        value=orden.fecha_entrega.strftime("%Y-%m-%d") if editando and orden.fecha_entrega else "",
    )

    # --- Sección de tela y patrón ---
    tela_tipo_input = ft.TextField(
        label="Tipo de tela:",
        width=210,
        border_radius=6,
        value=orden.tela_tipo if editando and orden.tela_tipo else "",
    )
    tela_ancho_input = ft.TextField(
        label="Ancho de tela (m):",
        width=210,
        border_radius=6,
        value=str(orden.tela_ancho) if editando and orden.tela_ancho is not None else "",
    )
    tela_largo_input = ft.TextField(
        label="Largo de tela (m):",
        width=210,
        border_radius=6,
        value=str(orden.tela_largo) if editando and orden.tela_largo is not None else "",
    )
    patron_largo_input = ft.TextField(
        label="Largo del patrón (m):",
        width=210,
        border_radius=6,
        value=str(orden.patron_largo) if editando and orden.patron_largo is not None else "",
    )
    patron_ancho_input = ft.TextField(
        label="Ancho del patrón (m):",
        width=210,
        border_radius=6,
        value=str(orden.patron_ancho) if editando and orden.patron_ancho is not None else "",
    )
    tela_total_input = ft.TextField(
        label="Tela total utilizada (m²):",
        width=210,
        border_radius=6,
        value=str(orden.tela_total_utilizada) if editando and orden.tela_total_utilizada is not None else "",
    )
    retazo_input = ft.TextField(
        label="Retazo sobrante (m²):",
        width=210,
        border_radius=6,
        value=str(orden.retazo_sobrante) if editando and orden.retazo_sobrante is not None else "",
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def calcular_tela(e):
        """Calcula tela total utilizada y retazo sobrante a partir del patrón, la cantidad y la tela disponible."""
        try:
            cantidad = float(cantidad_input.value or 0)
            p_largo = float(patron_largo_input.value or 0)
            p_ancho = float(patron_ancho_input.value or 0)
            t_ancho = float(tela_ancho_input.value or 0)
            t_largo = float(tela_largo_input.value or 0)
        except ValueError:
            mensaje.value = "Para calcular, llena cantidad, patrón y tela con números válidos"
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        total_utilizada = round(p_largo * p_ancho * cantidad, 2)
        tela_disponible = round(t_ancho * t_largo, 2)
        sobrante = round(tela_disponible - total_utilizada, 2)
        sobrante_final = max(sobrante, 0)

        tela_total_input.value = str(total_utilizada)
        retazo_input.value = str(sobrante_final)

        if sobrante < 0:
            faltante = abs(sobrante)
            mensaje.value = (
                f"Se necesitan {total_utilizada} m² de tela para {int(cantidad)} pieza(s), "
                f"pero solo tienes {tela_disponible} m² disponibles "
                f"(faltan {faltante} m²)."
            )
            mensaje.color = ft.Colors.RED
        else:
            mensaje.value = (
                f"Con {tela_disponible} m² de tela disponible, esta orden usa "
                f"{total_utilizada} m² para {int(cantidad)} pieza(s) y sobran {sobrante_final} m²."
            )
            mensaje.color = ft.Colors.GREEN

        if page:
            page.update()

    seccion_tela = ft.Container(
        padding=15,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Tela y patrón (opcional)", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
                        ft.TextButton(
                            "Calcular tela usada y sobrante",
                            icon=ft.Icons.CALCULATE,
                            on_click=calcular_tela,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(controls=[tela_tipo_input, tela_ancho_input, tela_largo_input], wrap=True, spacing=10),
                ft.Row(controls=[patron_largo_input, patron_ancho_input], wrap=True, spacing=10),
                ft.Row(controls=[tela_total_input, retazo_input], wrap=True, spacing=10),
            ],
            spacing=10,
        ),
    )

    def guardar_orden(e):
        p_page = page or e.page

        if not pedido_dropdown.value or not producto_dropdown.value or not encargado_dropdown.value or not cantidad_input.value:
            mensaje.value = "Pedido, producto, encargado y cantidad son obligatorios"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            cantidad_num = int(cantidad_input.value)
        except ValueError:
            mensaje.value = "La cantidad debe ser un número entero"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            fecha_inicio_val = _parsear_fecha(fecha_inicio_input.value)
            fecha_entrega_val = _parsear_fecha(fecha_entrega_input.value) if fecha_entrega_input.value.strip() else None
        except ValueError as error_fecha:
            mensaje.value = str(error_fecha)
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        def a_flotante(texto):
            texto = (texto or "").strip()
            return float(texto) if texto else None

        try:
            dao = OrdenProduccionDAO()

            datos_comunes = dict(
                pedido_id=int(pedido_dropdown.value),
                producto_id=int(producto_dropdown.value),
                encargado_produccion_id=int(encargado_dropdown.value),
                produccion_cantidad=cantidad_num,
                produccion_estado=estado_dropdown.value,
                fecha_inicio=fecha_inicio_val,
                fecha_entrega=fecha_entrega_val,
                tela_tipo=tela_tipo_input.value or None,
                tela_ancho=a_flotante(tela_ancho_input.value),
                tela_largo=a_flotante(tela_largo_input.value),
                patron_largo=a_flotante(patron_largo_input.value),
                patron_ancho=a_flotante(patron_ancho_input.value),
                retazo_sobrante=a_flotante(retazo_input.value),
                tela_total_utilizada=a_flotante(tela_total_input.value),
            )

            if editando:
                orden_actualizada = OrdenProduccion(produccion_id=orden.produccion_id, **datos_comunes)
                dao.actualizar(orden_actualizada)
                mensaje.value = "Orden de producción actualizada"
                mensaje.color = ft.Colors.GREEN
                if p_page:
                    p_page.update()
                regresar()
                return

            nuevo_id = dao.obtener_ultimo_id() + 1
            nueva_orden = OrdenProduccion(produccion_id=nuevo_id, **datos_comunes)
            dao.insertar(nueva_orden)

            mensaje.value = "Orden de producción registrada"
            mensaje.color = ft.Colors.GREEN
            pedido_dropdown.value = None
            producto_dropdown.value = None
            encargado_dropdown.value = None
            cantidad_input.value = ""
            fecha_entrega_input.value = ""
            tela_tipo_input.value = ""
            tela_ancho_input.value = ""
            tela_largo_input.value = ""
            patron_largo_input.value = ""
            patron_ancho_input.value = ""
            tela_total_input.value = ""
            retazo_input.value = ""

        except Exception as error:
            mensaje.value = f"Error al guardar la orden: {error}"
            mensaje.color = ft.Colors.RED

        if p_page:
            p_page.update()

    encabezado = ft.Container(
        bgcolor=ft.Colors.LIGHT_BLUE_500,
        padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Editar orden de producción" if editando else "Nueva orden de producción",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: regresar(),
                ),
            ],
        ),
    )

    columna_izquierda = ft.Column(
        controls=[pedido_dropdown, producto_dropdown, encargado_dropdown],
        spacing=15,
    )
    columna_derecha = ft.Column(
        controls=[cantidad_input, estado_dropdown, fecha_inicio_input, fecha_entrega_input],
        spacing=15,
    )

    cuerpo = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Modifica los datos de la orden" if editando else "Captura los datos de la nueva orden",
                    size=14,
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Row(
                    controls=[columna_izquierda, columna_derecha],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                seccion_tela,
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
        height=420,
    )

    pie = ft.Container(
        padding=ft.Padding.only(left=30, right=30, bottom=20, top=5),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton("Cancelar", icon=ft.Icons.CLOSE, on_click=lambda e: regresar()),
                ft.ElevatedButton(
                    "Guardar cambios" if editando else "Registrar orden",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.LIGHT_BLUE_500,
                    color=ft.Colors.WHITE,
                    on_click=guardar_orden,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Container(
        width=760,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26, offset=ft.Offset(0, 4)),
        content=ft.Column(controls=[encabezado, cuerpo, pie], spacing=0),
    )