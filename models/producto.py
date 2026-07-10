class Producto:
    def __init__(self, producto_id, producto_nombre, producto_categoria, producto_precio, producto_stock, producto_descripcion, producto_unidad_medida, producto_color):
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.producto_categoria = producto_categoria
        self.producto_precio = producto_precio
        self.producto_stock = producto_stock
        self.producto_descripcion = producto_descripcion
        self.producto_unidad_medida = producto_unidad_medida
        self.producto_color = producto_color

    def mostrar_info_completa(self):
        return (
            f"ID Producto: {self.producto_id}"
            f"Nombre: {self.producto_nombre}"
            f"Categoría: {self.producto_categoria}"
            f"Precio: {self.producto_precio}"
            f"Stock: {self.producto_stock}"
            f"Descripción: {self.producto_descripcion}"
            f"Unidad Medida: {self.producto_unidad_medida}"
            f"Color: {self.producto_color}"
        )