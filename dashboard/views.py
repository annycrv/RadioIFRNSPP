from django.shortcuts import render, redirect, get_list_or_404
from radio.models import Home, Programacao, Programa, Podcast, Sobre

def index(request):
    context = {
        "home": Home.objects.all,
        "programacao": Programacao.objects.all,
        "programa": Programa.objects.all,
        "podcast": Podcast.objects.all,
        "sobre": Sobre.objects.all
    }
    return render(request, "dashboard/index.html", context)

