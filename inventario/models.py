from django.db import models


# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.TextField()
    fabricante = models.CharField(max_length=100, default='Fabricante Desconocido')
    modelo = models.CharField(max_length=100, default='Modelo Desconocido')
    n_serie = models.IntegerField(default=0)
    stock = models.IntegerField()
    categoria = models.CharField(max_length=100, default='Sin categoria')
    ubicacion = models.CharField(max_length=100, default='Ubicacion no asignada')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def delete(self, using = None, keep_parents = False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()