import flet as ft
from database.conexion import Conexion
from models.producto import Producto
from dao.producto_dao import ProductoDAO
from ui.notificaciones import agregar_notificacion
from ui.componentes import mostrar_notificacion


def _obtener_categorias():
    """Trae (categoria_id, categoria_nombre) directo de la tabla categorias real."""
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT categoria_id, categoria_nombre FROM categorias ORDER BY categoria_nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def _crear_control_stock(valor_inicial, page):
    """
    Control de Stock incrementable: botones -/+ alrededor de un campo numérico.
    Devuelve (control_visual, campo_de_texto) -- usa campo_de_texto.value para leer/escribir el número.
    """
    campo_valor = ft.TextField(
        value=str(valor_inicial or "0"),
        width=70,
        text_align=ft.TextAlign.CENTER,
        border_radius=6,
    )

    def _leer_valor():
        try:
            return int(campo_valor.value)
        except (TypeError, ValueError):
            return 0

    def decrementar(e):
        nuevo = max(0, _leer_valor() - 1) 
        campo_valor.value = str(nuevo)
        if page:
            page.update()

    def incrementar(e):
        campo_valor.value = str(_leer_valor() + 1)
        if page:
            page.update()

    control_visual = ft.Column(
        controls=[
            ft.Text("Stock:", size=12, color=ft.Colors.BLUE_GREY_700),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                        icon_size=22,
                        tooltip="Quitar uno",
                        on_click=decrementar,
                    ),
                    campo_valor,
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                        icon_size=22,
                        tooltip="Agregar uno",
                        on_click=incrementar,
                    ),
                ],
                spacing=5,
            ),
        ],
        spacing=2,
        width=320,
    )

    return control_visual, campo_valor


def producto_form(regresar, producto=None, page=None):
    editando = producto is not None

    val_nombre = getattr(producto, "producto_nombre", "") if editando else ""
    val_precio = str(getattr(producto, "producto_precio", "")) if editando else ""
    val_stock = str(getattr(producto, "producto_stock", "")) if editando else "0"
    val_unidad = getattr(producto, "producto_unidad_medida", "") if editando else ""
    val_color = getattr(producto, "producto_color", "") if editando else ""
    val_categoria_nombre = getattr(producto, "producto_categoria", "") if editando else ""
    val_desc = getattr(producto, "producto_descripcion", "") if editando else ""

    categorias = _obtener_categorias()
    id_a_nombre = {str(cid): nombre for cid, nombre in categorias}
   
    nombre_a_id = {nombre: str(cid) for cid, nombre in categorias}
    val_cat_id = nombre_a_id.get(val_categoria_nombre) if editando else None

    nombre_input = ft.TextField(
        label="Nombre del producto:",
        hint_text="Ingresa el nombre del producto",
        width=320,
        border_radius=6,
        value=val_nombre,
    )

    precio_input = ft.TextField(
        label="Precio:",
        width=320,
        border_radius=6,
        prefix=ft.Text("$"),
        value=val_precio,
    )

    stock_control, stock_input = _crear_control_stock(val_stock, page)

    UNIDADES_DISPONIBLES = [
        "Pieza",
        "Par",
        "Metro",
        "Kilogramo",
        "Gramo",
        "Litro",
        "Mililitro",
        "Caja",
        "Paquete",
    ]

    if val_unidad and val_unidad not in UNIDADES_DISPONIBLES:
        UNIDADES_DISPONIBLES = [val_unidad] + UNIDADES_DISPONIBLES

    unidad_input = ft.Dropdown(
        label="Unidad de medida:",
        width=320,
        value=val_unidad or None,
        options=[
            ft.dropdown.Option(key=u, text=u) for u in UNIDADES_DISPONIBLES
        ],
    )

    color_input = ft.TextField(
        label="Color:",
        hint_text="Ingresa el color",
        width=320,
        border_radius=6,
        value=val_color,
    )

    categoria_dropdown = ft.Dropdown(
        label="Categoría:",
        width=320,
        value=val_cat_id,
        options=[
            ft.dropdown.Option(key=str(cid), text=nombre)
            for cid, nombre in categorias
        ],
    )

    descripcion_input = ft.TextField(
        label="Descripción:",
        hint_text="Añade una descripcción del producto",
        width=670,
        multiline=True,
        min_lines=2,
        max_lines=3,
        border_radius=6,
        value=val_desc,
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def guardar_producto(e):
        p_page = page or e.page

        nombre = (nombre_input.value or "").strip()
        precio = (precio_input.value or "").strip()
        stock = (stock_input.value or "").strip()
        unidad = (unidad_input.value or "").strip()
        color = (color_input.value or "").strip()
        categoria_id_seleccionada = categoria_dropdown.value
        descripcion = (descripcion_input.value or "").strip()

        if not nombre or not precio or not stock or not unidad or not color or not categoria_id_seleccionada:
            mensaje.value = "Todos los campos son obligatorios (excepto descripción)"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        try:
            precio_num = float(precio)
            stock_num = int(stock)
        except ValueError:
            mensaje.value = "Precio debe ser numérico y Stock debe ser un número entero"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if precio_num <= 0:
            mensaje.value = "El precio debe ser mayor a 0"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        if stock_num < 0:
            mensaje.value = "El stock no puede ser negativo"
            mensaje.color = ft.Colors.RED
            if p_page:
                p_page.update()
            return

        nombre_categoria = id_a_nombre.get(categoria_id_seleccionada, "")

        try:
            dao = ProductoDAO()

            if editando:
                producto_actualizado = Producto(
                    producto_id=producto.producto_id,
                    producto_nombre=nombre,
                    producto_categoria=nombre_categoria,
                    producto_precio=precio_num,
                    producto_stock=stock_num,
                    producto_descripcion=descripcion,
                    producto_unidad_medida=unidad,
                    producto_color=color,
                )
                dao.actualizar(producto_actualizado)

                texto = f"Producto '{nombre}' actualizado"
                agregar_notificacion(texto)
                mostrar_notificacion(p_page, "Producto actualizado", texto, "exito")

                mensaje.value = f"Producto '{nombre}' actualizado"
                mensaje.color = ft.Colors.GREEN
                if p_page:
                    p_page.update()
                regresar()
                return

            ultimo_id = dao.obtener_ultimo_id()
            nuevo_id = (ultimo_id or 0) + 1
            nuevo_producto = Producto(
                producto_id=nuevo_id,
                producto_nombre=nombre,
                producto_categoria=nombre_categoria,
                producto_precio=precio_num,
                producto_stock=stock_num,
                producto_descripcion=descripcion,
                producto_unidad_medida=unidad,
                producto_color=color,
            )
            dao.insertar(nuevo_producto)

            texto = f"Producto '{nombre}' registrado (stock: {stock_num})"
            agregar_notificacion(texto)
            mostrar_notificacion(p_page, "Nuevo producto", texto, "exito")

            mensaje.value = f"Producto '{nombre}' ha sido registrado"
            mensaje.color = ft.Colors.GREEN
            nombre_input.value = ""
            precio_input.value = ""
            stock_input.value = "0"
            unidad_input.value = None
            color_input.value = ""
            categoria_dropdown.value = None
            descripcion_input.value = ""

        except Exception as error:
            mensaje.value = f"Error al guardar el producto: {error}"
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
                    "Editar producto" if editando else "Registrar nuevo producto",
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
        controls=[
            nombre_input,
            unidad_input,
            categoria_dropdown,
        ],
        spacing=15,
    )

    columna_derecha = ft.Column(
        controls=[
            precio_input,
            stock_control,
            color_input,
        ],
        spacing=15,
    )

    cuerpo = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Modifica los datos del producto" if editando else "Captura los datos del nuevo producto",
                    size=14,
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Row(
                    controls=[columna_izquierda, columna_derecha],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                descripcion_input,
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    pie = ft.Container(
        padding=ft.Padding.only(left=30, right=30, bottom=20, top=5),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.OutlinedButton(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    on_click=lambda e: regresar(),
                ),
                ft.ElevatedButton(
                    "Guardar cambios" if editando else "Registrar producto",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.LIGHT_BLUE_500,
                    color=ft.Colors.WHITE,
                    on_click=guardar_producto,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Container(
        width=720,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            controls=[
                encabezado,
                cuerpo,
                pie,
            ],
            spacing=0,
        ),
    )