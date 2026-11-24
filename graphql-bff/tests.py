from django.test import SimpleTestCase
from unittest.mock import patch, Mock
from types import SimpleNamespace

from schema import schema


class GraphQLTests(SimpleTestCase):

    def setUp(self):
        self.contexto = SimpleNamespace(
            headers={"Authorization": "Bearer token_prueba"}
        )

    @patch("schema.requests.get")
    def test_panel_general(self, mock_get):

        respuesta_usuarios = Mock()
        respuesta_usuarios.json.return_value = [
            {
                "username": "usuario1",
                "email": "usuario1@example.com"
            }
        ]

        respuesta_productos = Mock()
        respuesta_productos.json.return_value = [
            {
                "name": "Monitor",
                "price": "3000.00"
            }
        ]

        mock_get.side_effect = [
            respuesta_usuarios,
            respuesta_productos
        ]

        consulta = """
        query {
            panelGeneral {
                usuarios {
                    username
                    email
                }
                productos {
                    name
                    price
                }
            }
        }
        """

        resultado = schema.execute(
            consulta,
            context_value=self.contexto
        )

        self.assertIsNone(resultado.errors)
        self.assertEqual(
            resultado.data["panelGeneral"]["productos"][0]["name"],
            "Monitor"
        )
        self.assertEqual(
            resultado.data["panelGeneral"]["usuarios"][0]["username"],
            "usuario1"
        )
        self.assertEqual(mock_get.call_count, 2)

    @patch("schema.requests.post")
    def test_crear_producto(self, mock_post):

        respuesta = Mock()
        respuesta.json.return_value = {
            "name": "Teclado",
            "price": "1200.00",
            "status": True
        }

        mock_post.return_value = respuesta

        consulta = """
        mutation {
            crearProducto(
                type: "Hardware"
                name: "Teclado"
                price: 1200
                status: true
                description: "Teclado mecanico"
                productKey: "TEC001"
                imageLink: "https://example.com/teclado.jpg"
            ) {
                producto {
                    name
                    price
                }
            }
        }
        """

        resultado = schema.execute(
            consulta,
            context_value=self.contexto
        )

        self.assertIsNone(resultado.errors)
        self.assertEqual(
            resultado.data["crearProducto"]["producto"]["name"],
            "Teclado"
        )

        mock_post.assert_called_once()

    @patch("schema.requests.patch")
    def test_actualizar_producto(self, mock_patch):

        respuesta = Mock()
        respuesta.json.return_value = {
            "name": "Monitor",
            "price": "3000.00"
        }

        mock_patch.return_value = respuesta

        consulta = """
        mutation {
            actualizarProducto(
                id: "e8d19307-a8b7-49c4-b1c3-e276e22c39bb"
                price: 3000
            ) {
                producto {
                    name
                    price
                }
            }
        }
        """

        resultado = schema.execute(
            consulta,
            context_value=self.contexto
        )

        self.assertIsNone(resultado.errors)
        self.assertEqual(
            str(resultado.data["actualizarProducto"]["producto"]["price"]),
            "3000.00"
        )

        mock_patch.assert_called_once()