import logging
import os

import requests

logger = logging.getLogger(__name__)


def enviar_notificacion(evento, datos):
    """
    Envia un evento del microservicio de Productos
    al microservicio de Notificaciones.
    """

    url = os.environ.get("NOTIFICACIONES_URL")
    token = os.environ.get("NOTIFICACIONES_TOKEN")

    if not url or not token:
        logger.error("Falta configurar el servicio de Notificaciones")
        return False

    mensaje = {
        "evento": evento,
        "datos": datos
    }

    try:
        respuesta = requests.post(
            url,
            json=mensaje,
            headers={
                "X-Internal-Token": token
            },
            timeout=3
        )

        respuesta.raise_for_status()
        return True

    except requests.RequestException as error:
        logger.error("Error al enviar notificacion: %s", error)
        return False