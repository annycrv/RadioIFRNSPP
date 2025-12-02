from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Usuario
from .forms import UsuarioForm, UsuarioCreationForm
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UsuarioChangeForm

def cadastro(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuário {username} criado com sucesso! Faça login para acessar o sistema.")
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    
    context = {
        "form": form,
    }
    return render(request, "usuarios/cadastro.html", context)

@permission_required("usuarios.view_usuario", raise_exception=True)
def usuarios(request):
    lista = Usuario.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "usuarios": page_obj,
        "titulo_pagina": "Usuários",
        "url_novo": "usuarios:usuarios_novo",
        "partial_tabela": "dashboard/partials/_tabela_usuarios.html",
        "texto_botao_novo": "Adicionar Usuário",
        "page_obj": page_obj
    }
    return render(request, "dashboard/listar.html", context)

@login_required
@permission_required("usuarios.add_usuario", raise_exception=True)
def usuarios_novo(request):
    context = {
        "titulo_pagina": "Novo Usuário",
        "url_cancelar": "dashboard:usuarios"
    }
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuário {username} criado com sucesso!")
            return redirect("usuarios:usuarios")
        else:
            messages.error(request, "Falha ao criar usuário!")
    else:
        context["form"] = UsuarioCreationForm()
    return render(request, "dashboard/novo.html", context)

@login_required
@permission_required("usuarios.change_usuario", raise_exception=True)
def usuarios_editar(request, id_usuario):
    context = {
        "usuario": get_object_or_404(Usuario, id=id_usuario),
        "titulo_pagina": "Editar Usuario",
        "url_cancelar": "dashboard:usuarios"
    }
    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES, instance=context["usuario"])
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuário {username} alterado com sucesso!")

            return redirect("usuarios:usuarios")
        else:
            messages.error(request, "Falha ao alterar usuário!")
    else:
        context["form"] = UsuarioForm(instance=context["usuario"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("usuarios.delete_usuario", raise_exception=True)
def usuarios_remover(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    context = {
        "usuario": usuario,            # objeto singular
        "tipo": "usuário",             # para mostrar no título do template
        "objeto": usuario.get_full_name() or usuario.username,  # para exibir no template
        "titulo_pagina": "Remover Usuário",
    }
    if request.method == "POST":
        context["usuario"].delete()
        messages.success(request, "Usuário removido com sucesso!")
        return redirect("usuarios:usuarios")
    else:
        return render(request, "dashboard/remover.html", context)

@login_required   
def perfil(request):
    return render(request, "registration/perfil.html")

@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = UsuarioChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado!")
            return redirect("usuarios:perfil")
        else:
            messages.success(request, "Falha ao atualizar o perfil!")
    else:
        form = UsuarioChangeForm(instance=request.user)
    return render(request, "registration/editar_perfil.html", {"form": form})