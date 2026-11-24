import graphene 
import requests

PRODUCTOS_URL = "http://servicio-productos:8000/api/productos/products/"
USUARIOS_URL  = "http://servicio-usuarios:8000/api/usuarios/users/"

class ProductoType(graphene.ObjectType):
    id = graphene.UUID()
    type = graphene.String()
    name = graphene.String()
    price = graphene.Decimal()
    status = graphene.Boolean()
    description = graphene.String()
    product_key = graphene.String()
    image_link = graphene.String()

class UsuarioType(graphene.ObjectType):
    id = graphene.UUID()
    username = graphene.String()
    date_of_birth = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene. String()

class CrearProducto(graphene.Mutation):
    class Arguments:
        type = graphene.String(required=True)
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        status = graphene.Boolean(required=True)
        description = graphene.String(required=True)
        product_key = graphene.String(required=True)
        image_link = graphene.String(required=True)

    producto = graphene.Field(ProductoType)
    def mutate(
        root,
        info,
        type,
        name,
        price,
        status,
        description,
        product_key,
        image_link
    ):
        authorization = info.context.headers.get("Authorization")
        headers={}
        if authorization:
            headers["Authorization"] = authorization

        datos = {
            "type": type,
            "name": name,
            "price": str(price),
            "status": status,
            "description": description,
            "product_key": product_key,
            "image_link": image_link,
        }

        try:
            response = requests.post(
                PRODUCTOS_URL,
                json=datos,
                headers=headers,
                timeout=5
            )

            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            raise

        return CrearProducto(
            producto=response.json()
        )

class CrearUsuario(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        date_of_birth = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    usuario = graphene.Field(UsuarioType)

    def mutate(root, info, username, password, date_of_birth, email, first_name, last_name):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        datos = {
            "username": username,
            "password": password,
            "date_of_birth": date_of_birth,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(
            USUARIOS_URL,
            json=datos,
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return CrearUsuario(usuario = response.json())

class ActualizarProducto(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        type = graphene.String()
        name = graphene.String()
        price = graphene.Decimal()
        status = graphene.Boolean()
        description = graphene.String()
        product_key = graphene.String()
        image_link = graphene.String()
    producto = graphene.Field(ProductoType)
    def mutate(
        root,
        info,
        id,
        type = None,
        name = None,
        price = None,
        status = None,
        description = None,
        product_key = None,
        image_link= None
    ):
        authorization = info.context.headers.get("Authorization")

        headers = {}

        if authorization:
            headers["Authorization"] = authorization

        datos = {}

        if type is not None:
            datos["type"] = type

        if name is not None:
            datos["name"] = name

        if price is not None:
            datos["price"] = str(price)

        if status is not None:
            datos["status"] = status

        if description is not None:
            datos["description"] = description

        if product_key is not None:
            datos["product_key"] = product_key

        if image_link is not None:
            datos["image_link"] = image_link

        response = requests.patch(
            f"{PRODUCTOS_URL}{id}/",
            json=datos,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        return ActualizarProducto(
            producto=response.json()
        )
class ActualizarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        username = graphene.String()
        password = graphene.String()
        date_of_birth = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
    usuario = graphene.Field(UsuarioType)
    def mutate(root, info, id, **kwargs):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        datos = {
           campo: valor
           for campo, valor in kwargs.items()
           if valor is not None
        }
        response = requests.patch(
            f"{USUARIOS_URL}{id}/",
            json=datos,
            headers= headers,
            timeout=5
        )
        response.raise_for_status()
        return ActualizarUsuario(usuario=response.json())
            
class EliminarProducto(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    mensaje = graphene.String()

    def mutate(root, info, id):
        authorization = info.context.headers.get("Authorization")

        headers = {}

        if authorization:
            headers["Authorization"] = authorization

        response = requests.delete(
            f"{PRODUCTOS_URL}{id}/",
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        return EliminarProducto(
            mensaje=response.json()["mensaje"]
        )
class EliminarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
    mensaje = graphene.String()
    def mutate(root, info, id):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        response = requests.delete(
            f"{USUARIOS_URL}{id}/",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return EliminarUsuario(mensaje= response.json()["mensaje"])

class panelGeneralType(graphene.ObjectType):
    productos = graphene.List(ProductoType)
    usuarios = graphene.List(UsuarioType)

class Mutation(graphene.ObjectType):
    crear_producto = CrearProducto.Field()
    actualizar_producto = ActualizarProducto.Field()
    eliminar_producto = EliminarProducto.Field()
    crear_usuario = CrearUsuario.Field()
    actualizar_usuario = ActualizarUsuario.Field()
    eliminar_usuario = EliminarUsuario.Field()



class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType)
    producto = graphene.Field(ProductoType, id=graphene.UUID(required=True))
    usuarios = graphene.List(UsuarioType)
    usuario = graphene.Field(UsuarioType, id=graphene.UUID(required=True))
    panel_general = graphene.Field(panelGeneralType)

    def resolve_productos(root, info):
        authorization = info.context.headers.get("Authorization", "")

        headers = {}

        if authorization:
            headers["Authorization"] = authorization

        response = requests.get(
            PRODUCTOS_URL,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()
        return response.json()

    def resolve_producto(root, info, id):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        response = requests.get(
            f"{PRODUCTOS_URL}{id}/",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    
    def resolve_usuarios(root, info):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if  authorization:
            headers["Authorization"] = authorization
        response = requests.get(USUARIOS_URL, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    def resolve_usuario(root, info, id):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        response = requests.get(
            f"{USUARIOS_URL}{id}/",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    def resolve_panel_general(root, info):
        authorization = info.context.headers.get("Authorization", "")
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        response_usuarios = requests.get(
            USUARIOS_URL,
            headers=headers,
            timeout=5
        )
        response_productos = requests.get(
            PRODUCTOS_URL,
            headers=headers,
            timeout=5
        )
        response_usuarios.raise_for_status()
        response_productos.raise_for_status()
        return panelGeneralType(
            usuarios = response_usuarios.json(),
            productos = response_productos.json()
        )
schema = graphene.Schema(
    query=Query,
    mutation=Mutation
    )