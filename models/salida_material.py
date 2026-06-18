class SalidaMaterial:
    def __init__(self, salida_id, material_id, produccion_id, usuario_id, salida_fecha, salida_cantidad):
        self.salida_id = salida_id
        self.material_id = material_id
        self.produccion_id = produccion_id
        self.usuario_id = usuario_id
        self.salida_fecha = salida_fecha
        self.salida_cantidad = salida_cantidad

    def mostrar_info_completa(self):
        return (
            f"ID Salida: {self.salida_id}"
            f"ID Material: {self.material_id}"
            f"ID Producción: {self.produccion_id}"
            f"ID Usuario: {self.usuario_id}"
            f"Fecha Salida: {self.salida_fecha}"
            f"Cantidad Salida: {self.salida_cantidad}"
        )