from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Usuario
from .forms import UsuarioForm, UsuarioCreationForm
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UsuarioChangeForm
from django.http import HttpResponse
from django.urls import reverse

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

@login_required
@permission_required("usuarios.view_usuario", raise_exception=True)
def ajax_listar_usuarios(request):

    ordenar_por = request.GET.get(
        "ordenar",
        "first_name"
    )

    lista = Usuario.objects.all().order_by(
        ordenar_por,
        "id",
        "email"
    )

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "usuarios": page_obj,
        "partial_tabela":
            "dashboard/partials/_tabela_usuarios.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


@login_required
@permission_required("usuarios.view_usuario", raise_exception=True)
def usuarios(request):

    ordenar_por = request.GET.get(
        "ordenar",
        "first_name"
    )

    lista = Usuario.objects.all().order_by(
        ordenar_por,
        "id",
        "email"
    )

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "usuarios": page_obj,
        "titulo_pagina": "Usuários",
        "subtitulo_pagina":
            "Gerencie os usuários do sistema",
        "url_novo": "usuarios:usuarios_novo",
        "url_ajax":
            reverse("usuarios:ajax_listar_usuarios"),
        "partial_tabela":
            "dashboard/partials/_tabela_usuarios.html",
        "texto_botao_novo":
            "Adicionar Usuário",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("usuarios.add_usuario", raise_exception=True)
def usuarios_novo(request):

    partial_form = (
        "dashboard/partials/_form_generico.html"
    )

    context = {
        "titulo_pagina": "Novo Usuário",
        "url_cancelar": "usuarios:usuarios",
        "url_salvar": reverse(
            "usuarios:usuarios_novo"
        ),
    }

    if request.method == "POST":

        form = UsuarioCreationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            usuario = form.save()

            messages.success(
                request,
                f"Usuário {usuario.username} criado com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao criar usuário!"
        )

        context["form"] = form

    else:

        context["form"] = UsuarioCreationForm()

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("usuarios.change_usuario", raise_exception=True)
def usuarios_editar(request, id_usuario):

    partial_form = (
        "dashboard/partials/_form_generico.html"
    )

    usuario = get_object_or_404(
        Usuario,
        id=id_usuario
    )

    context = {
        "usuario": usuario,
        "titulo_pagina": "Editar Usuário",
        "url_cancelar": "usuarios:usuarios",
        "url_salvar": reverse(
            "usuarios:usuarios_editar",
            args=[usuario.id]
        ),
    }

    if request.method == "POST":

        form = UsuarioForm(
            request.POST,
            request.FILES,
            instance=usuario
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"Usuário {usuario.username} alterado com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao alterar usuário!"
        )

        context["form"] = form

    else:

        context["form"] = UsuarioForm(
            instance=usuario
        )

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("usuarios.delete_usuario", raise_exception=True)
def usuarios_remover(request, id_usuario):

    partial_remover = (
        "dashboard/remover.html"
    )

    usuario = get_object_or_404(
        Usuario,
        id=id_usuario
    )

    context = {
        "tipo": "usuário",
        "objeto":
            usuario.get_full_name()
            or usuario.username,
        "url_remover": reverse(
            "usuarios:usuario_remover",
            args=[usuario.id]
        ),
    }

    if request.method == "POST":

        usuario.delete()

        messages.success(
            request,
            "Usuário removido com sucesso!"
        )

        return HttpResponse("ok")

    return render(
        request,
        partial_remover,
        context
    )
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