from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Home, Programa, Programacao, Sobre,Pedido,Episodio
from radio.forms import PedidoModelForm, HomeModelForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    context = {
        "home": Home.objects.first()
    }
    if request.method == "POST":
        form = HomeModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            context["form"] = form
    else:
        context["form"] = HomeModelForm()
    return render(request, "radio/index.html", context)

@login_required
def pedidos(request):
    context = {
        "pedido": Pedido.objects.first(),
    }
    if request.method == "POST":
        form = PedidoModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pedidos")
        else:
            context["form"] = form
    else:
        context["form"] = PedidoModelForm()
    return render(request, "radio/pedidos.html", context)


def programacao(request,dia):
    dias_validos = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
    if dia not in dias_validos:
        dia = 'segunda' 
    
    lista = Programacao.objects.filter(dia=dia).order_by("programa")

    paginator = Paginator(lista, 9) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "programacao": page_obj,
        # "podcasts": Podcast.objects.all(),
        "dia": dia.capitalize(),
        "page_obj": page_obj,
    }
    return render(request, "radio/programacao.html", context)

def programas(request):
    lista = Programa.objects.all().order_by("nome_programa")

    paginator = Paginator(lista, 6) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "programas": page_obj,
        "page_obj": page_obj,
    }
    return render(request, "radio/programas.html", context)

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
def registrar_curtida(request):
    if request.method == "POST":
        postagem = get_object_or_404(Programa, id=request.POST["id_programa"])
        if not request.user in postagem.curtidas.all():
            postagem.curtidas.add(request.user)
        else:
            postagem.curtidas.remove(request.user)
        return redirect(request.POST.get("next", "programas"))
    return redirect(request.POST.get("next", "programas"))