from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Apresentador,Programa, Programacao,Pedido,Episodio, Sugestao
from radio.forms import PedidoModelForm, SugestaoModelForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse

def sugestao_ajax(request):
    if request.method == "POST":

        form = SugestaoModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Sugestão registrada com sucesso!"
            )

            mensagens_html = render(
                request,
                "dashboard/partials/_messages.html"
            ).content.decode("utf-8")

            return JsonResponse({
                "sucesso": True,
                "mensagens": mensagens_html
            })

        messages.error(
            request,
            "Falha ao registrar sugestão!"
        )

        mensagens_html = render(
            request,
            "dashboard/partials/_messages.html"
        ).content.decode("utf-8")

        return JsonResponse({
            "sucesso": False,
            "mensagens": mensagens_html
        }, status=400)

    return JsonResponse(
        {"erro": "Método não permitido"},
        status=405
    )

def index(request):
    context = {
        "sugestao": Sugestao.objects.first()
    }
    if request.method == "POST":
        form = SugestaoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sugestão registrada com sucesso!")
            return redirect("radio:index")
        else:
            messages.error(request, "Falha ao registrar sugestão!")
    else:
        context["form"] = SugestaoModelForm()
    return render(request, "radio/index.html", context)

@login_required
def pedido_ajax(request):
    if request.method == "POST":

        form = PedidoModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Pedido de música registrado com sucesso!"
            )

            mensagens_html = render(
                request,
                "dashboard/partials/_messages.html"
            ).content.decode("utf-8")

            return JsonResponse({
                "sucesso": True,
                "mensagens": mensagens_html
            })

        messages.error(
            request,
            "Falha ao registrar pedido de música!"
        )

        mensagens_html = render(
            request,
            "dashboard/partials/_messages.html"
        ).content.decode("utf-8")

        return JsonResponse({
            "sucesso": False,
            "mensagens": mensagens_html
        }, status=400)

    return JsonResponse(
        {"erro": "Método não permitido"},
        status=405
    )

@login_required
def pedidos(request):
    context = {
        "pedido": Pedido.objects.first(),
    }
    if request.method == "POST":
        form = PedidoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido de música registrado com sucesso!")
            return redirect("radio:pedidos")
        else:
            messages.error(request, "Falha ao registrar pedido de música!")
    else:
        context["form"] = PedidoModelForm()
    return render(request, "radio/pedidos.html", context)


def programacao(request,dia):
    dias_validos = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
    if dia not in dias_validos:
        dia = 'segunda' 
    
    lista = Programacao.objects.filter(dia=dia).order_by("programa")

    paginator = Paginator(lista, 6) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "programacao": page_obj,
        "dia": dia.capitalize(),
        "page_obj": page_obj,
    }
    return render(request, "radio/programacao.html", context)


def programas(request):
    filtro = request.GET.get("f", "")

    programas_filtrados = Programa.objects.all()

    if filtro:
        programas_filtrados = Programa.objects.filter(
            nome_programa__icontains=filtro,
        ) | Programa.objects.filter(
            apresentador_programa__icontains=filtro,
        )

    programas_filtrados = programas_filtrados.order_by("nome_programa")

    paginator = Paginator(programas_filtrados, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    apresentadores = Apresentador.objects.all()

    return render(request, "radio/programas.html", {
        "programas": page_obj,
        "page_obj": page_obj,
        "filtro": filtro,
        "apresentadores": apresentadores,
    })

def episodios(request, id_programa):
    programa = get_object_or_404(Programa,id=id_programa)
    episodios = Episodio.objects.filter(programa=programa)

    context = {
        "programa": programa,
        "episodios": episodios
    }

    return render(request, "radio/episodios.html",context)


def sobre(request):
    return render(request, "radio/sobre.html")

@login_required
def curtida_ajax(request):
    if request.method == "POST":
        programa = get_object_or_404(
            Programa,
            id=request.POST["id_programa"]
        )

        if request.user in programa.curtidas.all():
            programa.curtidas.remove(request.user)
            curtido = False
        else:
            programa.curtidas.add(request.user)
            curtido = True

        return JsonResponse({
            "curtido": curtido,
            "total_curtidas": programa.curtidas.count()
        })

    return JsonResponse(
        {"erro": "Método não permitido"},
        status=405
    )
    
@login_required
def registrar_curtida(request):
    if request.method == "POST":
        postagem = get_object_or_404(Programa, id=request.POST["id_programa"])
        if not request.user in postagem.curtidas.all():
            postagem.curtidas.add(request.user)
        else:
            postagem.curtidas.remove(request.user)
        return redirect(request.POST.get("next", "radio:programas"))
    return redirect(request.POST.get("next", "radio:programas"))