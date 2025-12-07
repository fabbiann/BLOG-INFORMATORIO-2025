from django.shortcuts import render
from .models import Post

# Vista para la página de inicio
def index(request):
    # Obtener todos los posts de la base de datos
    posts = Post.objects.all()
    
    # Crear el contexto (la cajita de datos que viaja al HTML)
    ctx = {
        'posts': posts
    }
    
    # Renderizar el template con los datos
    return render(request, 'index.html', ctx)