from datetime import datetime
import flet as ft
from database.conexion import Conexion
from models.orden_produccion import OrdenProduccion
from dao.ordenes_produccion_dao import OrdenProduccionDAO
from ui.notificaciones import agregar_notificacion
from ui.componentes import mostrar_notificacion


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
    """(pedido_id, 'Pedido #N — Cliente', producto_id, cantidad_pedida)"""
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.pedido_id, c.cliente_nombre, p.producto_id, p.pedido_cantidad
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.cliente_id
        ORDER BY p.pedido_id DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [
        (pid, f"Pedido #{pid} — {nombre}", producto_id, cantidad)
        for pid, nombre, producto_id, cantidad in filas
    ]


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
    Usuarios con rol 'Encargado de Producción' si existe ese rol;
    si no encuentra ninguno con ese rol exacto, regresa todos los usuarios
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

    # Mapa rápido:
    mapa_pedidos = {str(pid): (producto_id, cantidad) for pid, _, producto_id, cantidad in pedidos}

    pedido_dropdown = ft.Dropdown(
        label="Pedido:",
        width=320,
        value=str(orden.pedido_id) if editando else None,
        options=[ft.dropdown.Option(key=str(pid), text=texto) for pid, texto, _, _ in pedidos],
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

    # Autocompletar producto y cantidad al elegir el pedido 
    def al_elegir_pedido(e):
        datos = mapa_pedidos.get(pedido_dropdown.value)
        if not datos:
            return
        producto_id_pedido, cantidad_pedida = datos

        if producto_id_pedido is not None:
            producto_dropdown.value = str(producto_id_pedido)

        if cantidad_pedida is not None:
            cantidad_input.value = str(cantidad_pedida)

        if page:
            page.update()

    pedido_dropdown.on_select = al_elegir_pedido

    #  Campos de fecha con botón de calendario 
    def _campo_fecha(label, valor_inicial, ancho=320):
        """TextField normal (se puede escribir a mano) + botón de calendario para elegir la fecha."""
        campo = ft.TextField(
            label=label,
            width=ancho - 55,
            border_radius=6,
            value=valor_inicial,
        )

        def abrir_calendario(e):
            def al_elegir_fecha(ev):
                campo.value = ev.control.value.strftime("%Y-%m-%d")
                page.update()

            selector = ft.DatePicker(
                value=datetime.now(),
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2035, 12, 31),
                on_change=al_elegir_fecha,
            )
            page.show_dialog(selector)

        boton_calendario = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            tooltip="Elegir del calendario",
            on_click=abrir_calendario,
        )

        return ft.Row(controls=[campo, boton_calendario], spacing=4, width=ancho), campo

    fila_fecha_inicio, fecha_inicio_input = _campo_fecha(
        "Fecha de inicio (AAAA-MM-DD):",
        orden.fecha_inicio.strftime("%Y-%m-%d") if editando and orden.fecha_inicio else datetime.now().strftime("%Y-%m-%d"),
    )

    fila_fecha_entrega, fecha_entrega_input = _campo_fecha(
        "Fecha de entrega (opcional):",
        orden.fecha_entrega.strftime("%Y-%m-%d") if editando and orden.fecha_entrega else "",
    )

    #  Sección de tela y patrón 
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
    margen_desperdicio_input = ft.TextField(
        label="Margen de desperdicio (%):",
        width=210,
        border_radius=6,
        value="10",
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def calcular_tela(e):
        try:
            cantidad = int(float(cantidad_input.value or 0))
            p_largo = float(patron_largo_input.value or 0)
            p_ancho = float(patron_ancho_input.value or 0)
            t_ancho = float(tela_ancho_input.value or 0)
            t_largo = float(tela_largo_input.value or 0)
            margen_pct = float(margen_desperdicio_input.value or 0)
        except ValueError:
            mensaje.value = "Para calcular, llena cantidad, patrón, tela y margen con números válidos"
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        if cantidad <= 0 or p_largo <= 0 or p_ancho <= 0 or t_ancho <= 0:
            mensaje.value = "Cantidad, patrón y ancho de tela deben ser mayores a 0"
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        piezas_por_fila = int(t_ancho // p_ancho)
        if piezas_por_fila < 1:
            mensaje.value = (
                f"El ancho de la tela ({t_ancho} m) es menor al ancho del patrón "
                f"({p_ancho} m) — no cabe ni una pieza así acomodada."
            )
            mensaje.color = ft.Colors.RED
            if page:
                page.update()
            return

        filas_necesarias = -(-cantidad // piezas_por_fila)
        largo_necesario_sin_margen = round(filas_necesarias * p_largo, 2)

        margen_factor = 1 + (margen_pct / 100)
        largo_necesario_con_margen = round(largo_necesario_sin_margen * margen_factor, 2)

        area_utilizada = round(t_ancho * largo_necesario_con_margen, 2)

        tela_disponible = round(t_ancho * t_largo, 2) if t_largo > 0 else None

        tela_total_input.value = str(area_utilizada)

        espacios_sobrantes_ultima_fila = (piezas_por_fila * filas_necesarias) - cantidad

        if tela_disponible is None:
            retazo_input.value = ""
            mensaje.value = (
                f"Caben {piezas_por_fila} pieza(s) por fila. Para {cantidad} pieza(s) se necesitan "
                f"{filas_necesarias} fila(s) ≈ {largo_necesario_con_margen} m de largo de tela "
                f"(incluye {margen_pct}% de margen). Captura el 'Largo de tela' disponible para "
                f"saber cuánto sobra."
            )
            mensaje.color = ft.Colors.GREEN
        else:
            sobrante = round(tela_disponible - area_utilizada, 2)
            retazo_input.value = str(max(sobrante, 0))

            if sobrante < 0:
                mensaje.value = (
                    f"Caben {piezas_por_fila} pieza(s) por fila. Para {cantidad} pieza(s) se necesitan "
                    f"{filas_necesarias} fila(s) ≈ {largo_necesario_con_margen} m de largo "
                    f"(con {margen_pct}% de margen) = {area_utilizada} m², pero solo tienes "
                    f"{tela_disponible} m² disponibles (faltan {abs(sobrante)} m²)."
                )
                mensaje.color = ft.Colors.RED
            else:
                mensaje.value = (
                    f"Caben {piezas_por_fila} pieza(s) por fila en {filas_necesarias} fila(s) "
                    f"(sobran {espacios_sobrantes_ultima_fila} espacio(s) en la última fila). "
                    f"Se usan {area_utilizada} m² de {tela_disponible} m² disponibles "
                    f"(incluye {margen_pct}% de margen) — sobran {max(sobrante, 0)} m²."
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
                ft.Row(controls=[patron_largo_input, patron_ancho_input, margen_desperdicio_input], wrap=True, spacing=10),
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

                texto_notificacion = f"Orden #{orden.produccion_id} actualizada"
                agregar_notificacion(texto_notificacion)

                regresar()

                if p_page:
                    mostrar_notificacion(p_page, "Orden de producción actualizada", texto_notificacion, "exito")

                return

            nuevo_id = dao.obtener_ultimo_id() + 1
            nueva_orden = OrdenProduccion(produccion_id=nuevo_id, **datos_comunes)
            dao.insertar(nueva_orden)

            nombre_producto = dict(productos).get(int(producto_dropdown.value), "un producto")
            texto_notificacion = f"Orden #{nuevo_id} registrada — {nombre_producto}"
            agregar_notificacion(texto_notificacion)

            regresar()

            if p_page:
                mostrar_notificacion(p_page, "Nueva orden de producción", texto_notificacion, "exito")

            return

        except Exception as error:
            mensaje.value = f"Error al guardar la orden: {error}"
            mensaje.color = ft.Colors.RED

        if p_page:
            p_page.update()

    encabezado = ft.Container(
        bgcolor=ft.Colors.LIGHT_BLUE_500,
        padding=ft.Padding(left=20, right=20, top=14, bottom=14),
        border_radius=ft.BorderRadius(top_left=10, top_right=10, bottom_left=0, bottom_right=0),
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
        controls=[cantidad_input, estado_dropdown, fila_fecha_inicio, fila_fecha_entrega],
        spacing=15,
    )

    cuerpo = ft.Container(
        padding=ft.Padding(left=30, right=30, top=20, bottom=20),
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
        ),
    )

    pie = ft.Container(
        padding=ft.Padding(left=30, right=30, top=10, bottom=20),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(top=ft.BorderSide(1, ft.Colors.BLUE_GREY_100)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE_GREY_700,
                        side=ft.BorderSide(1, ft.Colors.BLUE_GREY_300),
                    ),
                    on_click=lambda e: regresar(),
                ),
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

    alto_disponible = (page.height - 120) if (page and page.height) else 640
    alto_dialogo = max(420, min(alto_disponible, 680))

    cuerpo_con_scroll = ft.Container(
        content=ft.Column(controls=[cuerpo], scroll=ft.ScrollMode.AUTO, expand=True),
        expand=True,
    )

    return ft.Container(
        width=760,
        height=alto_dialogo,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26, offset=ft.Offset(0, 4)),
        content=ft.Column(
            controls=[encabezado, cuerpo_con_scroll, pie],
            spacing=0,
            expand=True,
        ),
    )