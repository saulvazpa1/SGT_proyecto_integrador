class TrabajoAsignado:
    def __init__(self, trabajo_id, trabajador_id, produccion_id, trabajo_nombre, trabajo_fecha, trabajo_estado):
        self.trabajo_id = trabajo_id
        self.trabajador_id = trabajador_id
        self.produccion_id = produccion_id
        self.trabajo_nombre = trabajo_nombre
        self.trabajo_fecha = trabajo_fecha
        self.trabajo_estado = trabajo_estado

    def mostrar_info_completa(self):
        return (
            f"ID Trabajo: {self.trabajo_id}"
            f"ID Trabajador: {self.trabajador_id}"
            f"ID Producción: {self.produccion_id}"
            f"Trabajo: {self.trabajo_nombre}"
            f"Fecha: {self.trabajo_fecha}"
            f"Estado: {self.trabajo_estado}"
        )