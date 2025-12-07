from django.contrib import admin
from .models import Categoria, Post

# Esta clase permite ver columnas extras en el listado de posts dentro del admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'publicado', 'activo')
    list_filter = ('categoria', 'activo') 

# Registramos los modelos
admin.site.register(Categoria)
admin.site.register(Post, PostAdmin)