from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Usuario
from .forms import UsuarioForm, UsuarioCreationForm

def cadastro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    
    context = {
        "form": form,
    }
    return render(request, "usuarios/cadastro.html", context)

@permission_required("usuarios.view_usuario", raise_exception=True)
def usuarios(request):
    context = {
        "usuarios": Usuario.objects.all(),
        "titulo_pagina": "Usuários",
        "url_novo": "usuarios:usuarios_novo",
        "partial_tabela": "dashboard/partials/_tabela_usuarios.html",
        "texto_botao_novo": "Adicionar Usuário",
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
            return redirect("usuarios:usuarios")
        else:
            context["form"] = form
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
            return redirect("usuarios:usuarios")
        else:
            context["form"] = form
    else:
        context["form"] = UsuarioForm(instance=context["usuario"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("usuarios.delete_usuario", raise_exception=True)
def usuarios_remover(request, id_usuario):
    context = {
        "usuario": get_object_or_404(Usuario, id=id_usuario),
        "titulo_pagina": "Remover Usuario",
    }
    if request.method == "POST":
        context["usuario"].delete()
        return redirect("usuarios:usuarios")
    else:
        return render(request, "dashboard/remover.html", context)