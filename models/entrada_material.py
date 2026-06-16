class Entrada_material:
    # Constructor con los atributos de tu documento de requerimientos
    def __init__(self, entrada_id, material_id, usuario_id, entrada_fecha, entrada_cantidad):
        self.entrada_id = entrada_id
        self.material_id=material_id
        self.usuario_id = usuario_id
        self.entrada_fecha=entrada_fecha
        self.entrada_catidad = entrada_cantidad
        

    def mostrar_info_completa(self):
        return (
            f"ID entrada: {self.entrada_id}"
            f"ID Material: {self.material_id}\n"
            f"ID Usuario: {self.usuario_id}\n"
            f"Fecha de entrada: {self.entrada_fecha}\n"
            f"Cantidad: {self.entrada_catidad}\n"
            
        )