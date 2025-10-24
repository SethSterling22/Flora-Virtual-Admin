from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Definición de la clase historial
class Historial(models.Model):
    # Tipos de acciones
    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
    ]

    # Campos del historial
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES, verbose_name='Acción')
    modelo_afectado = models.CharField(max_length=100, verbose_name='Modelo Afectado')
    id_objeto = models.PositiveIntegerField(verbose_name='ID del Objeto') 
    usuario = models.CharField(max_length=150, verbose_name='Usuario') 
    fecha = models.DateTimeField(default=timezone.now, verbose_name='Fecha')
    detalles = models.TextField(blank=True, null=True, verbose_name='Detalles') 
    datos_formulario = models.TextField(blank=True, null=True, verbose_name='Datos del Formulario') 

    def __str__(self):
        return f"{self.accion} - {self.modelo_afectado} (ID: {self.id_objeto}) por {self.usuario} el {self.fecha}"

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'
        ordering = ['-fecha'] 