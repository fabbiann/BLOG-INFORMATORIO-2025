from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.posts.views import index  # Importamos nuestra vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), # Ruta raíz
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)