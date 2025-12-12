from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.posts.views import (
    index, 
    registrar_usuario, 
    detalle_post, 
    posts_por_categoria, 
    acerca_de, 
    contacto,
    borrar_comentario,  
    borrar_post,        
    crear_post,          
    editar_post,
    editar_comentario
)

urlpatterns = [
    # Rutas de Administración y Autenticación
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Rutas de Usuario y Estáticas
    path('registro/', registrar_usuario, name='registro'),
    path('acerca-de/', acerca_de, name='acerca_de'),
    path('contacto/', contacto, name='contacto'),

    # Rutas de Posts
    path('post/<int:pk>/', detalle_post, name='detalle'),
    path('categoria/<int:categoria_id>/', posts_por_categoria, name='posts_por_categoria'),
    path('crear_post/', crear_post, name='crear_post'),

    # Rutas de Borrado (Las que daban error)
    path('borrar-comentario/<int:comentario_id>/', borrar_comentario, name='borrar_comentario'),
    path('borrar-post/<int:pk>/', borrar_post, name='borrar_post'),

<<<<<<< HEAD
    # Rutas de Edición
=======
>>>>>>> 9cef5c3ec9f7efba4144bfd1c05d67e0b112b7b7
    path('post/editar/<int:pk>/', editar_post, name='editar_post'),
    path('comentario/editar/<int:comentario_id>/', editar_comentario, name='editar_comentario'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)