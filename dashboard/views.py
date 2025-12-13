from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from radio.models import Programa, Programacao,Episodio, Sugestao, Pedido
from radio.forms import ProgramaModelForm
from radio.forms import ProgramacaoModelForm
from radio.forms import EpisodioModelForm
from usuarios.forms import UsuarioChangeForm
from usuarios.models import Usuario
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def index(request):
    context = {
        "sugestao": Sugestao.objects.all,
        "programacao": Programacao.objects.all,
        "programas": Programa.objects.all,
        "total_programas": Programa.objects.count(),
        "total_programacoes": Programacao.objects.count(),
        "total_usuarios": Usuario.objects.count(),
        "total_curtidos": Programa.objects.filter(curtidas=request.user).count()

    }
    return render(request, "dashboard/index.html", context)


# programas

@login_required
@permission_required("radio.view_programas", raise_exception=True)
def programas(request):
    lista = Programa.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "programas": page_obj,
        "titulo_pagina": "Programas",
        "subtitulo_pagina": "Gerencie os programas da rádio",
        "url_novo": "dashboard:programa_novo",
        "partial_tabela": "dashboard/partials/_tabela_programas.html",
        "texto_botao_novo": "Adicionar Programa",
        "page_obj": page_obj,  
    }
    return render(request, "dashboard/listar.html", context)

@login_required
@permission_required("radio.add_programa", raise_exception=True)
def programa_novo(request):
    context = { 
        "titulo_pagina": "Adicionar programa",
        "url_cancelar": "dashboard:programas",
    }
    if request.method == "POST":
        form = ProgramaModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Programa registrado com sucesso!")
            return redirect("dashboard:programas")
        else:
            messages.error(request, "Falha ao registrar Programa!")
            context["form"] = form
    else:
        context["form"] = ProgramaModelForm()
    return render(request, "dashboard/novo.html", context)


@login_required
@permission_required("radio.change_programa", raise_exception=True)
def programa_editar(request, id_programa):
    context = {
        "programa": get_object_or_404(Programa, id=id_programa),
        "titulo_pagina": "Editar programa",
        "url_cancelar": "dashboard:programas",
    }
    if request.method == "POST":
        form = ProgramaModelForm(request.POST,request.FILES, instance=context["programa"])
        if form.is_valid():
            form.save()
            messages.success(request, "Programa alterado com sucesso!")
            return redirect("dashboard:programas")
        else:
            messages.error(request, "Falha ao alterar programa!")
    else:
        context["form"] = ProgramaModelForm(instance=context["programa"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("radio.delete_programa", raise_exception=True)
def programa_remover(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    context = {
        "programa":programa,
        "tipo": "programa",  
        "objeto": programa.nome_programa, 
    }
    if request.method == "POST":
        context["programa"].delete()
        messages.success(request, "Programa removido com sucesso!")
        return redirect("dashboard:programas")
    else:
        return render(request, "dashboard/remover.html", context)
    
@login_required
@permission_required("radio.view_programa", raise_exception=True)
def programa_detalhar(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)

    context = {
        'programa': programa,
        "titulo_pagina": "Programas",
        'partial_detalhe':"dashboard/partials/_detalhar_programa.html",
        "url_cancelar": "dashboard:programas",
    }
    return render(request, 'dashboard/detalhar.html', context)


# Programacao


@login_required
@permission_required("radio.view_programacao", raise_exception=True)
def programacao(request):
    lista = Programacao.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "programacao": page_obj,
        "titulo_pagina": "Programação",
        "subtitulo_pagina": "Gerencie a programação da rádio",
        "url_novo": "dashboard:programacao_novo",
        "partial_tabela": "dashboard/partials/_tabela_programacoes.html",
        "texto_botao_novo": "Adicionar Programação", 
        "page_obj": page_obj, 
    }
    return render(request, "dashboard/listar.html", context)

@login_required
@permission_required("radio.add_programacao", raise_exception=True)
def programacao_novo(request):
    context = {
        "titulo_pagina": "Adicionar Programação",
        "url_cancelar": "dashboard:programacao",
    }
    if request.method == "POST":
        form = ProgramacaoModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Programação registrada com sucesso!")
            return redirect("dashboard:programacao")
        else:
            messages.error(request, "Falha ao registrar programação!")
            context["form"] = form
    else:
        context["form"] = ProgramacaoModelForm()
    return render(request, "dashboard/novo.html", context)


@login_required
@permission_required("radio.change_programacao", raise_exception=True)
def programacao_editar(request, id_item):
    old = get_object_or_404(Programacao, id=id_item)

    context = {
        "titulo_pagina": "Editar Programação",
        "url_cancelar": "dashboard:programacao",
    }

    if request.method == "POST":
        form = ProgramacaoModelForm(request.POST)
        if form.is_valid():
            programa = form.cleaned_data["programa"]
            dias = form.cleaned_data["dias"]
            horarios = form.cleaned_data["horarios"]

            # Remove o original
            old.delete()

            # recria tudo
            for dia in dias:
                for horario in horarios:
                    Programacao.objects.create(
                        programa=programa,
                        dia=dia,
                        horario=horario
                    )

            messages.success(request, "Programação alterada com sucesso!")
            return redirect("dashboard:programacao")

        context["form"] = form

    else:
        context["form"] = ProgramacaoModelForm(initial={
            "programa": old.programa,
            "dias": [old.dia],
            "horarios": [old.horario],
        })

    return render(request, "dashboard/editar.html", context)


@login_required
@permission_required("radio.delete_programacao", raise_exception=True)
def programacao_remover(request, id_item):
    context = {
        "programacao": get_object_or_404(Programacao, id=id_item),
    }
    if request.method == "POST":
        context["programacao"].delete()
        messages.success(request, "Programação removida com sucesso!")
        return redirect("dashboard:programacao")
    else:
        return render(request, "dashboard/remover.html", context)


# episodios 

@login_required
@permission_required("radio.view_episodios", raise_exception=True)
def episodios(request):

    lista = Episodio.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        "titulo_pagina": "Episódios",
        "subtitulo_pagina": "Gerencie os episódios da rádio",
        "partial_tabela": "dashboard/partials/_tabela_episodios.html",
        "page_obj": page_obj, 
    }
    return render(request, "dashboard/listar.html", context)


@login_required
@permission_required("radio.add_episodio", raise_exception=True)
def episodio_novo(request, id_programa):

    programa = get_object_or_404(Programa, id=id_programa)

    context = {
        "titulo_pagina": "Adicionar Episódio",
        "url_cancelar": "dashboard:episodios",
        "programa": get_object_or_404(Programa, id=id_programa),
    }

    if request.method == "POST":
        form = EpisodioModelForm(request.POST, request.FILES)
        if form.is_valid():
            episodio = form.save(commit=False)
            episodio.programa = programa 
            episodio.save()
            messages.success(request, "Episódio registrado com sucesso!")
            return redirect("dashboard:episodios")
        else:
            messages.error(request, "Falha ao registrar episódio!")
            context["form"] = form
    else:
        context["form"] = EpisodioModelForm()

    return render(request, "dashboard/novo.html", context)


@login_required
@permission_required("radio.change_episodio", raise_exception=True)
def episodio_editar(request, id_item):
    context = {
        "episodio": get_object_or_404(Episodio, id=id_item),
        "titulo_pagina": "Editar Episódio",
        "url_cancelar": "dashboard:episodios",
    }
    if request.method == "POST":
        form = EpisodioModelForm(request.POST,request.FILES, instance=context["episodio"])
        if form.is_valid():
            form.save()
            messages.success(request, "Episódio alterado com sucesso!")
            return redirect("dashboard:episodios")
        else:
            messages.error(request, "Falha ao alterar episódio!")
    else:
        context["form"] = EpisodioModelForm(instance=context["episodio"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("radio.delete_episodio", raise_exception=True)
def episodio_remover(request, id_item):
    episodio = get_object_or_404(Episodio, id=id_item)
    context = {
        "episodio": episodio,       
        "tipo": "episódio",        
        "objeto": episodio.titulo, 
    }
    if request.method == "POST":
        context["episodio"].delete()
        messages.success(request, "Episódio removido com sucesso!")
        return redirect("dashboard:episodios")
    else:
        return render(request, "dashboard/remover.html", context)


@login_required
@permission_required("radio.view_episodio", raise_exception=True)
def detalhar_episodio(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    episodios = Episodio.objects.filter(programa=programa).order_by('-id')
    paginator = Paginator(episodios, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        'programa': programa,
        'titulo_pagina': f'Episódios de {programa.nome_programa}',
        'partial_detalhe':"dashboard/partials/_detalhar_episodio.html",
        "url_cancelar": "dashboard:episodios",
        "page_obj": page_obj,  
    }
    return render(request, 'dashboard/detalhar.html', context)

# curtidos

@login_required
def meus_curtidos(request):
    lista = Programa.objects.filter(curtidas=request.user)

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "curtidos": page_obj,
        "titulo_pagina": "Meus Curtidos",
        "partial_tabela": "dashboard/partials/_tabela_curtidos.html",
        "page_obj": page_obj,  
    }
    return render(request, "dashboard/listar.html", context)

# sugestões

@login_required
@permission_required("radio.view_sugestao", raise_exception=True)
def view_sugestoes(request):
    lista = Sugestao.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "sugestao": page_obj,
        "titulo_pagina": "Sugestões",
        "partial_tabela": "dashboard/partials/_tabela_sugestoes.html",
        "page_obj": page_obj, 
    }
    return render(request, "dashboard/listar.html", context)


@login_required
@permission_required("radio.delete_sugestao", raise_exception=True)
def sugestoes_remover(request, id_item):
    sugestao = get_object_or_404(Sugestao, id=id_item)

    if request.method == "POST":
        sugestao.delete()
        messages.success(request, "Sugestão removida com sucesso!")
        return redirect("dashboard:sugestoes")

    return render(request, "dashboard/remover.html", {"sugestao": sugestao})

# pedidos

@login_required
@permission_required("radio.view_pedido", raise_exception=True)
def view_pedidos(request):
    lista = Pedido.objects.all().order_by("-id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "pedidos": page_obj,
        "titulo_pagina": "Pedidos",
        "partial_tabela": "dashboard/partials/_tabela_pedidos.html",
        "page_obj": page_obj, 
    }
    return render(request, "dashboard/listar.html", context)


@login_required
@permission_required("radio.delete_pedido", raise_exception=True)
def pedidos_remover(request, id_item):
    pedido = get_object_or_404(Pedido, id=id_item)

    if request.method == "POST":
        pedido.delete()
        messages.success(request, "Pedido removido com sucesso!")
        return redirect("dashboard:pedidos")

    return render(request, "dashboard/remover.html", {"pedido": pedido})

#perfil

@login_required   
def perfil(request):
    context = {
        "titulo_pagina": "Meu Perfil",
        "partial_tabela": "dashboard/partials/_tabela_perfil.html",
    }
    return render(request, "dashboard/listar.html",context)

@login_required
def editar_perfil(request):

    context = {
        "titulo_pagina": "Editar Perfil",
        "url_cancelar": "dashboard:perfil",
    }

    if request.method == "POST":
        form = UsuarioChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("dashboard:perfil")
        else:
            messages.error(request, "Falha ao atualizar o perfil. Verifique os dados.")
    else:
        form = UsuarioChangeForm(instance=request.user)

    context["form"] = form

    return render(request, "dashboard/editar.html", context)
