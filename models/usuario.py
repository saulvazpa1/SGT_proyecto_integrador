class Usuario:
    def __init__(self, usuario_id, usuario_nombre, usuario_apellidop, usuario_apellidom, usuario_telefono, usuario_correo, usuario_password, rol_id):
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.usuario_apellidop = usuario_apellidop
        self.usuario_apellidom = usuario_apellidom
        self.usuario_telefono = usuario_telefono
        self.usuario_correo = usuario_correo
        self.usuario_password = usuario_password
        self.rol_id = rol_id

    def mostrar_info_completa(self):
        return (
            f"ID Usuario: {self.usuario_id}"
            f"Nombre: {self.usuario_nombre}"
            f"Apellido Paterno: {self.usuario_apellidop}"
            f"Apellido Materno: {self.usuario_apellidom}"
            f"Teléfono: {self.usuario_telefono}"
            f"Correo: {self.usuario_correo}"
            f"Password: {self.usuario_password}"
            f"ID Rol: {self.rol_id}"
        )