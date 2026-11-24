
from django.db import models


class RegistroAuditoria(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)
    nivel = models.CharField(max_length=20, default="INFO")
    logger = models.CharField(max_length=100, default="auditoria")
    mensaje = models.TextField()

    class Meta:
        db_table = "registro_auditoria"
        ordering = ["-fecha"]
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"

    def __str__(self):
        return f"[{self.fecha}] [{self.nivel}] {self.mensaje[:100]}"
