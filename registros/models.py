from django.db import models
from etiquetas.models import Etiqueta

# Create your models here.

class Registro(models.Model):
    etiqueta = models.ForeignKey(Etiqueta, null=True, on_delete=models.SET_NULL, verbose_name="Etiqueta")
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    valor = models.IntegerField(verbose_name="Valor")
    fecha = models.DateField(verbose_name= "Fecha")

    def __str__(self) -> str:
        return f"{self.etiqueta}, {self.descripcion}, {self.valor}, {self.fecha}"