class Pedido:
    def __init__(self, pedido_id, cliente_id, vendedor_id, producto_id, pedido_cantidad, pedido_total, pedido_estado, pedido_fecha):
        self.pedido_id = pedido_id
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        self.producto_id = producto_id
        self.pedido_cantidad = pedido_cantidad
        self.pedido_total = pedido_total
        self.pedido_estado = pedido_estado
        self.pedido_fecha = pedido_fecha

    def mostrar_info_completa(self):
        return (
            f"ID Pedido: {self.pedido_id}"
            f"ID Cliente: {self.cliente_id}"
            f"ID Vendedor: {self.vendedor_id}"
            f"ID Producto: {self.producto_id}"
            f"Cantidad: {self.pedido_cantidad}"
            f"Total: {self.pedido_total}"
            f"Estado: {self.pedido_estado}"
            f"Fecha: {self.pedido_fecha}"
        )