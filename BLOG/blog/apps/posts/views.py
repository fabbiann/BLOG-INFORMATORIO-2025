from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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

# Vista para registrar usuarios
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el usuario en la BD
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Bienvenido {username}! Tu cuenta ha sido creada.')
            return redirect('login') # Redirige al login
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})