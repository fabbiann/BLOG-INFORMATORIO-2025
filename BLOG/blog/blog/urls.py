from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# AGREGAMOS detalle_post AQUÍ:
from apps.posts.views import index, registrar_usuario, detalle_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registrar_usuario, name='registro'),
    
    # NUEVA RUTA PARA VER EL DETALLE
    path('post/<int:pk>/', detalle_post, name='detalle'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)