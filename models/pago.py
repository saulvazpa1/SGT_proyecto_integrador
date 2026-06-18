class Pago:
    def __init__(self, pago_id, pedido_id, pago_monto, pago_fecha, pago_metodo):
        self.pago_id = pago_id
        self.pedido_id = pedido_id
        self.pago_monto = pago_monto
        self.pago_fecha = pago_fecha
        self.pago_metodo = pago_metodo

    def mostrar_info_completa(self):
        return (
            f"ID Pago: {self.pago_id}"
            f"ID Pedido: {self.pedido_id}"
            f"Monto: {self.pago_monto}"
            f"Fecha: {self.pago_fecha}"
            f"Método: {self.pago_metodo}"
        )