from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from radio.models import Home, Programa, Sobre, Programacao
from radio.forms import ProgramaModelForm
from radio.forms import ProgramacaoModelForm
from usuarios.models import Usuario
from django.core.paginator import Paginator

@login_required
@permission_required("radio.view_index", raise_exception=True)
def index(request):
    context = {
        "home": Home.objects.all,
        "programacao": Programacao.objects.all,
        "programas": Programa.objects.all,
        # "podcast": Podcast.objects.all,
        "sobre": Sobre.objects.all,
        "total_programas": Programa.objects.count(),
        "total_programacoes": Programacao.objects.count(),
        "total_usuarios": Usuario.objects.count(),
    }
    return render(request, "dashboard/index.html", context)

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
            return redirect("dashboard:programas")
        else:
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
        form = ProgramaModelForm(request.POST, instance=context["programa"])
        if form.is_valid():
            form.save()
            return redirect("dashboard:programas")
        else:
            context["form"] = form
    else:
        context["form"] = ProgramaModelForm(instance=context["programa"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("radio.delete_programa", raise_exception=True)
def programa_remover(request, id_programa):
    context = {
        "programa": get_object_or_404(Programa, id=id_programa),
    }
    if request.method == "POST":
        context["programa"].delete()
        return redirect("dashboard:programas")
    else:
        return render(request, "dashboard/remover.html", context)
    
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
            return redirect("dashboard:programacao")
        else:
            context["form"] = form
    else:
        context["form"] = ProgramacaoModelForm()
    return render(request, "dashboard/novo.html", context)

@login_required
@permission_required("radio.change_programacao", raise_exception=True)
def programacao_editar(request, id_item):
    context = {
        "programacao": get_object_or_404(Programacao, id=id_item),
        "titulo_pagina": "Editar Programação",
        "url_cancelar": "dashboard:programacao",
    }
    if request.method == "POST":
        form = ProgramacaoModelForm(request.POST, instance=context["programacao"])
        if form.is_valid():
            form.save()
            return redirect("dashboard:programacao")
        else:
            context["form"] = form
    else:
        context["form"] = ProgramacaoModelForm(instance=context["programacao"])
    return render(request, "dashboard/editar.html", context)

@login_required
@permission_required("radio.delete_programacao", raise_exception=True)
def programacao_remover(request, id_item):
    context = {
        "programacao": get_object_or_404(Programacao, id=id_item),
    }
    if request.method == "POST":
        context["programacao"].delete()
        return redirect("dashboard:programacao")
    else:
        return render(request, "dashboard/remover.html", context)
    
