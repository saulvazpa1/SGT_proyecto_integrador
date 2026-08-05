import re

NOMBRE_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")
CORREO_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
NOMBRE_PRODUCTO_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .,#-]+$")


def validar_nombre(texto, campo="Nombre", max_len=50, obligatorio=True):
    """Solo letras y espacios, hasta max_len caracteres."""
    texto = (texto or "").strip()

    if not texto:
        if obligatorio:
            return False, f"{campo} es obligatorio"
        return True, ""

    if len(texto) > max_len:
        return False, f"{campo} no puede tener más de {max_len} caracteres"

    if not NOMBRE_REGEX.match(texto):
        return False, f"{campo} solo puede contener letras"

    return True, ""


def validar_nombre_producto(texto, campo="Nombre del producto", max_len=50, obligatorio=True):
    """Letras, números y algunos símbolos comunes (., #, -), hasta max_len caracteres."""
    texto = (texto or "").strip()

    if not texto:
        if obligatorio:
            return False, f"{campo} es obligatorio"
        return True, ""

    if len(texto) > max_len:
        return False, f"{campo} no puede tener más de {max_len} caracteres"

    if not NOMBRE_PRODUCTO_REGEX.match(texto):
        return False, f"{campo} contiene caracteres no permitidos"

    return True, ""


def validar_correo(texto, obligatorio=True):
    """Formato tipo usuario@dominio.com (gmail, hotmail, etc.)."""
    texto = (texto or "").strip()

    if not texto:
        if obligatorio:
            return False, "El correo es obligatorio"
        return True, ""

    if not CORREO_REGEX.match(texto):
        return False, "El correo no tiene un formato válido (ej. usuario@gmail.com)"

    return True, ""


def validar_password(texto, min_len=8, obligatorio=True):
    """Mínimo min_len caracteres."""
    texto = texto or ""

    if not texto:
        if obligatorio:
            return False, "La contraseña es obligatoria"
        return True, ""

    if len(texto) < min_len:
        return False, f"La contraseña debe tener al menos {min_len} caracteres"

    return True, ""


def validar_telefono(texto, longitud=10, obligatorio=True):
    """Solo números, exactamente 'longitud' dígitos."""
    texto = (texto or "").strip()

    if not texto:
        if obligatorio:
            return False, "El teléfono es obligatorio"
        return True, ""

    if not texto.isdigit():
        return False, "El teléfono solo puede contener números"

    if len(texto) != longitud:
        return False, f"El teléfono debe tener exactamente {longitud} dígitos"

    return True, ""