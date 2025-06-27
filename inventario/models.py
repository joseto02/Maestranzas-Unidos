from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator



# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.TextField()
    fabricante = models.CharField(max_length=100, default='')
    modelo = models.CharField(max_length=100, default='')
    n_serie = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    nivel_minimo = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.CharField(max_length=100, default='')
    ubicacion = models.CharField(max_length=100, default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def delete(self, using = None, keep_parents = False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
        

class Movimiento(models.Model):
    
    TIPO_CHOICES = [
    ('entrada', 'Entrada'),
    ('salida', 'Salida'),
    ('creación', 'Creación'),
    ('edición', 'Edición'),
    ('eliminación', 'Eliminación'),
    ]
    
    componente = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    origen = models.CharField(max_length=100, null=True, blank=True)
    destino = models.CharField(max_length=100, null=True, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return f"{self.tipo.upper()} - {self.componente.nombre} ({self.cantidad})"
    