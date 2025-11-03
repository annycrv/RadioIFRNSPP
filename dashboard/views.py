from django.shortcuts import render, redirect, get_list_or_404
from radio.models import Home, Programacao, Quadro, Podcast, Sobre

def index(request):
    context = {
        "home": Home.objects.all,
        "programacao": Programacao.objects.all,
        "quadros": Quadro.objects.all,
        "podcast": Podcast.objects.all,
        "sobre": Sobre.objects.all
    }
    return render(request, "dashboard/index.html", context)

