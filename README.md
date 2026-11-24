# Práctica 9 — GraphQL y WebSockets

Continuación de la práctica 8. Agrega un BFF GraphQL y un servicio de notificaciones por WebSocket.

| Servicio | Puerto host | Ruta |
| --- | --- | --- |
| gateway | 80 | `/graphql/`, `/ws/notificaciones` |
| graphql-bff | 8004 | `/graphql/` |
| notificaciones | 8005 | `POST /notificar`, `ws/notificaciones` |

El BFF no tiene base de datos. Compone usuarios y productos por HTTP. Los hostnames internos son `servicio-usuarios` y `servicio-productos`.

## Arranque

```bash
cp servicio_auth/.env.example servicio_auth/.env
cp servicio_usuarios/.env.example servicio_usuarios/.env
cp servicio_productos/.env.example servicio_productos/.env
cp notificaciones/.env.example notificaciones/.env
docker compose up --build
```

GraphiQL: `http://localhost/graphql/`

WebSocket: `ws://localhost/ws/notificaciones?token=<access>`

## Tests

```bash
cd graphql-bff && python manage.py test tests
cd notificaciones && python manage.py test
cd servicio_auth && python manage.py test
cd servicio_usuarios && python manage.py test
cd servicio_productos && python manage.py test
```
