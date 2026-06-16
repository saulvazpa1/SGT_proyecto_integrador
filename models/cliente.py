class Cliente:
    # Constructor con los atributos de tu documento de requerimientos
    def __init__(self, cliente_id, cliente_nombre, cliente_telefono, cliente_correo, cliente_calle, cliente_numero, cliente_municipio, cliente_estado, cliente_codigopostal):
        self.cliente_id = cliente_id
        self.cliente_nombre=cliente_nombre
        self.cliente_telefono = cliente_telefono
        self.cliente_correo = cliente_correo
        self.cliente_calle = cliente_calle
        self.cliente_numero = cliente_numero
        self.cliente_municipio = cliente_municipio
        self.cliente_estado = cliente_estado
        self.cliente_codigopostal = cliente_codigopostal
        

    def mostrar_info_completa(self):
        return (
            f"ID Cliente: {self.cliente_id}"
            f"Nombre Completo: {self.cliente_nombre} "
            f"Teléfono: {self.cliente_telefono}"
            f"Correo: {self.cliente_correo}"
            f"Calle: {self.cliente_calle}"
            f"Numero: {self.cliente_numero}"
            f"Municipio: {self.cliente_municipio}"
            f"Estado: {self.cliente_estado}"
            f"C.P: {self.cliente_codigopostal}"
            
            
        )