class Material:
    # Constructor con los atributos de tu documento de requerimientos
    def __init__(self, material_id, material_nombre, material_tipo, material_color, material_cantidad, material_unidad, material_marca, material_proveedor, material_precio):
        self.material_id = material_id
        self.material_nombre=material_nombre
        self.material_tipo = material_tipo
        self.material_color = material_color
        self.material_cantidad = material_cantidad
        self.material_unidad = material_unidad
        self.material_marca = material_marca
        self.material_proveedor = material_proveedor
        self.material_precio = material_precio
       

    def mostrar_info_completa(self):
        return (
            f"ID Material: {self.material_id}"
            f"Material: {self.material_nombre}"
            f"Tipo: {self.material_tipo}"
            f"Color: {self.material_color}"
            f"Cantidad: {self.material_cantidad}"
            f"Unidad: {self.material_unidad}"
            f"Marca: {self.material_marca}"
            f"Proveedor: {self.material_proveedor}"
            f"Precio: {self.material_precio}"
            
        )