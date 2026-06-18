class EntradaMaterial:
    def __init__(self, entrada_id, material_id, usuario_id, entrada_fecha, entrada_cantidad):
        self.entrada_id = entrada_id
        self.material_id = material_id
        self.usuario_id = usuario_id
        self.entrada_fecha = entrada_fecha
        self.entrada_cantidad = entrada_cantidad

    def mostrar_info_completa(self):
        return (
            f"ID Entrada: {self.entrada_id}"
            f"ID Material: {self.material_id}"
            f"ID Usuario: {self.usuario_id}"
            f"Fecha Entrada: {self.entrada_fecha}"
            f"Cantidad Entrada: {self.entrada_cantidad}"
        )