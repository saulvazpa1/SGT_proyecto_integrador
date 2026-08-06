import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from dao.producto_dao import ProductoDAO
from dao.pedido_dao import PedidoDAO


def _carpeta_reportes():
    """Guarda los PDFs en Documentos\\Reportes SGIT, creando la carpeta si no existe."""
    carpeta = os.path.join(os.path.expanduser("~"), "Documents", "Reportes SGIT")
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def _fecha_legible(valor_fecha):
    """Recorta la fecha a 'AAAA-MM-DD HH:MM:SS', sin los microsegundos."""
    if hasattr(valor_fecha, "strftime"):
        return valor_fecha.strftime("%Y-%m-%d %H:%M:%S")
    return str(valor_fecha)[:19]


def _celda(texto, estilo_celda):
    """Envuelve el texto en un Paragraph para que se ajuste dentro del ancho de columna."""
    return Paragraph(str(texto), estilo_celda)


def _estilo_tabla():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2196F3")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])


def generar_reporte_inventario():
    productos = ProductoDAO().obtener_todos()

    ruta = os.path.join(_carpeta_reportes(), f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Reporte de Inventario de Productos", estilos["Title"]))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    total_productos = len(productos)
    try:
        valor_total = sum(float(p.producto_precio or 0) * int(p.producto_stock or 0) for p in productos)
    except Exception:
        valor_total = 0

    elementos.append(Paragraph(f"Total de productos: {total_productos}", estilos["Normal"]))
    elementos.append(Paragraph(f"Valor total del inventario: ${valor_total:,.2f}", estilos["Normal"]))
    elementos.append(Spacer(1, 16))

    datos = [["Nombre", "Categoría", "Precio", "Stock", "Color"]]
    for p in productos:
        try:
            precio_texto = f"${float(p.producto_precio):,.2f}"
        except (TypeError, ValueError):
            precio_texto = str(p.producto_precio)

        datos.append([
            str(p.producto_nombre),
            str(p.producto_categoria),
            precio_texto,
            str(p.producto_stock),
            str(p.producto_color),
        ])

    tabla = Table(datos, repeatRows=1)
    tabla.setStyle(_estilo_tabla())
    elementos.append(tabla)

    doc.build(elementos)
    return ruta


def generar_reporte_ventas():
    pedidos = PedidoDAO().obtener_todos()

    ruta = os.path.join(_carpeta_reportes(), f"ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    doc = SimpleDocTemplate(
        ruta,
        pagesize=landscape(letter),  
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=30,
    )
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Reporte de Ventas y Pedidos", estilos["Title"]))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    total_pedidos = len(pedidos)
    try:
        ingresos_totales = sum(float(p.pedido_total or 0) for p in pedidos)
    except Exception:
        ingresos_totales = 0

    elementos.append(Paragraph(f"Total de pedidos: {total_pedidos}", estilos["Normal"]))
    elementos.append(Paragraph(f"Ingresos totales: ${ingresos_totales:,.2f}", estilos["Normal"]))
    elementos.append(Spacer(1, 16))

    estilos = getSampleStyleSheet()
    estilo_celda = estilos["Normal"].clone("celda")
    estilo_celda.fontSize = 8
    estilo_celda.leading = 10

    datos = [["ID", "Cliente", "Vendedor", "Producto", "Cant.", "Total", "Estado", "Fecha"]]
    for p in pedidos:
        try:
            total_texto = f"${float(p.pedido_total):,.2f}"
        except (TypeError, ValueError):
            total_texto = str(p.pedido_total)

        datos.append([
            str(p.pedido_id),
            _celda(p.cliente_id, estilo_celda),
            _celda(p.vendedor_id, estilo_celda),
            _celda(p.producto_id, estilo_celda),
            str(p.pedido_cantidad),
            total_texto,
            str(p.pedido_estado),
            _fecha_legible(p.pedido_fecha),  
        ])

    
    anchos_columnas = [30, 130, 90, 130, 40, 70, 80, 110]

    tabla = Table(datos, repeatRows=1, colWidths=anchos_columnas)
    tabla.setStyle(_estilo_tabla())
    elementos.append(tabla)

    doc.build(elementos)
    return ruta