from django.shortcuts import render,redirect
from .models import Home, Programacao,Programa, Podcast, Sobre,Pedido
from radio.forms import PedidoModelForm, HomeModelForm

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

    context = {
        "programacao": Programacao.objects.filter(dia_semana=dia),
        "programas": Programa.objects.all(),
        "podcasts": Podcast.objects.all(),
        "dia": dia.capitalize(),
    }
    return render(request, "radio/programacao.html", context)

def programas(request):
    context = {
        "programas": Programa.objects.all()
    }
    return render(request, "radio/programas.html", context)

def podcasts(request):
    context = {
        "podcasts": Podcast.objects.all()
    }
    return render(request, "radio/podcasts.html", context)

def sobre(request):
    return render(request, "radio/sobre.html")