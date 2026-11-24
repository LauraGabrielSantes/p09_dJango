from channels.generic.websocket import AsyncJsonWebsocketConsumer
import jwt
from pathlib import Path
from urllib.parse import parse_qs

class NotificacionesConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.grupo = "notificaciones_productos"
        self.autenticado = False

        # Obtener el token de la URL
        parametros = parse_qs(
            self.scope["query_string"].decode()
        )

        token = parametros.get("token", [None])[0]

        if not token:
            await self.close(code=4401)
            return

        # Leer la clave pública
        ruta_clave = (
            Path(__file__).resolve().parent.parent
            / "keys" / "public.pem"
        )

        try:
            with open(ruta_clave, "r") as archivo:
                clave_publica = archivo.read()

            # Validar el JWT firmado con RS256
            datos = jwt.decode(
                token,
                clave_publica,
                algorithms=["RS256"],
                options={"require": ["exp", "token_type", "user_id"]}
            )

            # Solo permitimos access tokens
            if datos.get("token_type") != "access":
                await self.close(code=4401)
                return

            self.autenticado = True

        except (jwt.InvalidTokenError, OSError):
            await self.close(code=4401)
            return

        # Agregar al grupo solo después de autenticar
        await self.channel_layer.group_add(
            self.grupo,
            self.channel_name
        )

        await self.accept()

        print("Cliente autenticado y conectado", flush=True)

    async def disconnect(self, close_code):
        if getattr(self, "autenticado", False):
            await self.channel_layer.group_discard(
                self.grupo,
                self.channel_name
            )

        print("Cliente desconectado", flush=True)

    async def enviar_notificacion(self, event):
        # Enviamos el mensaje recibido al cliente WebSocket
        await self.send_json(event["mensaje"])