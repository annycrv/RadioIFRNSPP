from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from radio.models import Home, Programacao, Quadro, Podcast, Sobre
from radio.forms import QuadroModelForm, ProgramacaoModelForm 

def index(request):
    context = {
        "home": Home.objects.all,
        "programacao": Programacao.objects.all,
        "quadros": Quadro.objects.all,
        "podcast": Podcast.objects.all,
        "sobre": Sobre.objects.all,
        "total_quadros": Quadro.objects.count(),
        "total_programacoes": Programacao.objects.count(),
        # "total_usuarios": User.objects.count(),
    }
    return render(request, "dashboard/index.html", context)

def quadros(request):
    context = {
        "quadros": Quadro.objects.all(),
    }
    return render(request, "dashboard/quadros.html", context)


def quadro_novo(request):
    context = {}
    if request.method == "POST":
        form = QuadroModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:quadros")
        else:
            context["form"] = form
    else:
        context["form"] = QuadroModelForm()
    return render(request, "dashboard/quadro_novo.html", context)

# def quadro_detalhar(request, id_post):
#     return render(request,"dashboard/quadro_detalhar.html",{"post": get_object_or_404(Quadro, id=id_post)})

def quadro_editar(request, id_quadro):
    context = {
        "quadro": get_object_or_404(Quadro, id=id_quadro),
    }
    if request.method == "POST":
        form = QuadroModelForm(request.POST, instance=context["quadro"])
        if form.is_valid():
            form.save()
            return redirect("dashboard:quadros")
        else:
            context["form"] = form
    else:
        context["form"] = QuadroModelForm(instance=context["quadro"])
    return render(request, "dashboard/quadro_editar.html", context)


def quadro_remover(request, id_quadro):
    context = {
        "quadro": get_object_or_404(Quadro, id=id_quadro),
    }
    if request.method == "POST":
        context["quadro"].delete()
        return redirect("dashboard:quadros")
    else:
        return render(request, "dashboard/quadro_remover.html", context)