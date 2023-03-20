from django.db import models

# Create your models here.


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=30, verbose_name="Nombre", unique=True)
    oculta = models.BooleanField(verbose_name="Oculta", blank=False)

    def __str__(self) -> str:
        return f"{str.capitalize(self.nombre)}, {self.oculta}"