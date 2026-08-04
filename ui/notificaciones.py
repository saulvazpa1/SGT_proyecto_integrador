from dao.notificacion_dao import NotificacionDAO


def agregar_notificacion(mensaje):
    NotificacionDAO().insertar(mensaje)


def obtener_notificaciones():
    notifs = NotificacionDAO().obtener_recientes()
    return [
        {
            "id": n.notificacion_id,
            "mensaje": n.mensaje,
            "fecha": n.fecha_creacion.strftime("%Y-%m-%d %H:%M") if n.fecha_creacion else "",
            "leida": n.leida,
        }
        for n in notifs
    ]


def contar_no_leidas():
    return NotificacionDAO().contar_no_leidas()


def marcar_todas_leidas():
    NotificacionDAO().marcar_todas_leidas()


def eliminar_notificacion(notificacion_id):
    NotificacionDAO().eliminar(notificacion_id)


def eliminar_todas_las_notificaciones():
    NotificacionDAO().eliminar_todas()