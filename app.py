# app.py
from dao.usuario_dao import UsuarioDAO #Carpeta/archivo/clase
from models.usuario import Usuario
from dao.cliente_dao import ClienteDAO

from dao.entrada_material_dao import EntradaMaterialDAO #Carpeta/archivo/clase



def ver_usuarios():
    try:
        usuario_dao = UsuarioDAO() #tiene todo de Usuario Dao

        usuarios = usuario_dao.obtener_todos()

        print("=== Usuarios en el Sistema ===")

    #si es que no hay usuarios
        if len(usuarios) == 0:
            print("No hay usuarios registrados")
        else:
            for usuario in usuarios:
                print("-------------------------------------------")

                print(
                    f"ID:{usuario.usuario_id},Nombre:{usuario.usuario_nombre},"
                    f"Apellido Paterno:{usuario.usuario_apellidop},Apellido Materno:{usuario.usuario_apellidom},"
                    f"Teléfono:{usuario.usuario_telefono},Correo:{usuario.usuario_correo},"
                    f"Password:{usuario.usuario_password},Rol ID:{usuario.rol_id}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    ver_usuarios()



def ver_clientes():
    try:
        cliente_dao = ClienteDAO()#tiene todo de Cliente Dao

        clientes = cliente_dao.obtener_todos()

        print("=== Clientes en el Sistema ===")

    #si es que no hay clientes
        if len(clientes) == 0:
            print("No hay clientes registrados")
        else:
            for cliente in clientes:
                print("-------------------------------------------")

                print(
                    f"ID:{cliente.cliente_id}, Nombre:{cliente.cliente_nombre},"
                    f" Teléfono:{cliente.cliente_telefono}, Correo:{cliente.cliente_correo},"
                    f" Calle:{cliente.cliente_calle}, Num:{cliente.cliente_numero},"
                    f" Municipio:{cliente.cliente_municipio}, Estado:{cliente.cliente_estado},"
                    f" CP:{cliente.cliente_codigopostal}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    ver_clientes()


def ver_entradas_materiales():
    try:
        entrada_dao = EntradaMaterialDAO() #tiene todo de EntradaMaterialDAO

        entradas = entrada_dao.obtener_todos()

        print("=== Entradas de Materiales en el Sistema ===")

        #si es que no hay entradas
        if len(entradas) == 0:
            print("No hay entradas de materiales registradas")
        else:
            for entrada in entradas:
                print("-------------------------------------------")
                print(
                    f"ID Entrada:{entrada.entrada_id}, ID Material:{entrada.material_id},"
                    f" ID Usuario:{entrada.usuario_id}, Fecha:{entrada.entrada_fecha},"
                    f" Cantidad:{entrada.entrada_cantidad}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    ver_entradas_materiales()


# app.py
from dao.material_dao import MaterialDAO
from models.material import Material

def ver_materiales():
    try:
        material_dao = MaterialDAO()
        materiales = material_dao.obtener_todos()

        print("=== Materiales en Inventario ===")

        if len(materiales) == 0:
            print("No hay materiales registrados")
        else:
            for mat in materiales:
                print("-------------------------------------------")
                print(
                    f"ID:{mat.material_id}, Nombre:{mat.material_nombre},"
                    f" Tipo:{mat.material_tipo}, Color:{mat.material_color},"
                    f" Cantidad:{mat.material_cantidad} {mat.material_unidad},"
                    f" Marca:{mat.material_marca}, Precio:${mat.material_precio}"
                )
                print("-------------------------------------------")
        print("\n Conexión exitosa ala base de datos")
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    ver_materiales()