# gestion_productos/tests.py

import logging
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class TestEndpointsProductos(TestCase):
    """Pruebas sobre /api/products/ — autenticación y operaciones CRUD."""

    def setUp(self):
        self.client = APIClient()
        self.url_login = "/api/auth/token/"
        self.url_products = "/api/productos/products/"

        self.admin = User.objects.create_superuser(
            username="admin_prod",
            password="AdminProd123",
            email="adminprod@test.com",
        )

    def _token_admin(self):
        self.client.force_authenticate(user=self.admin)

    # ── Protección ─────────────────────────────────────────────────────────────

    def test_listar_productos_sin_token_devuelve_401(self):
        self.client.credentials()
        response = self.client.get(self.url_products)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_productos_con_token_devuelve_200(self):
        self._token_admin()
        response = self.client.get(self.url_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ── Creación ───────────────────────────────────────────────────────────────

    def test_crear_producto_devuelve_201(self):
        self._token_admin()
        response = self.client.post(
            self.url_products,
            {
                "type": "BIEN",
                "name": "Producto test",
                "price": "99.99",
                "status": True,
                "description": "Descripción del producto de prueba",
                "product_key": "TEST0001",
                "image_link": "http://example.com/img.png",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_producto_sin_token_devuelve_401(self):
        self.client.credentials()
        response = self.client.post(
            self.url_products,
            {
                "name": "Sin token",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── Auditoría ──────────────────────────────────────────────────────────────

    def test_crear_producto_registra_en_log_auditoria(self):
        """Crear un producto debe escribir CREAR_PRODUCTO en el log de auditoría."""
        with self.assertLogs("auditoria", level="INFO") as cm:
            self._token_admin()
            self.client.post(
                self.url_products,
                {
                    "type": "BIEN",
                    "name": "Producto auditado",
                    "price": "50.00",
                    "status": True,
                    "description": "Para test de auditoría",
                    "product_key": "AUD00001",
                    "image_link": "http://example.com/img.png",
                },
                format="json",
            )

        mensajes = "\n".join(cm.output)
        self.assertIn("CREAR_PRODUCTO", mensajes)

    def test_eliminar_producto_registra_en_log_auditoria(self):
        """Eliminar un producto debe escribir ELIMINAR_PRODUCTO en auditoría."""
        # Primero crear un producto
        self._token_admin()
        crear = self.client.post(
            self.url_products,
            {
                "type": "BIEN",
                "name": "Para eliminar",
                "price": "10.00",
                "status": True,
                "description": "Se eliminará en el test",
                "product_key": "DEL00001",
                "image_link": "http://example.com/img.png",
            },
            format="json",
        )

        producto_id = crear.data["id"]

        # Luego eliminarlo y verificar el log
        with self.assertLogs("auditoria", level="INFO") as cm:
            self.client.delete(f"{self.url_products}{producto_id}/")

        mensajes = "\n".join(cm.output)
        self.assertIn("ELIMINAR_PRODUCTO", mensajes)
