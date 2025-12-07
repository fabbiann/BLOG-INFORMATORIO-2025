from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comentario
from .forms import ComentarioForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

# Vista del inicio (Index)
def index(request):
    posts = Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'index.html', ctx)

# Vista del detalle del post + Comentarios
def detalle_post(request, pk):
    # Buscamos el post o devolvemos error 404 si no existe
    post = get_object_or_404(Post, pk=pk)
    # Traemos los comentarios de este post específico
    comentarios = post.comentarios.all()

    if request.method == 'POST':
        # Solo usuarios logueados pueden comentar
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.posts = post  # Asignamos el post actual
                comentario.usuario = request.user # Asignamos el usuario actual
                comentario.save() # Guardamos en BD
                return redirect('detalle', pk=post.pk) # Recargamos la página
        else:
            return redirect('login') # Si no está logueado, lo mandamos al login
    else:
        form = ComentarioForm()

    ctx = {
        'post': post,
        'comentarios': comentarios,
        'form': form
    }
    return render(request, 'detalle_post.html', ctx)

# Vista de registro (La que ya tenías)
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Bienvenido {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

# Vista para filtrar por categoría
def posts_por_categoria(request, categoria_id):
    # Buscamos la categoría o error 404
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Filtramos los posts que tengan esa categoría
    posts = Post.objects.filter(categoria=categoria)
    
    ctx = {
        'posts': posts,
        'categoria_seleccionada': categoria
    }
    return render(request, 'index.html', ctx) # Reutilizamos el index para mostrar la lista



def acerca_de(request):
    return render(request, 'acerca_de.html')

def contacto(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del formulario
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje') + " / Email del usuario: " + request.POST.get('email_usuario')
        email_origen = settings.EMAIL_HOST_USER # (Configuración ficticia por ahora)
        email_destino = ['tu_correo_real@gmail.com'] # Aquí llegaría el correo en la vida real

        # 2. Enviamos el correo (Al estar en modo consola, saldrá en la terminal)
        send_mail(
            asunto,
            mensaje,
            email_origen,
            email_destino,
            fail_silently=False,
        )
        
        # 3. Redirigimos o mostramos mensaje de éxito
        return render(request, 'contacto.html', {'mensaje_enviado': True})
    
    return render(request, 'contacto.html')