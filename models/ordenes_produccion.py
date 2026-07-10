class OrdenProduccion:
    def __init__(self, produccion_id, pedido_id, producto_id, encargado_produccion_id, produccion_cantidad, produccion_estado, fecha_inicio, fecha_entrega, tela_tipo, tela_ancho, tela_largo, patron_largo, patron_ancho, retazo_sobrante, tela_total_utilizada):
        self.produccion_id = produccion_id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.encargado_produccion_id = encargado_produccion_id
        self.produccion_cantidad = produccion_cantidad
        self.produccion_estado = produccion_estado
        self.fecha_inicio = fecha_inicio
        self.fecha_entrega = fecha_entrega
        self.tela_tipo = tela_tipo
        self.tela_ancho = tela_ancho
        self.tela_largo = tela_largo
        self.patron_largo = patron_largo
        self.patron_ancho = patron_ancho
        self.retazo_sobrante = retazo_sobrante
        self.tela_total_utilizada = tela_total_utilizada

    def mostrar_info_completa(self):
        return (
            f"ID Producción: {self.produccion_id}"
            f"ID Pedido: {self.pedido_id}"
            f"ID Producto: {self.producto_id}"
            f"ID Encargado: {self.encargado_produccion_id}"
            f"Cantidad: {self.produccion_cantidad}"
            f"Estado: {self.produccion_estado}"
            f"Fecha Inicio: {self.fecha_inicio}"
            f"Fecha Entrega: {self.fecha_entrega}"
            f"Tipo Tela: {self.tela_tipo}"
            f"Ancho Tela: {self.tela_ancho}"
            f"Largo Tela: {self.tela_largo}"
            f"Largo Patrón: {self.patron_largo}"
            f"Ancho Patrón: {self.patron_ancho}"
            f"Retazo Sobrante: {self.retazo_sobrante}"
            f"Tela Total Utilizada: {self.tela_total_utilizada}"
        )