from django.shortcuts import render

def index(request):
    return render(request, "radio/index.html")

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