from django.db import models
from django.utils import timezone

# 1. Modelo Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre

# 2. Modelo Post
class Post(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    subtitulo = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    
    # Relación con Categoría (1 a N)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default='Sin categoría')
    
    # Imagen del post (Requiere la librería Pillow instalada)
    imagen = models.ImageField(null=True, blank=True, upload_to='imagenes', default='static/post_default.png')
    
    publicado = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publicado',) # Ordena por fecha de publicación descendente

    def __str__(self):
        return self.titulo

    # Método para borrar la imagen física cuando se borra el post de la BD
    def delete(self, using=None, keep_parents=False):
        self.imagen.delete(self.imagen.name)
        super().delete()