from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# AGREGAMOS detalle_post AQUÍ:
from apps.posts.views import index, registrar_usuario, detalle_post, posts_por_categoria, acerca_de, contacto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registrar_usuario, name='registro'),
    
    # NUEVA RUTA PARA VER EL DETALLE
    path('post/<int:pk>/', detalle_post, name='detalle'),

    path('categoria/<int:categoria_id>/', posts_por_categoria, name='posts_por_categoria'),
    path('acerca-de/', acerca_de, name='acerca_de'),
    path('contacto/', contacto, name='contacto'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)