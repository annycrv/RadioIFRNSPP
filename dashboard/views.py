from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from radio.models import Apresentador, Programa, Programacao,Episodio, Sugestao, Pedido
from radio.forms import ApresentadorModelForm
from radio.forms import ProgramaModelForm
from radio.forms import ProgramacaoModelForm
from radio.forms import EpisodioModelForm
from usuarios.forms import UsuarioChangeForm
from usuarios.models import Usuario
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import JsonResponse 
import time
from django.urls import reverse
from django.http import HttpResponse


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


def ajax_mensagens(request):
    messages = get_messages(request)
    return render(request, 'dashboard/partials/_messages.html', {'messages': messages})
#apresentadores

@login_required
@permission_required("radio.view_apresentador", raise_exception=True)
def ajax_listar_apresentadores(request):

    lista = Apresentador.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "apresentadores": page_obj,
        "partial_tabela": "dashboard/partials/_tabela_apresentadores.html",
        "page_obj": page_obj,
    }

    return render(request,"dashboard/partials/_conteudo_lista.html",context)

@login_required
@permission_required("radio.view_apresentador", raise_exception=True)
def apresentadores(request):
    lista = Apresentador.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "apresentadores": page_obj,
        "titulo_pagina": "Apresentadores",
        "subtitulo_pagina": "Gerencie os apresentadores da rádio",
        "url_novo": "dashboard:apresentador_novo",
        "url_ajax": reverse("dashboard:ajax_listar_apresentadores"),
        "partial_tabela": "dashboard/partials/_tabela_apresentadores.html",
        "partial_form": "dashboard/partials/_form_generico.html",
        "texto_botao_novo": "Adicionar Apresentador",
        "page_obj": page_obj,
    }
    return render(request, "dashboard/listar.html", context)


@login_required
@permission_required("radio.add_apresentador", raise_exception=True)
def apresentador_novo(request):
    partial_form = "dashboard/partials/_form_generico.html"
    context = {
        "titulo_pagina": "Adicionar apresentador",
        "url_cancelar": "dashboard:apresentadores",
        "url_salvar": reverse("dashboard:apresentador_novo"),
    }

    if request.method == "POST":
        form = ApresentadorModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Apresentador registrado com sucesso!")
            return HttpResponse("ok")
        else:
            messages.error(request, "Falha ao registrar apresentador!")
            context["form"] = form
    else:
        context["form"] = ApresentadorModelForm()

    return render(request, partial_form, context)


@login_required
@permission_required("radio.change_apresentador", raise_exception=True)
def apresentador_editar(request, id_apresentador):
    apresentador = get_object_or_404(Apresentador, id=id_apresentador)
    partial_form = "dashboard/partials/_form_generico.html"

    context = {
        "apresentador": apresentador,
        "titulo_pagina": "Editar apresentador",
        "url_cancelar": "dashboard:apresentadores",
        "partial_form": "dashboard/partials/_form_generico.html",
        "url_salvar": reverse(
            "dashboard:apresentador_editar",
            args=[apresentador.id]
        ),
    }

    if request.method == "POST":
        form = ApresentadorModelForm(
            request.POST,
            request.FILES,
            instance=apresentador
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Apresentador alterado com sucesso!")
            return HttpResponse("ok")
        else:
            messages.error(request, "Falha ao alterar apresentador!")
    else:
        context["form"] = ApresentadorModelForm(instance=apresentador)

    return render(request, partial_form, context)


@login_required
@permission_required("radio.delete_apresentador", raise_exception=True)
def apresentador_remover(request, id_apresentador):
    apresentador = get_object_or_404(Apresentador, id=id_apresentador)
    partial_remover = "dashboard/remover.html"
    context = {
        "tipo": "apresentador",
        "objeto": apresentador.nome,
        "url_remover": reverse(
            "dashboard:apresentador_remover",
            args=[apresentador.id]
        ),
    }

    if request.method == "POST":
        apresentador.delete()
        messages.success(request, "Apresentador removido com sucesso!")
        return HttpResponse("ok")
    return render(
        request,
        partial_remover,
        context
    )
    
    
@login_required
@permission_required("radio.view_apresentador", raise_exception=True)
def apresentador_detalhar(request, id_apresentador):
    apresentador = get_object_or_404(Apresentador, id=id_apresentador)
    partial_detalhe = (
        "dashboard/partials/_detalhar_apresentador.html"
    )
    context = {
        "apresentador": apresentador,
        "titulo_pagina": "Apresentador",
        "url_cancelar": "dashboard:apresentadores",
    }
    return render(
        request,
        partial_detalhe,
        context
    )



# programas

@login_required
@permission_required("radio.view_programa", raise_exception=True)
def ajax_listar_programas(request):

    lista = Programa.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "partial_tabela": "dashboard/partials/_tabela_programas.html",
        "programas": page_obj,
        "page_obj": page_obj,
    }

    return render(request, "dashboard/partials/_conteudo_lista.html", context)

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
        "url_ajax": reverse("dashboard:ajax_listar_programas"),
        "partial_tabela": "dashboard/partials/_tabela_programas.html",
        "texto_botao_novo": "Adicionar Programa",
        "page_obj": page_obj,  
    }
    return render(request, "dashboard/listar.html", context)


@login_required
@permission_required("radio.add_programa", raise_exception=True)
def programa_novo(request):
    partial_form = "dashboard/partials/_form_generico.html"
    context = { 
        "titulo_pagina": "Adicionar programa",
        "url_cancelar": "dashboard:programas",
        "url_salvar": reverse("dashboard:programa_novo")
    }
    if request.method == "POST":
        form = ProgramaModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Programa registrado com sucesso!")
            return HttpResponse("ok")
        else:
            messages.error(request, "Falha ao registrar Programa!")
            context["form"] = form
    else:
        context["form"] = ProgramaModelForm()
    return render(request, partial_form, context)


@login_required
@permission_required("radio.change_programa", raise_exception=True)
def programa_editar(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    partial_form = "dashboard/partials/_form_generico.html"
    context = {
        "programa": programa,
        "titulo_pagina": "Editar programa",
        "url_cancelar": "dashboard:programas",
        "url_salvar": reverse(
        "dashboard:programa_editar",
        args=[programa.id]
    ),
    }
    if request.method == "POST":
        form = ProgramaModelForm(request.POST,request.FILES, instance=context["programa"])
        if form.is_valid():
            form.save()
            messages.success(request, "Programa alterado com sucesso!")
            return HttpResponse("ok")
        else:
            messages.error(request, "Falha ao alterar programa!")
    else:
        context["form"] = ProgramaModelForm(instance=context["programa"])
    return render(request, partial_form, context)

@login_required
@permission_required("radio.delete_programa", raise_exception=True)
def programa_remover(request, id_programa):
    partial_remover = "dashboard/remover.html"
    programa = get_object_or_404(Programa, id=id_programa)
    context = {
        "url_remover": reverse(
            "dashboard:programa_remover",
            args=[programa.id]
        ),
        "tipo": "programa",  
        "objeto": programa.nome_programa, 
    }
    if request.method == "POST":
        programa.delete()
        messages.success(request, "Programa removido com sucesso!")
        return HttpResponse("ok")
    return render(request, partial_remover, context)
    
@login_required
@permission_required("radio.view_programa", raise_exception=True)
def programa_detalhar(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    partial_detalhe = (
    "dashboard/partials/_detalhar_programa.html"
)
    context = {
        'programa': programa,
        "titulo_pagina": "Programas",
        "url_cancelar": "dashboard:programas",
    }
    return render(request, partial_detalhe, context)




# Programacao

@login_required
@permission_required("radio.view_programacao", raise_exception=True)
def ajax_listar_programacoes(request):

    lista = Programacao.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "programacao": page_obj,
        "partial_tabela": "dashboard/partials/_tabela_programacoes.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


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
        "url_ajax": reverse(
            "dashboard:ajax_listar_programacoes"
        ),
        "partial_tabela": (
            "dashboard/partials/_tabela_programacoes.html"
        ),
        "texto_botao_novo": "Adicionar Programação",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("radio.add_programacao", raise_exception=True)
def programacao_novo(request):

    partial_form = "dashboard/partials/_form_generico.html"

    context = {
        "titulo_pagina": "Adicionar Programação",
        "url_cancelar": "dashboard:programacao",
        "url_salvar": reverse(
            "dashboard:programacao_novo"
        ),
    }

    if request.method == "POST":

        form = ProgramacaoModelForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Programação registrada com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao registrar programação!"
        )

        context["form"] = form

    else:
        context["form"] = ProgramacaoModelForm()

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("radio.change_programacao", raise_exception=True)
def programacao_editar(request, id_item):

    partial_form = "dashboard/partials/_form_generico.html"

    programacao = get_object_or_404(
        Programacao,
        id=id_item
    )

    context = {
        "programacao": programacao,
        "titulo_pagina": "Editar Programação",
        "url_cancelar": "dashboard:programacao",
        "url_salvar": reverse(
            "dashboard:programacao_editar",
            args=[programacao.id]
        ),
    }

    if request.method == "POST":

        form = ProgramacaoModelForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            programa = form.cleaned_data["programa"]
            dias = form.cleaned_data["dias"]
            horarios = form.cleaned_data["horarios"]

            programacao.delete()

            for dia in dias:
                for horario in horarios:
                    Programacao.objects.create(
                        programa=programa,
                        dia=dia,
                        horario=horario
                    )

            messages.success(
                request,
                "Programação alterada com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao alterar programação!"
        )

        context["form"] = form

    else:

        context["form"] = ProgramacaoModelForm(
            initial={
                "programa": programacao.programa,
                "dias": [programacao.dia],
                "horarios": [programacao.horario],
            }
        )

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("radio.delete_programacao", raise_exception=True)
def programacao_remover(request, id_item):

    partial_remover = "dashboard/remover.html"

    programacao = get_object_or_404(
        Programacao,
        id=id_item
    )

    context = {
        "tipo": "programação",
        "objeto": (
            f"{programacao.programa} - "
            f"{programacao.dia} - "
            f"{programacao.horario}"
        ),
        "url_remover": reverse(
            "dashboard:programacao_remover",
            args=[programacao.id]
        ),
    }

    if request.method == "POST":

        programacao.delete()

        messages.success(
            request,
            "Programação removida com sucesso!"
        )

        return HttpResponse("ok")

    return render(
        request,
        partial_remover,
        context
    )


# episodios 

@login_required
@permission_required("radio.view_episodio", raise_exception=True)
def ajax_listar_episodios(request):

    lista = Episodio.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        "partial_tabela": "dashboard/partials/_tabela_episodios.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


@login_required
@permission_required("radio.view_episodio", raise_exception=True)
def episodios(request):

    lista = Episodio.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        "titulo_pagina": "Episódios",
        "subtitulo_pagina": "Gerencie os episódios da rádio",
        "url_ajax": reverse(
            "dashboard:ajax_listar_episodios"
        ),
        "partial_tabela": (
            "dashboard/partials/_tabela_episodios.html"
        ),
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("radio.add_episodio", raise_exception=True)
def episodio_novo(request, id_programa):

    partial_form = "dashboard/partials/_form_generico.html"

    programa = get_object_or_404(
        Programa,
        id=id_programa
    )

    context = {
        "programa": programa,
        "titulo_pagina": "Adicionar Episódio",
        "url_cancelar": "dashboard:episodios",
        "url_salvar": reverse(
            "dashboard:episodio_novo",
            args=[programa.id]
        ),
    }

    if request.method == "POST":

        form = EpisodioModelForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            episodio = form.save(commit=False)
            episodio.programa = programa
            episodio.save()

            messages.success(
                request,
                "Episódio registrado com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao registrar episódio!"
        )

        context["form"] = form

    else:
        context["form"] = EpisodioModelForm()

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("radio.change_episodio", raise_exception=True)
def episodio_editar(request, id_item):

    partial_form = "dashboard/partials/_form_generico.html"

    episodio = get_object_or_404(
        Episodio,
        id=id_item
    )

    context = {
        "episodio": episodio,
        "titulo_pagina": "Editar Episódio",
        "url_cancelar": "dashboard:episodios",
        "url_salvar": reverse(
            "dashboard:episodio_editar",
            args=[episodio.id]
        ),
    }

    if request.method == "POST":

        form = EpisodioModelForm(
            request.POST,
            request.FILES,
            instance=episodio
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Episódio alterado com sucesso!"
            )

            return HttpResponse("ok")

        messages.error(
            request,
            "Falha ao alterar episódio!"
        )

        context["form"] = form

    else:

        context["form"] = EpisodioModelForm(
            instance=episodio
        )

    return render(
        request,
        partial_form,
        context
    )


@login_required
@permission_required("radio.delete_episodio", raise_exception=True)
def episodio_remover(request, id_item):

    partial_remover = "dashboard/remover.html"

    episodio = get_object_or_404(
        Episodio,
        id=id_item
    )

    context = {
        "tipo": "episódio",
        "objeto": episodio.titulo,
        "url_remover": reverse(
            "dashboard:episodio_remover",
            args=[episodio.id]
        ),
    }

    if request.method == "POST":

        episodio.delete()

        messages.success(
            request,
            "Episódio removido com sucesso!"
        )

        return HttpResponse("ok")

    return render(
        request,
        partial_remover,
        context
    )


@login_required
@permission_required("radio.view_episodio", raise_exception=True)
def detalhar_episodio(request, id_programa):

    programa = get_object_or_404(
        Programa,
        id=id_programa
    )

    episodios = Episodio.objects.filter(
        programa=programa
    ).order_by("-id")

    paginator = Paginator(episodios, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        "programa": programa,
        "titulo_pagina":
            f"Episódios - {programa.nome_programa}",
        "subtitulo_pagina":
            "Gerencie os episódios deste programa",
        "partial_tabela":
            "dashboard/partials/_detalhar_episodio.html",
        "url_ajax": reverse(
            "dashboard:ajax_listar_episodios_programa",
            args=[programa.id]
        ),
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("radio.view_episodio", raise_exception=True)
def ajax_listar_episodios_programa(request, id_programa):

    programa = get_object_or_404(
        Programa,
        id=id_programa
    )

    episodios = Episodio.objects.filter(
        programa=programa
    ).order_by("-id")

    paginator = Paginator(episodios, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "episodios": page_obj,
        "page_obj": page_obj,
        "partial_tabela":
            "dashboard/partials/_detalhar_episodio.html",
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


# curtidos

@login_required
def ajax_listar_curtidos(request):

    lista = Programa.objects.filter(
        curtidas=request.user
    )

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "curtidos": page_obj,
        "partial_tabela":
            "dashboard/partials/_tabela_curtidos.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )

@login_required
def meus_curtidos(request):

    lista = Programa.objects.filter(
        curtidas=request.user
    )

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "curtidos": page_obj,
        "titulo_pagina": "Meus Curtidos",
        "subtitulo_pagina":
            "Programas curtidos por você",
        "url_ajax": reverse(
            "dashboard:ajax_listar_curtidos"
        ),
        "partial_tabela":
            "dashboard/partials/_tabela_curtidos.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )

# sugestões

@login_required
@permission_required("radio.view_sugestao",raise_exception=True)
def ajax_listar_sugestoes(request):

    lista = Sugestao.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "sugestao": page_obj,
        "partial_tabela":
            "dashboard/partials/_tabela_sugestoes.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


@login_required
@permission_required("radio.view_sugestao",raise_exception=True)
def view_sugestoes(request):

    lista = Sugestao.objects.all().order_by("id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "sugestao": page_obj,
        "titulo_pagina": "Sugestões",
        "subtitulo_pagina":
            "Sugestões enviadas pelos usuários",
        "url_ajax": reverse(
            "dashboard:ajax_listar_sugestoes"
        ),
        "partial_tabela":
            "dashboard/partials/_tabela_sugestoes.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("radio.delete_sugestao",raise_exception=True)
def sugestoes_remover(request, id_item):

    partial_remover = "dashboard/remover.html"

    sugestao = get_object_or_404(
        Sugestao,
        id=id_item
    )

    context = {
        "tipo": "sugestão",
        "objeto": str(sugestao),
        "url_remover": reverse(
            "dashboard:sugestoes_remover",
            args=[sugestao.id]
        ),
    }

    if request.method == "POST":

        sugestao.delete()

        messages.success(
            request,
            "Sugestão removida com sucesso!"
        )

        return HttpResponse("ok")

    return render(
        request,
        partial_remover,
        context
    )

# pedidos
@login_required
@permission_required("radio.view_pedido",raise_exception=True)
def ajax_listar_pedidos(request):

    lista = Pedido.objects.all().order_by("-id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "pedidos": page_obj,
        "partial_tabela":
            "dashboard/partials/_tabela_pedidos.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/partials/_conteudo_lista.html",
        context
    )


@login_required
@permission_required("radio.view_pedido",raise_exception=True)
def view_pedidos(request):

    lista = Pedido.objects.all().order_by("-id")

    paginator = Paginator(lista, 6)
    pagina_atual = request.GET.get("page")
    page_obj = paginator.get_page(pagina_atual)

    context = {
        "pedidos": page_obj,
        "titulo_pagina": "Pedidos",
        "subtitulo_pagina":
            "Pedidos enviados pelos ouvintes",
        "url_ajax": reverse(
            "dashboard:ajax_listar_pedidos"
        ),
        "partial_tabela":
            "dashboard/partials/_tabela_pedidos.html",
        "page_obj": page_obj,
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )


@login_required
@permission_required("radio.delete_pedido",raise_exception=True)
def pedidos_remover(request, id_item):

    partial_remover = "dashboard/remover.html"

    pedido = get_object_or_404(
        Pedido,
        id=id_item
    )

    context = {
        "tipo": "pedido",
        "objeto": str(pedido),
        "url_remover": reverse(
            "dashboard:pedidos_remover",
            args=[pedido.id]
        ),
    }

    if request.method == "POST":

        pedido.delete()

        messages.success(
            request,
            "Pedido removido com sucesso!"
        )

        return HttpResponse("ok")

    return render(
        request,
        partial_remover,
        context
    )

#perfil

@login_required
def perfil(request):

    context = {
        "titulo_pagina": "Meu Perfil",
        "subtitulo_pagina":
            "Gerencie suas informações",
        "partial_tabela":
            "dashboard/partials/_tabela_perfil.html",
    }

    return render(
        request,
        "dashboard/listar.html",
        context
    )

@login_required
def editar_perfil(request):

    context = {
        "titulo_pagina": "Editar Perfil",
        "url_cancelar": "dashboard:perfil",
        "partial_form": "dashboard/partials/_form_perfil.html",
    }

    if request.method == "POST":

        form = UsuarioChangeForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Perfil atualizado com sucesso!"
            )

            return redirect("dashboard:perfil")

        messages.error(
            request,
            "Falha ao atualizar perfil!"
        )

    else:

        form = UsuarioChangeForm(
            instance=request.user
        )

    context["form"] = form

    return render(
        request,
        "dashboard/editar.html",
        context
    )
