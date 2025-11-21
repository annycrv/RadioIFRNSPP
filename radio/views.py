from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Home, Programa, Programacao, Sobre,Pedido
from radio.forms import PedidoModelForm, HomeModelForm
from django.core.paginator import Paginator

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
        # "quadros": Quadro.objects.all(),
        # "podcasts": Podcast.objects.all(),
        "dia": dia.capitalize(),
        "page_obj": page_obj,
    }
    return render(request, "radio/programacao.html", context)

def programas(request):
    lista = Programa.objects.all().order_by("nome_programa")

    paginator = Paginator(lista, 9) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "programas": page_obj,
        "page_obj": page_obj,
    }
    return render(request, "radio/programas.html", context)

# def podcasts(request):
#     context = {
#         "podcasts": Podcast.objects.all()
#     }
#     return render(request, "radio/podcasts.html", context)

def sobre(request):
    return render(request, "radio/sobre.html")

@login_required
def redirecionar(request):
    if request.user.is_superuser:
        return redirect("dashboard:index")
    else:
        return redirect("radio:index")