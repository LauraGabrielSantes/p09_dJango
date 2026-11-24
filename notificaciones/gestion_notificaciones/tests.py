import json
import os

from django.test import TestCase


class NotificarTest(TestCase):
    def setUp(self):
        os.environ["NOTIFICACIONES_TOKEN"] = "token-interno-lab"

    def test_sin_token_responde_403(self):
        response = self.client.post(
            "/notificar",
            data=json.dumps({"evento": "producto_creado", "datos": {}}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_evento_valido_responde_200(self):
        response = self.client.post(
            "/notificar",
            data=json.dumps({"evento": "producto_creado", "datos": {"name": "Lapiz"}}),
            content_type="application/json",
            HTTP_X_INTERNAL_TOKEN="token-interno-lab",
        )
        self.assertEqual(response.status_code, 200)
