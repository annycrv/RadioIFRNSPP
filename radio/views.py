from django.shortcuts import render
from .models import Home, Programacao,Programa, Podcast, Sobre

def index(request):
    context = {
        "home": Home.objects.first()
    }
    return render(request, "radio/index.html", context)

def pedidos(request):
    return render(request, "radio/pedidos.html")

def programacao(request):
    return render(request, "radio/programacao.html")

def programas(request):
    return render(request, "radio/programas.html")

def podcasts(request):
    return render(request, "radio/podcasts.html")

def sobre(request):
    return render(request, "radio/sobre.html")