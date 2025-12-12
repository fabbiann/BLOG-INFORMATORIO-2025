from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comentario, Categoria
from .forms import ComentarioForm, PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

# Vista del inicio (Index)
def index(request):
    posts = Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'index.html', ctx)

# Vista del detalle del post + Comentarios
def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comentarios = post.comentarios.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.posts = post
                comentario.usuario = request.user
                comentario.save()
                return redirect('detalle', pk=post.pk)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    ctx = {
        'post': post,
        'comentarios': comentarios,
        'form': form
    }
    return render(request, 'detalle_post.html', ctx)

# Vista para CREAR POST (Solo Colaboradores o Root)
@login_required
@permission_required('posts.add_post', raise_exception=True)
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user 
            post.save()
            messages.success(request, '¡Post creado exitosamente!')
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'crear_post.html', {'form': form})

# Vista para BORRAR POST (Solo Colaboradores o Root)
@login_required
@permission_required('posts.delete_post', raise_exception=True)
def borrar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'El artículo ha sido eliminado.')
    return redirect('index')

# Vista para BORRAR COMENTARIO (Dueño del comentario o Colaborador)
@login_required
def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # ¿Es el dueño O tiene permiso de borrar comentarios (Colaborador)?
    if comentario.usuario == request.user or request.user.has_perm('posts.delete_comentario'):        
        comentario.delete()
        messages.success(request, 'Comentario eliminado.')
    else:
        messages.error(request, 'No tienes permiso para borrar este comentario.')
        
    return redirect('detalle', pk=comentario.posts.pk)

# Vista de registro
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
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categoria=categoria)
    
    ctx = {
        'posts': posts,
        'categoria_seleccionada': categoria
    }
    return render(request, 'index.html', ctx)

# Páginas estáticas
def acerca_de(request):
    return render(request, 'acerca_de.html')

def contacto(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje') + " / Email del usuario: " + request.POST.get('email_usuario')
        email_origen = settings.EMAIL_HOST_USER
        email_destino = ['tu_correo_real@gmail.com']

        send_mail(
            asunto,
            mensaje,
            email_origen,
            email_destino,
            fail_silently=False,
        )
        return render(request, 'contacto.html', {'mensaje_enviado': True})
    
    return render(request, 'contacto.html')

# --- VISTA PARA EDITAR POST (Solo Colaborador/Root) ---
@login_required
@permission_required('posts.change_post', raise_exception=True)
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Artículo actualizado correctamente!')
            return redirect('detalle', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'crear_post.html', {'form': form, 'es_edicion': True})

# --- VISTA PARA EDITAR COMENTARIO (Solo el dueño) ---
@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Validación de dueño
    if comentario.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar este comentario.')
        return redirect('detalle', pk=comentario.posts.pk)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comentario actualizado.')
            return redirect('detalle', pk=comentario.posts.pk)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'editar_comentario.html', {'form': form})