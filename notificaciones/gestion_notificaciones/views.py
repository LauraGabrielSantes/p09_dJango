import os
import json
import secrets

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@csrf_exempt
def notificar(request):

    # Solo permitimos peticiones POST
    if request.method != "POST":
        return JsonResponse(
            {"error": "Metodo no permitido"},
            status=405
        )

    # Obtenemos el token configurado en el entorno
    token_esperado = os.environ.get("NOTIFICACIONES_TOKEN")

    # Obtenemos el token enviado por el cliente
    token_recibido = request.headers.get("X-Internal-Token", "")

    # Rechazamos peticiones sin un token valido
    if not token_esperado or not secrets.compare_digest(
        token_recibido, token_esperado
    ):
        return JsonResponse(
            {"error": "Acceso no autorizado"},
            status=403
        )

    # Procesamos el JSON recibido
    try:
        mensaje = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "JSON invalido"},
            status=400
        )

    if (
        not isinstance(mensaje, dict)
        or "evento" not in mensaje
        or "datos" not in mensaje
    ):
        return JsonResponse(
            {"error": "Faltan los campos evento o datos"},
            status=400
        )

    # Enviamos el evento al grupo WebSocket
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "notificaciones_productos",
        {
            "type": "enviar_notificacion",
            "mensaje": mensaje
        }
    )

    return JsonResponse({
        "mensaje": "Notificacion enviada correctamente"
    })