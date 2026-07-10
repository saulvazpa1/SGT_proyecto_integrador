class Rol:
    def __init__(self, rol_id, rol_nombre, rol_permisos):
        self.rol_id = rol_id
        self.rol_nombre = rol_nombre
        self.rol_permisos = rol_permisos

    def mostrar_info_completa(self):
        return (
            f"ID Rol: {self.rol_id}"
            f"Nombre: {self.rol_nombre}"
            f"Permisos: {self.rol_permisos}"
        )