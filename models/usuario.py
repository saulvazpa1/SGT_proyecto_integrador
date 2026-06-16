class Usuario:
    # Constructor con los atributos de tu documento de requerimientos
    def __init__(self, id_usuario, nombre, apellido_p, apellido_m, telefono, correo, password, rol_id):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.telefono = telefono
        self.correo = correo
        self.password = password  # Almacena el hash encriptado (RNF_08)
        self.rol_id = rol_id

    def mostrar_info_completa(self):
        return (
            f"ID Usuario: {self.id_usuario}"
            f"Nombre Completo: {self.nombre} {self.apellido_p} {self.apellido_m if self.apellido_m else ''}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo}\n"
            f"ID Rol Asignado: {self.rol_id}\n"
            f"Password (Hash): {self.password}\n"
            
        )