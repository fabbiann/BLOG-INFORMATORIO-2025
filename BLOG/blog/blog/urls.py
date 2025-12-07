from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.posts.views import index , registrar_usuario 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), # Ruta raíz
    # RUTAS DE AUTENTICACIÓN (Login, Logout, Password reset)
    path('accounts/', include('django.contrib.auth.urls')), 

    # NUEVA RUTA DE REGISTRO
    path('registro/', registrar_usuario, name='registro'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)