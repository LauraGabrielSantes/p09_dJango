
import logging


class DatabaseAuditHandler(logging.Handler):
    """Guarda los eventos del logger de auditoría en la BD."""

    def emit(self, record):
        try:
            # Importación diferida para evitar problemas durante
            # la inicialización de Django.
            from autentificacion.models import RegistroAuditoria

            RegistroAuditoria.objects.create(
                fecha=__import__(
                    "datetime"
                ).datetime.fromtimestamp(
                    record.created,
                    tz=__import__("datetime").timezone.utc,
                ),
                nivel=record.levelname,
                logger=record.name,
                mensaje=record.getMessage(),
            )
        except Exception:
            # Reporta el fallo del handler sin propagar la excepción
            # a la operación de negocio que originó el log.
            self.handleError(record)
